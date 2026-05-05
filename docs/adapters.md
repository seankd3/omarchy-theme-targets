# Adapter Safety Classes

Adapters should be small enough that a person or bot can inspect them quickly.
They should prefer generated artifacts over direct mutation of app-owned config.

## full-theme

The app has a supported theme file format and can load a complete theme without
touching unrelated settings.

MVP example: `btop`.

## ui-theme

The adapter styles application chrome or UI variables. It should avoid editing
project, document, vault, workspace, or profile content unless the user
explicitly opts in.

MVP examples: `gtk`, `obsidian`.

## color-critical

The app displays work where color neutrality matters. The adapter must avoid
surfaces that can affect image, video, canvas, preview, histogram, or calibrated
content. Style chrome only.

MVP example: `darktable`.

## fragile-brand

The app has unsupported internals, frequently changing selectors, branding
constraints, or fragile injection paths. These are out of scope for the MVP.

Examples intentionally not included here: Discord and Spotify.
