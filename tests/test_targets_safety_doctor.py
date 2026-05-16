from pathlib import Path

from omarchy_theme_targets.colors import load_colors
from omarchy_theme_targets.doctor import run_doctor
from omarchy_theme_targets.palette import derive_palette
from omarchy_theme_targets.safety import (
    HEADER_PREFIX,
    can_write_generated,
    has_generated_header,
    remove_generated,
    write_generated,
)
from omarchy_theme_targets.targets import load_targets, render_target


FIXTURE = Path(__file__).parent / "fixtures/osaka-jade/colors.toml"


def test_target_manifests_load():
    targets = load_targets()
    assert {target.id for target in targets} == {"btop", "darktable", "gtk", "obsidian"}
    assert {target.safety_class for target in targets} >= {"full-theme", "ui-theme", "color-critical"}


def test_render_target_uses_semantic_values():
    colors = load_colors(FIXTURE)
    target = next(target for target in load_targets() if target.id == "obsidian")
    body = render_target(target, derive_palette(colors), colors.colors)
    assert "--interactive-accent: #7fbf9f;" in body
    assert "--background-primary: #101615;" in body


def test_generated_file_safety(tmp_path):
    target = tmp_path / "theme.css"
    status, message = write_generated(target, "body {}\n")
    assert status == "applied", message
    assert has_generated_header(target)
    assert target.read_text(encoding="utf-8").startswith(HEADER_PREFIX)

    manual = tmp_path / "manual.css"
    manual.write_text("body {}\n", encoding="utf-8")
    allowed, reason = can_write_generated(manual)
    assert not allowed
    assert "refusing to overwrite" in reason


def test_directory_output_is_error(tmp_path):
    output_dir = tmp_path / "theme.css"
    output_dir.mkdir()

    allowed, reason = can_write_generated(output_dir)
    assert not allowed
    assert "output path is a directory" in reason

    status, message = write_generated(output_dir, "body {}\n")
    assert status == "error"
    assert "output path is a directory" in message

    status, message = remove_generated(output_dir)
    assert status == "error"
    assert "output path is a directory" in message


def test_doctor_reports_invalid_colors(tmp_path):
    path = tmp_path / "colors.toml"
    path.write_text('accent = "#ffffff"\n', encoding="utf-8")
    checks = run_doctor(load_colors(path))
    assert any(row["status"] == "error" and "missing keys" in row["message"] for row in checks)
