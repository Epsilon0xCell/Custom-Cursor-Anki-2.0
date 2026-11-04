<p align="center"><img src="banner.png" alt="Custom-Cursor-Anki-2.0 banner" width="800"></p>

<p align="center"><img src="logo.png" alt="Custom-Cursor-Anki-2.0 logo" width="200"></p>

# Custom-Cursor-Anki-2.0

**The Infrared Garden**

In a surreal night garden shot like infrared film, flashcards are planted like seedlings and a giant mouse pointer stands over them like a sundial.

An Anki add-on that lets you set a custom mouse cursor inside Anki.

<p align="center"><img src="intro-banner.png" alt="Custom-Cursor-Anki-2.0 introduction" width="800"></p>

![Animated scene: The Infrared Garden](assets-scene.svg)

![Separator](sep-heavy.svg)

## Install

Copy this folder into Anki's add-ons folder, then restart Anki. A `Custom Cursor` entry appears in the Tools menu (shortcut from `config.json`, default `Ctrl+Shift+C`). Open it, browse to an image file, press Apply Cursor, or press Reset Cursor to restore the normal cursor.

![Separator](sep-heavy.svg)

## How it works

- `__init__.py` adds the Tools menu entry and owns the cursor state. `set_cursor` now refuses a path that does not exist instead of installing a broken cursor, and returns true only when the cursor was set. If `config.json` sets `auto_apply` to true and `default_cursor` to an existing file, that cursor is applied at start-up.
- `cursor_dialog.py` is the settings dialog: pick a file, apply it, or reset it. Reset also clears the file field.
- `config.json` holds `default_cursor`, `auto_apply`, and `shortcut`. The shortcut and the start-up behaviour above are now actually read from this file; before this pass they were ignored and the shortcut was always hardcoded.
- `manifest.json` names the add-on, its version, and its supported Anki range. Its homepage and author previously shipped as template placeholders (`yourusername`, `Your Name`); both now point at this repo and account.

![Separator](sep-heavy.svg)

## Verified behaviour and limits

Verified with a stub `aqt` harness (real Anki was not available here): the Tools menu entry is created with the configured shortcut, applying a nonexistent path now leaves the cursor unchanged, applying a valid path sets it, reset restores it, and the dialog's empty-path apply shows an information message instead of crashing. The add-on requires Anki (`aqt`) and was not run inside real Anki in this pass. Image files are loaded with `QPixmap`, so `.cur` and `.ani` files listed in the browse filter may not load on every platform; PNG, XPM, and JPG are the safe choices.

Files: `__init__.py`, `cursor_dialog.py`, `config.json`, `manifest.json`, `logo.png`, `banner.png`.

![Separator](sep-heavy.svg)

> **Note:** Please select a valid cursor file. That file could not be loaded as a cursor image. A file can exist and still not load.
