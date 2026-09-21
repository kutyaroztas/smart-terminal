# 0003 — Single Python file, system GTK only
Status: accepted (2026-09)
Decision: keep everything in `terminal_buttons.py`; depend only on distro packages
(python3-gi, gir1.2-vte-2.91). No pip, no build step, config in JSON next to the app.
Rationale: trivial install/run, easy for any agent to read whole. Revisit if the file grows far beyond ~2000 lines.
