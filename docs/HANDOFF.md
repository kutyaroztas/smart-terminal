# HANDOFF — current state

Updated: 2026-09-21. Docs added via PR #1 (`docs/agent-handoff` → `main`); `main` is the source of truth after merge.

## State
Smart Terminal v1.0 works; all features in `docs/CHANGELOG.md` shipped and pushed to
https://github.com/kutyaroztas/terminal-buttons. Owner: Kutyar (writes Turkish, wants Turkish replies in chat).

## Next step
Nothing mandatory pending. Candidate follow-ups (ask the owner before starting):
1. Manually verify the gaps listed in `docs/testing.md`.
2. Reproduce/confirm the original combo-box drop-down bug's root cause (never reproduced; popover replaced it).
3. Consider adding an automated smoke test (scripted App run) under `tests/`.

## Known issues / unverified
- Real-mouse interactions and file choosers untested by hand.
- Only the desktop entry `~/.local/share/applications/terminal-buttons.desktop` (outside repo) carries `Name=Smart Terminal`.

## Pending owner decisions
None.
