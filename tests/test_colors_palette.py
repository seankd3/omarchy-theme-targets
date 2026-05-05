from pathlib import Path

from omarchy_theme_targets.colors import load_colors
from omarchy_theme_targets.palette import derive_palette


FIXTURE = Path(__file__).parent / "fixtures/osaka-jade/colors.toml"


def test_load_colors_fixture():
    result = load_colors(FIXTURE)
    assert result.ok
    assert result.colors["accent"] == "#7fbf9f"
    assert result.colors["color15"] == "#f2fff8"


def test_load_colors_rejects_bad_hex(tmp_path):
    path = tmp_path / "colors.toml"
    path.write_text(FIXTURE.read_text().replace("#7fbf9f", "jade"), encoding="utf-8")
    result = load_colors(path)
    assert not result.ok
    assert any("accent is not a #RRGGBB color" in error for error in result.errors)


def test_derive_semantic_palette_roles():
    palette = derive_palette(load_colors(FIXTURE))
    assert palette["surface.base"] == "#101615"
    assert palette["accent.primary"] == "#7fbf9f"
    assert palette["danger"] == "#e67e80"
    assert set(palette) == {
        "surface.base",
        "surface.panel",
        "surface.raised",
        "text.primary",
        "text.muted",
        "accent.primary",
        "accent.hover",
        "selection.bg",
        "selection.fg",
        "border.subtle",
        "danger",
        "warning",
        "success",
        "info",
        "focus.ring",
    }
