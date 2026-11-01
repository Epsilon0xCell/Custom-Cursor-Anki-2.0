![Introduction: a silent street before dawn, empties washed and waiting, one full bottle already delivered](intro-banner.png)

# Custom-Cursor-Anki-2.0

<!-- deco -->
> Milkman Float at the Silent Hour. Help has arrived before the house asked.
<!-- /deco -->

![Custom-Cursor-Anki-2.0](banner.png)

![Animated scene: the round crossing a terraced street](assets-scene.svg)


An Anki add-on that lets you set a custom mouse cursor inside Anki.

![Measuring tape separator](sep-heavy.svg)

<!-- deco -->
> Day book page, ledger ruling, red margin at the left, a small milk bottle beside this first heading only: INSTALL.
<!-- /deco -->

## Install

Copy this folder into Anki's add-ons folder, then restart Anki. A `Custom Cursor` entry appears in the Tools menu (shortcut from `config.json`, default `Ctrl+Shift+C`). Open it, browse to an image file, press Apply Cursor, or press Reset Cursor to restore the normal cursor.

![Measuring tape separator](sep-heavy.svg)

<!-- deco -->
> Day book page, ruled: HOW IT WORKS, in a clerk upright hand.
<!-- /deco -->

## How it works

- `__init__.py` adds the Tools menu entry and owns the cursor state. `set_cursor` now refuses a path that does not exist instead of installing a broken cursor, and returns true only when the cursor was set. If `config.json` sets `auto_apply` to true and `default_cursor` to an existing file, that cursor is applied at start-up.
- `cursor_dialog.py` is the settings dialog: pick a file, apply it, or reset it. Reset also clears the file field.
- `config.json` holds `default_cursor`, `auto_apply`, and `shortcut`. The shortcut and the start-up behaviour above are now actually read from this file; before this pass they were ignored and the shortcut was always hardcoded.
- `manifest.json` names the add-on, its version, and its supported Anki range. Its homepage and author previously shipped as template placeholders (`yourusername`, `Your Name`); both now point at this repo and account.

![Measuring tape separator](sep-heavy.svg)

<!-- deco -->
> Day book page, ruled: VERIFIED BEHAVIOUR AND LIMITS, in a clerk upright hand.
<!-- /deco -->

## Verified behaviour and limits

Verified with a stub `aqt` harness (real Anki was not available here): the Tools menu entry is created with the configured shortcut, applying a nonexistent path now leaves the cursor unchanged, applying a valid path sets it, reset restores it, and the dialog's empty-path apply shows an information message instead of crashing. The add-on requires Anki (`aqt`) and was not run inside real Anki in this pass. Image files are loaded with `QPixmap`, so `.cur` and `.ani` files listed in the browse filter may not load on every platform; PNG, XPM, and JPG are the safe choices.

Files: `__init__.py`, `cursor_dialog.py`, `config.json`, `manifest.json`, `logo.png`, `banner.png`.

<!-- deco -->
> **Note left under a bottle:** Please select a valid cursor file. That file could not be loaded as a cursor image. A file can exist and still not load.
<!-- /deco -->
