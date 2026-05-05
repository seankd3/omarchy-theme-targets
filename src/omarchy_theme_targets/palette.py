from __future__ import annotations

from .colors import ColorsResult


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{max(0, min(255, channel)):02x}" for channel in rgb)


def _mix(a: str, b: str, weight: float) -> str:
    ar, ag, ab = _hex_to_rgb(a)
    br, bg, bb = _hex_to_rgb(b)
    return _rgb_to_hex((
        round(ar * (1 - weight) + br * weight),
        round(ag * (1 - weight) + bg * weight),
        round(ab * (1 - weight) + bb * weight),
    ))


def _luminance(value: str) -> float:
    r, g, b = [channel / 255 for channel in _hex_to_rgb(value)]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def derive_palette(result: ColorsResult) -> dict[str, str]:
    if not result.ok:
        raise ValueError("; ".join(result.errors))
    colors = result.colors
    bg = colors["background"]
    fg = colors["foreground"]
    accent = colors["accent"]
    dark_theme = _luminance(bg) < 0.5
    lift = "#ffffff" if dark_theme else "#000000"

    return {
        "surface.base": bg,
        "surface.panel": _mix(bg, lift, 0.07),
        "surface.raised": _mix(bg, lift, 0.12),
        "text.primary": fg,
        "text.muted": _mix(fg, bg, 0.36),
        "accent.primary": accent,
        "accent.hover": _mix(accent, "#ffffff" if dark_theme else "#000000", 0.16),
        "selection.bg": colors["selection_background"],
        "selection.fg": colors["selection_foreground"],
        "border.subtle": _mix(fg, bg, 0.72),
        "danger": colors.get("color1", "#ff5f57"),
        "warning": colors.get("color3", "#f5c542"),
        "success": colors.get("color2", "#63c174"),
        "info": colors.get("color4", "#58a6ff"),
        "focus.ring": colors["cursor"],
    }
