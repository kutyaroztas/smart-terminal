# Architecture

Single module `smart_terminal.py`. Symbols below are stable anchors — grep for them
(line numbers drift).

## Constants and data
- Paths: `APP_DIR`, `CONFIG_DIR`, `BUTTONS_FILE`, `SETTINGS_FILE`, icon files. Tests redirect
  `SETTINGS_FILE`/`BUTTONS_FILE` to temp files.
- `APP_NAME`, `APP_VERSION` — window title and About strings derive from these.
- `DEFAULT_BUTTONS`: `{label, cmd, enter, group, color}`; `cmd` uses escapes decoded by `decode()`
  (`\n \t \e \r \\`, `\xNN`). `enter=False` sends raw (Ctrl+C is `\x03`).
- `DEFAULT_SHORTCUTS`, `DEFAULT_SETTINGS`, `THEMES`, `LIGHT_PALETTE`, `TANGO_PALETTE`,
  `LANGS`, `STRINGS` (en/de/fr/tr/ru).
- Persistence helpers: `read_json`, `write_json`, `load_buttons` (migrates old group names),
  `load_settings` → `normalize_settings` (merge over defaults + validate), `ordered_groups`.

## Widget tree
```
App (Gtk.Window)
 ├─ toolbar / button bar (group MenuButton+Popover, flow of make_button() buttons)
 └─ Notebook (self.nb)  — one tab per Page
     └─ Page (Gtk.Box)  .root() → pane tree
         ├─ search bar (build_search_bar)
         └─ pane tree: Gtk.Paned splits → Pane leaves
             Pane (Gtk.Box) = header EventBox (penguin icon, title, close button; shown only
             when the tab has >1 pane) + body Box (Vte.Terminal + Gtk.Scrollbar)
```
Helpers: `pane_unit(term)` (terminal → its Pane), `is_open(term)`, `terminals(widget)`,
`first_terminal(widget)`, `replace_child(parent, old, new)`, `accel_label`.

## App responsibilities (grouped)
- **Setup/theme/lang:** `__init__`, `apply_language`, `apply_theme` (CSS provider, `.tb-root`,
  `.tb-panehead`, `.tb-tabclose`), `style_terminal`, `restyle_terminals`, `tr`.
- **Tray/autostart:** `build_indicator`, `update_tray`, `toggle_window/show_window`, `on_delete`,
  `on_window_state` (minimize → hide), `autostart_enabled/set_autostart`; `AppIndicator` is `None` when
  the library is missing (tray options are then disabled). CLI flag `--minimized` (see `main`).
- **Tabs:** `new_tab`, `clone_tab`, `close_page`, `tab_icon`, `tab_enter/leave/hover_switch`
  (hover-to-activate), `tab_click` (middle/right), `strip_click` (double-click empty strip → new tab),
  `rename_tab`, `update_title`, `page_of`, `current`.
- **Panes:** `split`, `make_pane`, `refresh_headers`, `close_pane`, `focused_terminal`,
  `on_terminal_focus`.
- **Terminal:** `new_terminal`, `on_terminal_title`, `term_click/term_release`,
  `show_terminal_menu`, `paste`, `paste_text`, `confirm_paste` (multi-line warning).
- **Shortcuts:** `match_shortcut`, `handle_shortcut`, `perform(action)`, `on_key`.
- **Search:** `build_search_bar`, `open_search`, `run_search`, `find`, `close_search`.
- **Button bar:** `rebuild_buttons`, `select_group`, `fill_buttons`, `make_button`,
  `button_click`, `send`.
- **Dialogs:** `build_edit_dialog`/`edit_dialog` (buttons editor + `order_dialog` group order),
  `build_settings_dialog` with `build_general_page`, `build_shortcuts_page`,
  `capture_shortcut`, `export_settings`/`import_settings`/`json_chooser`, `set_setting`.
- `main()` — entry point.

## Extension points
- **New shortcut action:** key in `DEFAULT_SHORTCUTS`, branch in `perform`, label in `STRINGS`.
- **New setting:** `DEFAULT_SETTINGS` + `normalize_settings` + UI in `build_general_page` + README.
- **New theme:** entry in `THEMES`; add its name string if shown in the UI.
- **New language:** add to `LANGS` and every `STRINGS` entry.
