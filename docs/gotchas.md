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
- **Personal config in repo** → `config/` is git-ignored; never `git add -f` it.
