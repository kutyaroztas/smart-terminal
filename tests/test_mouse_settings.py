"""Mouse actions: settings migration/validation and a scripted real-App run.

Run: python3 -m unittest tests.test_mouse_settings -v   (the App tests need a display, e.g. Xvfb)
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import gi  # noqa: E402

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Vte", "2.91")
from gi.repository import Gtk  # noqa: E402

import smart_terminal as tb  # noqa: E402


class SettingsMigration(unittest.TestCase):
    def test_defaults_keep_old_behaviour(self):
        s = tb.normalize_settings({})
        self.assertEqual((s["rightclick_action"], s["middle_action"]), ("menu", "paste"))

    def test_middle_paste_migrates(self):
        self.assertEqual(tb.normalize_settings({"middle_paste": True})["middle_action"], "paste")
        self.assertEqual(tb.normalize_settings({"middle_paste": False})["middle_action"], "none")
        self.assertNotIn("middle_paste", tb.normalize_settings({"middle_paste": True}))

    def test_explicit_middle_action_wins_over_old_key(self):
        s = tb.normalize_settings({"middle_paste": True, "middle_action": "menu"})
        self.assertEqual(s["middle_action"], "menu")

    def test_invalid_values_fall_back(self):
        s = tb.normalize_settings({"rightclick_action": "x", "middle_action": 5})
        self.assertEqual((s["rightclick_action"], s["middle_action"]), ("menu", "paste"))

    def test_valid_values_kept(self):
        s = tb.normalize_settings({"rightclick_action": "paste", "middle_action": "menu"})
        self.assertEqual((s["rightclick_action"], s["middle_action"]), ("paste", "menu"))


class FakeEvent:
    def __init__(self, button):
        self.button = button


class MouseActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = tempfile.mkdtemp()
        tb.SETTINGS_FILE = d + "/s.json"
        tb.BUTTONS_FILE = d + "/b.json"
        cls.app = tb.App()
        cls.app.show_all()
        cls.log = []
        cls.app.paste = lambda term, primary=False: cls.log.append(("paste", primary))
        cls.app.show_terminal_menu = lambda term, ev: cls.log.append(("menu", ev.button))

    @classmethod
    def tearDownClass(cls):
        cls.app.destroy()

    def click(self, button, **settings):
        self.app.settings.update(settings)
        self.log.clear()
        term = self.app.focused_terminal()
        handled = self.app.term_click(term, FakeEvent(button))
        return handled, list(self.log)

    def test_new_behaviour(self):
        cfg = {"rightclick_action": "paste", "middle_action": "menu"}
        self.assertEqual(self.click(3, **cfg), (True, [("paste", False)]))
        self.assertEqual(self.click(2, **cfg), (True, [("menu", 2)]))

    def test_right_click_pastes_even_with_selection(self):
        term = self.app.focused_terminal()
        term.feed(b"hello\r\n")
        term.select_all()
        self.assertTrue(term.get_has_selection())
        self.assertEqual(self.click(3, rightclick_action="paste"), (True, [("paste", False)]))
        self.assertTrue(term.get_has_selection())  # not cleared

    def test_old_modes_unchanged(self):
        self.assertEqual(self.click(2, middle_action="paste"), (True, [("paste", True)]))
        self.assertEqual(self.click(2, middle_action="none"), (True, []))
        self.assertEqual(self.click(3, rightclick_action="menu"), (True, [("menu", 3)]))


if __name__ == "__main__":
    unittest.main()
