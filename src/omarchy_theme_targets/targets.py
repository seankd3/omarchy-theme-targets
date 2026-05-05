from __future__ import annotations

import importlib.resources as resources
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .safety import classify_path, remove_generated, write_generated


ARTIFACT_ROOT = Path.home() / ".config/omarchy-theme-targets"


@dataclass(frozen=True)
class Target:
    id: str
    name: str
    safety_class: str
    description: str
    output: Path
    template: str


def _target_root():
    return resources.files("omarchy_theme_targets").joinpath("targets")


def load_targets() -> list[Target]:
    targets: list[Target] = []
    for child in sorted(_target_root().iterdir(), key=lambda item: item.name):
        manifest_path = child.joinpath("manifest.toml")
        if not manifest_path.is_file():
            continue
        manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
        raw_output = manifest["output"].replace("{home}", str(Path.home()))
        raw_output = raw_output.replace("{artifact_root}", str(ARTIFACT_ROOT))
        targets.append(Target(
            id=manifest["id"],
            name=manifest["name"],
            safety_class=manifest["safety_class"],
            description=manifest["description"],
            output=Path(raw_output),
            template=child.joinpath("templates", manifest["template"]).read_text(encoding="utf-8"),
        ))
    return targets


def render_target(target: Target, palette: dict[str, str], colors: dict[str, str]) -> str:
    values = {key.replace(".", "_"): value for key, value in palette.items()}
    values.update(colors)
    return target.template.format(**values)


def list_targets() -> list[dict[str, str]]:
    return [
        {
            "id": target.id,
            "name": target.name,
            "safety_class": target.safety_class,
            "output": str(target.output),
            "description": target.description,
        }
        for target in load_targets()
    ]


def target_statuses() -> list[dict[str, str]]:
    rows = []
    for target in load_targets():
        state = classify_path(target.output)
        message = {
            "missing": "not generated",
            "applied": "generated file present",
            "manual": "manual file present; apply will skip",
            "error": "output path is a directory",
        }.get(state, state)
        rows.append({
            "target": target.id,
            "status": "skipped" if state == "missing" else state,
            "output": str(target.output),
            "safety_class": target.safety_class,
            "message": message,
        })
    return rows


def apply_targets(palette: dict[str, str], colors: dict[str, str], dry_run: bool = False) -> list[dict[str, str]]:
    rows = []
    for target in load_targets():
        body = render_target(target, palette, colors)
        status, message = write_generated(target.output, body, dry_run=dry_run)
        rows.append({"target": target.id, "status": status, "output": str(target.output), "message": message})
    return rows


def rollback_targets(dry_run: bool = False) -> list[dict[str, str]]:
    rows = []
    for target in load_targets():
        status, message = remove_generated(target.output, dry_run=dry_run)
        rows.append({"target": target.id, "status": status, "output": str(target.output), "message": message})
    return rows
