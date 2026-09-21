# AGENTS.md — Smart Terminal (repo: terminal-buttons)

Vendor-neutral entry point for any coding agent (Claude Code, Codex, Antigravity/Gemini, Cursor, Aider…).
**Read `docs/HANDOFF.md` first** — it says where the last session stopped and what to do next.

## What this is
Smart Terminal v1.0: a SecureCRT/WindTerm-style tabbed terminal for Linux (GTK3 + VTE) with a bar of
configurable command buttons, split panes, themes, 5 UI languages. Single Python file, no build step.

## Run / check
```bash
python3 terminal_buttons.py                    # run the app (needs python3-gi, gir1.2-vte-2.91, gir1.2-gtk-3.0)
python3 -m py_compile terminal_buttons.py      # syntax check
```
There is no automated test suite; UI is verified with scripted GTK runs + screenshots →
`docs/testing.md`.

## Repo map
| Path | Purpose |
|---|---|
| `terminal_buttons.py` | the whole app (~1500 lines); module map in `docs/architecture.md` |
| `config/` | per-user `buttons.json` / `settings.json` — **personal, git-ignored, never commit** |
| `assets/tab-icon.svg`, `terminal-buttons.svg` | tab icon, app icon |
| `docs/` | architecture, gotchas, testing, ADRs, HANDOFF, CHANGELOG |
| `README.md` | end-user documentation (install/usage) — not developer notes |

## Conventions
- Python 3.12, PyGObject (Gtk 3.24, Gdk 3.0, Vte 2.91, Pango, GLib, GdkPixbuf). No third-party pip deps.
- Keep it one file unless a split is agreed (see `docs/decisions/`). Match existing style: short
  docstrings, few comments, GTK idioms.
- All user-visible text goes through `STRINGS` (5 languages: en, de, fr, tr, ru) — add every key to all.
- New settings: add to `DEFAULT_SETTINGS`, validate in `normalize_settings`, document in README.
- Shortcuts: `DEFAULT_SHORTCUTS` + `App.perform` action + `STRINGS` label.

## Rules
- Never commit `config/`, tokens, or personal data.
- Never push to `main` without a passing docs check (below); prefer a branch + PR.
- Test UI changes with a real scripted run (screenshot), not just `py_compile`.

## Documentation contract (checked before every push to main and every PR merge)
| If you change… | Update |
|---|---|
| a class/function/file layout | `docs/architecture.md`, repo map above |
| you hit a trap / root cause | `docs/gotchas.md` |
| test method | `docs/testing.md` |
| a significant design decision | new `docs/decisions/NNNN-*.md` |
| user-visible behaviour | `README.md`, `docs/CHANGELOG.md` |
| anything, every push/merge | `docs/HANDOFF.md` (state + next step) |
Put one line in the commit/PR body: `Docs: up to date (…)` or `Docs: no change needed (…)`.
General rules live in the owner's `~/.claude/reference/agentic-development-rules.md`
(summary above is the repo-local copy so non-Claude agents follow it too).
