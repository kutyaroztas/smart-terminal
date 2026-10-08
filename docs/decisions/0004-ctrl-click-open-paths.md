# 0004 — Ctrl+click opens folders and text files

Status: accepted (2026-10-08)

## Context
Wanted: click a folder name in terminal output to enter it, click a text file to open it in the editor.

## Decision
- **Ctrl+click**, not plain click: plain left click/drag is selection (and `copy_on_select`).
- Folder → type `cd <quoted path> && ll` (owner request: the old listing stays on screen and confuses) into the **same tab's shell** (owner's choice over opening a new tab),
  but only when the shell owns the foreground process group (`os.tcgetpgrp`); otherwise do nothing so
  `vim`/`ssh`/`python` never receive the text.
- Text file (no NUL in first 4 KiB) → default app for `text/plain`; any other file → default app for its guessed content type (`Gio.content_type_guess`); nothing happens if none is registered.
- Match regex (`PATH_PATTERN`) = words joined by single spaces; `path_at` takes the clicked word plus neighbours and picks the longest candidate that exists (handles `ls` quotes and spaces); resolved against the shell cwd and must exist, which removes
  false positives. Setting `ctrl_click_open` (default on).

## Consequences
- Names with spaces work, but a name followed by a single space and another existing name can resolve to the longer combined path only if that exists (longest wins).
- Relative names break if the shell changed directory since they were printed.
- A half-typed prompt line gets the `cd` appended.
- `ll` is not a real command: it relies on the user's shell alias (Ubuntu default `ls -alF`); without it `cd` still succeeds and `ll` reports not found.
