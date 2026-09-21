# 0002 — `Pane` wrapper with per-pane header and scrollbar
Status: accepted (2026-09)
Context: WindTerm-like look: each split pane has its own header (penguin, title, close) and a
scrollbar; the notebook tab alone cannot represent several terminals.
Decision: `Pane` = header EventBox + body Box(Vte.Terminal + Gtk.Scrollbar bound to the terminal's
vadjustment). Headers are only shown when a tab has more than one pane (`refresh_headers`).
Consequence: never assume `term.get_parent()` is the pane — use `pane_unit(term)`.
Alternatives: Gtk.Notebook per pane (too heavy), overlay scrollbars (VTE has none built in).
