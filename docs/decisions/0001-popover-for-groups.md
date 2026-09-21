# 0001 — Popover instead of ComboBox for button groups
Status: accepted (2026-09)
Context: the group `ComboBoxText` drop-down sometimes did not show every option (popup toplevel clipping).
Decision: `Gtk.MenuButton` + scrollable `Gtk.Popover` with `ModelButton` items.
Rationale: popover lives inside the app window's layout, scrolls, works with 25+ groups.
Alternatives: Gtk.Menu (same toplevel-popup class of issues), custom dialog (heavier).
