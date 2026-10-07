# HANDOFF — current state

Updated: 2026-10-07. Tab icon background orange → blue (`assets/tab-icon.svg`). Before: 2026-10-03. Added tray (minimize/close to tray) + autostart settings (branch `feat/tray-autostart`). Earlier: 2026-09-30. Repo, local folder and main script renamed to `smart-terminal` / `smart_terminal.py` (branch `chore/rename-smart-terminal`); `main` is the source of truth after merge.

## State
Smart Terminal v1.0 works; all features in `docs/CHANGELOG.md` shipped and pushed to
https://github.com/kutyaroztas/smart-terminal. Owner: Kutyar (writes Turkish, wants Turkish replies in chat).

## Next step
Nothing mandatory pending. Candidate follow-ups (ask the owner before starting):
1. Manually verify the gaps listed in `docs/testing.md`.
2. Reproduce/confirm the original combo-box drop-down bug's root cause (never reproduced; popover replaced it).
3. Consider adding an automated smoke test (scripted App run) under `tests/`.

## Known issues / unverified
- Tray/autostart: real minimize button + real login autostart not tested by hand (only scripted: hide/show/toggle, autostart file). No single-instance guard: starting a second copy while one is in the tray opens another window/tray icon.
- Real-mouse interactions and file choosers untested by hand.
- Icon (`terminal-buttons.svg`), app-id (`set_prgname`) and desktop file name intentionally keep the old name `terminal-buttons` (window matching / installed icon).
- Only the desktop entry `~/.local/share/applications/terminal-buttons.desktop` (outside repo) carries `Name=Smart Terminal`.

## Open work (PR 3 review nits, triaged)
- If the tray library is installed but no tray host runs (GNOME AppIndicator extension off), "close to tray"/`--minimized` hide the window with no way back: check `org.kde.StatusNotifierWatcher` owner on D-Bus, else treat `indicator` as `None`.
- `set_autostart`: also escape `\`, `%`, `$`, backtick in `Exec`; catch `OSError` and revert the checkbox.
- Single-instance guard (Gio/Gtk.Application) + ADR.
- Tray "Quit" could use `self.destroy()` instead of `Gtk.main_quit()` (consistency).

## Pending owner decisions
None.
