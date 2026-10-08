"""Ctrl+click on a path: unit tests (pure helpers) and a scripted real-App run.

Run: python3 -m unittest tests.test_ctrl_click -v   (the App tests need a display)
"""
import os
import re
import shlex
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import gi  # noqa: E402

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Vte", "2.91")
from gi.repository import Gdk, GLib, Gtk  # noqa: E402

import smart_terminal as tb  # noqa: E402


class PathHelpers(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.d, "sub"))
        for name, data in (("a.txt", b"hello\n"), ("Makefile", b"all:\n"), ("bin.dat", b"\x00\x01"), ("empty", b"")):
            with open(os.path.join(self.d, name), "wb") as f:
                f.write(data)

    def test_resolve_relative_absolute_home(self):
        self.assertEqual(tb.resolve_path("a.txt", self.d), os.path.join(self.d, "a.txt"))
        self.assertEqual(tb.resolve_path(self.d + "/sub", "/"), self.d + "/sub")
        self.assertEqual(tb.resolve_path("~", "/"), os.path.expanduser("~"))
        self.assertEqual(tb.resolve_path("sub/../a.txt", self.d), os.path.join(self.d, "a.txt"))

    def test_resolve_strips_ls_markers_and_punctuation(self):
        self.assertEqual(tb.resolve_path("sub/", self.d), os.path.join(self.d, "sub"))
        for tok in ("a.txt,", "a.txt:", "(a.txt)", "a.txt*", "a.txt@", "'a.txt'"):
            self.assertEqual(tb.resolve_path(tok, self.d), os.path.join(self.d, "a.txt"), tok)

    def test_resolve_missing_or_empty(self):
        self.assertIsNone(tb.resolve_path("nope.txt", self.d))
        self.assertIsNone(tb.resolve_path("...", self.d))
        self.assertIsNone(tb.resolve_path("", self.d))

    def test_is_text_file(self):
        self.assertTrue(tb.is_text_file(os.path.join(self.d, "a.txt")))
        self.assertTrue(tb.is_text_file(os.path.join(self.d, "Makefile")))
        self.assertTrue(tb.is_text_file(os.path.join(self.d, "empty")))
        self.assertFalse(tb.is_text_file(os.path.join(self.d, "bin.dat")))
        self.assertFalse(tb.is_text_file(os.path.join(self.d, "sub")))
        self.assertFalse(tb.is_text_file(os.path.join(self.d, "missing")))

    def test_handler_for_picks_text_editor_or_type_handler(self):
        txt = tb.Gio.AppInfo.get_default_for_type("text/plain", False)
        self.assertEqual(getattr(tb.handler_for(os.path.join(self.d, "a.txt")), "get_id", lambda: None)(),
                         getattr(txt, "get_id", lambda: None)())
        jpg = os.path.join(self.d, "pic.jpg")
        with open(jpg, "wb") as f:
            f.write(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01")
        want = tb.Gio.AppInfo.get_default_for_type("image/jpeg", False)
        self.assertEqual(getattr(tb.handler_for(jpg), "get_id", lambda: None)(),
                         getattr(want, "get_id", lambda: None)())
        self.assertIsNotNone(want, "this machine has no default image viewer")

    def fake_lookup(self, line):
        """Like Vte match_check for PATH_PATTERN: the run of words joined by single spaces under a cell."""
        spans, pos = [], 0
        for m in re.finditer(r"\S+(?: \S+)*", line):
            spans.append((m.start(), m.end(), m.group()))
        return lambda col, row: next(((t, 0) for a, b, t in spans if a <= col < b), (None, -1))

    def test_path_at_names_with_spaces(self):
        for name in ("my file.txt", "a b c.txt", "dir with space"):
            path = os.path.join(self.d, name)
            if name.startswith("dir"):
                os.mkdir(path)
            else:
                open(path, "w").close()
        line = f"-rw-r--r-- 1 u u 5 Oct  8 12:00 'my file.txt'  'a b c.txt'  a.txt  'dir with space'"
        look = self.fake_lookup(line)
        for word, want in (("my", "my file.txt"), ("file.txt", "my file.txt"), ("c.txt", "a b c.txt"),
                           ("b", "a b c.txt"), ("a.txt", "a.txt"), ("with", "dir with space")):
            col = line.index(word, line.index("12:00"))
            self.assertEqual(tb.path_at(look, col, 0, self.d), os.path.join(self.d, want), word)
        self.assertIsNone(tb.path_at(look, line.index("Oct"), 0, self.d))
        self.assertIsNone(tb.path_at(look, line.index("12:00"), 0, self.d))
        self.assertIsNone(tb.path_at(look, len(line) + 5, 0, self.d))

    def test_settings_default_and_validation(self):
        self.assertTrue(tb.normalize_settings({})["ctrl_click_open"])
        self.assertFalse(tb.normalize_settings({"ctrl_click_open": 0})["ctrl_click_open"])

    def test_all_languages_have_label(self):
        for lang in tb.LANGS:
            self.assertIn("ctrl_click_open", tb.STRINGS[lang], lang)


def pump(seconds, cond=None):
    end = time.time() + seconds
    while time.time() < end:
        while Gtk.events_pending():
            Gtk.main_iteration()
        if cond and cond():
            return True
        time.sleep(0.02)
    return bool(cond and cond())


@unittest.skipUnless(Gdk.Display.get_default(), "needs a display")
class AppCtrlClick(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = tempfile.mkdtemp()
        tb.SETTINGS_FILE = cls.t + "/s.json"
        tb.BUTTONS_FILE = cls.t + "/b.json"
        cls.work = os.path.realpath(tempfile.mkdtemp())
        os.mkdir(cls.work + "/proj dir")
        os.mkdir(cls.work + "/proj")
        open(cls.work + "/proj/inside-marker.txt", "w").close()
        with open(cls.work + "/notes.txt", "w") as f:
            f.write("hi\n")
        open(cls.work + "/my notes.txt", "w").close()
        open(cls.work + "/pic.jpg", "wb").close()
        with open(cls.work + "/blob.bin", "wb") as f:
            f.write(b"\x00\x01\x02")
        cls.app = tb.App()
        cls.app.show_all()
        cls.app.opened = []
        cls.app.open_file = lambda path: cls.app.opened.append(path) or True  # never launch a real app
        cls.term = cls.app.focused_terminal()
        pump(3, lambda: getattr(cls.term, "shell_pid", None))
        cls.term.feed_child(f"cd {shlex.quote(cls.work)}\n".encode())
        pump(1.5, lambda: tb.terminal_cwd(cls.term) == cls.work)

    @classmethod
    def tearDownClass(cls):
        cls.app.destroy()

    def setUp(self):
        self.app.opened.clear()
        self.app.settings["ctrl_click_open"] = True
        self.term.reset(True, True)  # blank screen without involving the shell
        pump(0.3)
        self.assertEqual(tb.terminal_cwd(self.term), self.work)

    def screen_text(self):
        return self.term.get_text_format(tb.Vte.Format.TEXT) or ""

    def cd_back(self):
        self.term.feed_child(f"cd {shlex.quote(self.work)}\n".encode())
        pump(1.5, lambda: tb.terminal_cwd(self.term) == self.work)

    def click(self, text, word=None, ctrl=True, button=1):
        """Print `text` (single-spaced) on a fresh line and Ctrl+click on `word` with real x/y coordinates."""
        self.term.feed(f"\r\n{text}".encode())
        pump(0.3)
        word = word or text.split(" ")[0]
        col = text.index(word)
        row = next((r for r in range(self.term.get_row_count())
                    if self.term.match_check(col, r)[0] == text), None)
        self.assertIsNotNone(row, f"{text!r} not on screen ({self.term.get_column_count()}x{self.term.get_row_count()}): {self.screen_text()!r}")
        pad = self.term.get_style_context().get_padding(Gtk.StateFlags.NORMAL)
        ev = type("Ev", (), {
            "button": button, "state": Gdk.ModifierType.CONTROL_MASK if ctrl else 0,
            "x": pad.left + (col + 0.5) * self.term.get_char_width(),
            "y": pad.top + (row + 0.5) * self.term.get_char_height()})()
        handled = self.app.term_click(self.term, ev)
        pump(1.0)
        return handled

    def test_ctrl_click_folder_changes_directory_in_same_tab(self):
        tabs = self.app.nb.get_n_pages()
        self.assertTrue(self.click("proj"))
        self.assertTrue(pump(2, lambda: tb.terminal_cwd(self.term) == self.work + "/proj"))
        self.assertEqual(self.app.nb.get_n_pages(), tabs)
        # `ll` ran in the new directory: its listing replaces the stale one
        self.assertTrue(pump(3, lambda: "inside-marker.txt" in self.screen_text()))
        self.cd_back()

    def test_ctrl_click_folder_with_space_as_ls_prints_it(self):
        self.assertTrue(self.click("'proj dir'", "dir"))  # `ls` quotes names with spaces
        self.assertTrue(pump(2, lambda: tb.terminal_cwd(self.term) == self.work + "/proj dir"))
        self.cd_back()

    def test_ctrl_click_file_with_space(self):
        self.assertTrue(self.click("'my notes.txt'", "notes.txt"))
        self.assertEqual(self.app.opened, [self.work + "/my notes.txt"])

    def test_ctrl_click_jpg_opens_with_its_handler(self):
        self.assertTrue(self.click("pic.jpg"))
        self.assertEqual(self.app.opened, [self.work + "/pic.jpg"])

    def test_ctrl_click_text_file_opens_editor(self):
        self.assertTrue(self.click("notes.txt"))
        self.assertEqual(self.app.opened, [self.work + "/notes.txt"])

    def test_file_without_handler_ignored(self):
        real, tb.handler_for = tb.handler_for, lambda _path: None
        try:
            self.assertFalse(tb.App.open_file(self.app, self.work + "/blob.bin"))
        finally:
            tb.handler_for = real

    def test_missing_path_not_handled(self):
        self.assertFalse(self.click("ghost.txt"))
        self.assertEqual(self.app.opened, [])

    def test_plain_click_not_handled(self):
        self.assertFalse(self.click("notes.txt", ctrl=False))
        self.assertEqual(self.app.opened, [])

    def test_setting_off_disables(self):
        self.app.settings["ctrl_click_open"] = False
        self.assertFalse(self.click("notes.txt"))
        self.assertEqual(self.app.opened, [])

    def test_folder_ignored_while_program_runs(self):
        self.term.feed_child(b"sleep 30\n")
        self.assertTrue(pump(3, lambda: not tb.shell_in_foreground(self.term)))
        self.assertTrue(self.app.open_path(self.term, self.work + "/proj"))  # consumed, nothing typed
        pump(1)
        self.assertEqual(tb.terminal_cwd(self.term), self.work)
        self.assertNotIn("inside-marker.txt", self.screen_text())  # no `ll` typed into the program
        self.term.feed_child(b"\x03")
        self.assertTrue(pump(3, lambda: tb.shell_in_foreground(self.term)))

    def test_shell_in_foreground_at_prompt(self):
        self.assertTrue(tb.shell_in_foreground(self.term))


if __name__ == "__main__":
    unittest.main()
