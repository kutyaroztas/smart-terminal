# Changelog

## [Unreleased]
- Ctrl+click on a folder name in the terminal enters it in the same tab and lists it (`cd … && ll`, only at the shell prompt); on a file opens it in the default application for its type (text → default editor, jpg → image viewer, …). Names with spaces are supported. Setting `ctrl_click_open` (default on).
- Tests: `tests/test_ctrl_click.py` (unittest, scripted real `App` run).
- Mouse actions: new right-click action "paste" (always pastes the clipboard) and `middle_action` setting (paste / context menu / nothing) replacing the `middle_paste` checkbox (migrated automatically). Defaults unchanged.
- App (desktop) icon body recolored from purple to blue (`terminal-buttons.svg`).
- Tray icon (optional, AyatanaAppIndicator3): minimize to tray, close button hides to tray, show/hide + quit menu.
- "Start automatically at login" setting (XDG autostart entry, `--minimized`).
- Rename repo to `smart-terminal` and `terminal_buttons.py` to `smart_terminal.py`.
- Agent handoff docs (AGENTS.md, docs/).
Credits: Design: Claude Sonnet 5.5 (Claude Code) · Impl: Claude Sonnet 5.5 (Claude Code) · Test: Claude Sonnet 5.5 (Claude Code) · UAT: Kutyar
Credits: Impl: Claude Sonnet 5.5 (Claude Code; Ctrl+click: ?) · Review: pingpong-reviewer agent (mouse actions) · Test: Claude Sonnet 5.5 (Claude Code, Xvfb) · UAT: Kutyar

## 1.0 (2026-09)
- Rename to Smart Terminal v1.0.
- Scrollbar on every terminal.
- Split panes get their own header (penguin icon, title, close button).
- Group order setting (top group is selected on start).
- Double-click on the empty tab strip opens a new tab.
- Group selection via popover (scrollable) instead of combo box.
- Penguin icon on each tab; dark gray title bar in all themes.
- Initial release: tabs, split panes, command buttons with groups/colors, themes, 5 languages,
  configurable shortcuts, search, paste warning, settings import/export.

## [0.1.0] — 2026-09-19
### Added
- Geçmiş: kit öncesi çalışma
Credits: Design: Claude Sonnet 5.5 (Claude Code) · Review: Claude Opus (pingpong) · Impl: Claude Sonnet 5.5 (Claude Code) · UAT: Kutyar
