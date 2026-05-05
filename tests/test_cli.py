from pathlib import Path

from omarchy_theme_targets.cli import main


FIXTURE = Path(__file__).parent / "fixtures/osaka-jade/colors.toml"


def test_cli_scaffold_palette_json(capsys):
    assert main(["palette", "--colors", str(FIXTURE), "--json"]) == 0
    out = capsys.readouterr().out
    assert '"accent.primary": "#7fbf9f"' in out


def test_cli_list_json(capsys):
    assert main(["list", "--json"]) == 0
    out = capsys.readouterr().out
    assert '"id": "btop"' in out
