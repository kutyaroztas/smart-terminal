# Testing

No automated suite. Verify with a scripted run of the real `App`, drive it with `GLib.timeout_add`,
and screenshot the window.

## Template
```python
import sys, os, tempfile
sys.path.insert(0, "/path/to/smart-terminal")
import gi
gi.require_version("Gtk","3.0"); gi.require_version("Gdk","3.0"); gi.require_version("Vte","2.91")
from gi.repository import Gdk, GLib, Gtk
import smart_terminal as tb
T = tempfile.mkdtemp()
tb.SETTINGS_FILE = T + "/s.json"; tb.BUTTONS_FILE = T + "/b.json"   # never touch real config
a = tb.App(); a.show_all()
def shot(n):
    w = a.get_window()
    Gdk.pixbuf_get_from_window(w, 0, 0, w.get_width(), w.get_height()).savev(f"{T}/{n}.png", "png", [], [])
def step():
    a.split(a.focused_terminal(), Gtk.Orientation.HORIZONTAL)
def done():
    shot("after"); print("ok", flush=True); os._exit(0)
GLib.timeout_add(2500, lambda: (step(), False)[1])
GLib.timeout_add(4000, lambda: (done(), False)[1])
Gtk.main()
```
View the PNG to check layout. Needs a display (Wayland/X11 session).

## Covered by scripted runs so far
group popover (4 and 25 groups), rename, strip double-click, group order + persistence, split-pane
headers incl. nested splits and closing via header X, scrollbars.

## NOT verified by hand (known gaps)
real mouse drags (scrollbar), physical double-click timing, file chooser dialogs (import/export),
title readback after rename, all non-English UI strings visually.
