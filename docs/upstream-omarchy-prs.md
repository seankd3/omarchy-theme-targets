# Likely Upstream Omarchy PRs

The useful upstream primitive is tiny: support a hook directory that runs after a
theme is set.

Suggested behavior:

- Add `~/.config/omarchy/hooks/theme-set.d/*.sh`.
- Execute readable executable scripts in sorted order after Omarchy renders its
  own templates.
- Pass through the active theme environment if Omarchy already has one.
- Document that hooks should be fast, user-owned, and failure-contained.

This repo does not need an upstream color schema rewrite. Existing Omarchy
themes already expose enough primitive colors in `colors.toml` for external
tools to derive semantic roles:

- `surface.base`
- `surface.panel`
- `surface.raised`
- `text.primary`
- `text.muted`
- `accent.primary`
- `accent.hover`
- `selection.bg`
- `selection.fg`
- `border.subtle`
- `danger`
- `warning`
- `success`
- `info`
- `focus.ring`

Theme authors can keep writing simple Omarchy themes. Adapter authors and bots
can consume a richer semantic palette externally.
