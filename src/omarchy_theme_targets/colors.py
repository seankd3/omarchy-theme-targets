from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_COLORS_PATH = Path.home() / ".config/omarchy/current/theme/colors.toml"
DEFAULT_THEME_DIR = Path.home() / ".config/omarchy/current/theme"
DEFAULT_THEME_NAME = Path.home() / ".config/omarchy/current/theme.name"

REQUIRED_KEYS = (
    "accent",
    "cursor",
    "foreground",
    "background",
    "selection_foreground",
    "selection_background",
    *(f"color{i}" for i in range(16)),
)

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


@dataclass(frozen=True)
class ColorsResult:
    path: Path
    colors: dict[str, str]
    warnings: list[str]
    errors: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_colors(path: Path | None = None) -> ColorsResult:
    colors_path = (path or DEFAULT_COLORS_PATH).expanduser()
    warnings: list[str] = []
    errors: list[str] = []
    raw: dict[str, Any] = {}

    if not colors_path.exists():
        return ColorsResult(colors_path, {}, warnings, [f"colors.toml not found: {colors_path}"])
    if not colors_path.is_file():
        return ColorsResult(colors_path, {}, warnings, [f"colors path is not a file: {colors_path}"])
    try:
        with colors_path.open("rb") as handle:
            raw = tomllib.load(handle)
    except OSError as exc:
        return ColorsResult(colors_path, {}, warnings, [f"colors.toml is unreadable: {exc}"])
    except tomllib.TOMLDecodeError as exc:
        return ColorsResult(colors_path, {}, warnings, [f"colors.toml is invalid TOML: {exc}"])

    colors: dict[str, str] = {}
    for key, value in raw.items():
        if isinstance(value, str):
            colors[key] = value.strip()

    missing = [key for key in REQUIRED_KEYS if key not in colors]
    if missing:
        errors.append(f"colors.toml missing keys: {', '.join(missing)}")

    for key in REQUIRED_KEYS:
        value = colors.get(key)
        if value is not None and not HEX_RE.match(value):
            errors.append(f"{key} is not a #RRGGBB color: {value}")

    extra = sorted(set(colors) - set(REQUIRED_KEYS))
    if extra:
        warnings.append(f"ignored non-standard color keys: {', '.join(extra)}")

    return ColorsResult(colors_path, colors, warnings, errors)


def read_theme_name() -> str | None:
    try:
        return DEFAULT_THEME_NAME.read_text(encoding="utf-8").strip() or None
    except OSError:
        return None
