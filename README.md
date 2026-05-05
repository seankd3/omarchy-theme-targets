# Omarchy Theme Targets

Machine-readable app theme targets for Omarchy.

Omarchy Theme Targets makes every app feel like it belongs to the active Omarchy
desktop theme, safely and reversibly. Theme once. Everything belongs. Nothing
gets mangled. Bots can inspect and repair it.

This MVP is intentionally small: it reads the active Omarchy `colors.toml`,
derives a semantic palette, and generates safe target artifacts for practical app
surfaces.

## Install

From this repo:

```bash
python -m pip install .
omarchy-theme-targets list
```

During development:

```bash
PYTHONPATH=src python -m omarchy_theme_targets.cli palette --colors tests/fixtures/osaka-jade/colors.toml --json
```

## Commands

```bash
omarchy-theme-targets palette --json
omarchy-theme-targets list --json
omarchy-theme-targets status
omarchy-theme-targets doctor
omarchy-theme-targets apply
omarchy-theme-targets rollback
omarchy-theme-targets install-hook
```

Use `--colors /path/to/colors.toml` to inspect or test another theme. `apply`,
`rollback`, and `install-hook` also support `--dry-run`.

## MVP Targets

- `btop`: full theme at `~/.config/btop/themes/omarchy.theme`.
- `darktable`: chrome-focused CSS artifact under
  `~/.config/omarchy-theme-targets/darktable/omarchy.css`; it avoids
  image/canvas surfaces.
- `obsidian`: local CSS artifact under
  `~/.config/omarchy-theme-targets/obsidian/omarchy.css`; it does not rewrite
  vaults.
- `gtk`: CSS artifact under `~/.config/omarchy-theme-targets/gtk/gtk.css`; it
  is not linked into user GTK config by default.

## Safety Model

The tool never overwrites an existing user-owned config file unless it starts
with the Omarchy Theme Targets generated header. Generated files can be removed
with `rollback`; manual files are reported as `manual` and left alone.

Bot-friendly commands support `--json` where useful. Stable status values are:
`applied`, `skipped`, `warning`, `error`, and `manual`.

## Verification

```bash
scripts/check.sh
```

See:

- [docs/theme-targets.md](docs/theme-targets.md)
- [docs/adapters.md](docs/adapters.md)
- [docs/upstream-omarchy-prs.md](docs/upstream-omarchy-prs.md)
