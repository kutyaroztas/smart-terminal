# Gotchas (symptom → cause → fix)

- **Group drop-down sometimes missed options** → `Gtk.ComboBoxText` popup is a separate toplevel that can
  be clipped by the screen/window. Cause not reproduced exactly. Fix: `Gtk.MenuButton` + scrollable
  `Gtk.Popover` of `ModelButton`s (ADR 0001).
- **Pane header shows only an orange line** → header uses `no_show_all=True`; `show_all()` on a
  parent then skips its children. Call `pane.box.show_all()` explicitly (see `refresh_headers`).
- **Hit-testing on the tab strip is off** → child allocations are in window coordinates, not
  notebook-relative. Use `widget.translate_coordinates(nb, 0, 0)` (see `strip_click`).
- **Tests: `Gdk.Event.button` returns a struct** → pass a plain object with `type/x/y/button`.
- **Tests: hang after popup screenshot** → exit with `os._exit(0)`; `os._exit` drops buffered stdout,
  so `print(..., flush=True)` first.
- **Tests: after Pane wrapping `term.get_parent()` is the body Box** → use `tb.pane_unit(term)`.
- **Dialog button lookup** → `get_children()[-1]` is the dialog's ButtonBox; search recursively by label.
- **Tray: `AppIndicator3` import fails** → Ubuntu 24.04+ ships only `AyatanaAppIndicator3` (`gir1.2-ayatanaappindicator3-0.1`); import is optional, tray features degrade to off.
- **Tests: `iconify()` never fires ICONIFIED in the sandbox session** → test `on_window_state` with a fake event (`changed_mask/new_window_state`).
- **Ctrl+click: `cd` typed into a running program** → `feed_child` writes to whatever owns the pty. Fix:
  `shell_in_foreground` compares `os.tcgetpgrp(pty fd)` with the shell pid; otherwise nothing is typed.
  A half-typed prompt line is still corrupted by the `cd` (not detectable).
- **Ctrl+click: relative name resolves wrong** → the shell's cwd may differ from where the name was
  printed; `get_current_directory_uri` is only set when the shell sends OSC 7, else `/proc/<pid>/cwd`.
- **Tests: `match_check_event` returns None for synthetic events** (Wayland cannot simulate pointer
  events; `Gdk.test_simulate_button` is a no-op) → stub it with `term.match_check(col, row)`.
  `match_check` rows are viewport rows and can differ from `get_text_range` rows: find the row by scanning
  `match_check`. `term.get_text_range_format(Vte.Format.TEXT, …)[0]` reads text.
- **Personal config in repo** → `config/` is git-ignored; never `git add -f` it.

- **Ctrl+click tests flake on the real (Wayland) display** → run them under `GDK_BACKEND=x11 xvfb-run -a`; there 3/3 full runs pass. Synthetic clicks are not possible on Wayland (`match_check_event` returns None), so tests drive `term_click` with real x/y and `match_check` instead.
