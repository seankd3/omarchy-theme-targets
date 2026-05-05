from __future__ import annotations

from pathlib import Path

from .colors import DEFAULT_THEME_DIR, ColorsResult
from .safety import can_write_generated
from .targets import load_targets


def run_doctor(colors: ColorsResult) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    if colors.ok:
        checks.append({"check": "colors", "status": "applied", "message": f"valid colors: {colors.path}"})
    else:
        for error in colors.errors:
            checks.append({"check": "colors", "status": "error", "message": error})
    for warning in colors.warnings:
        checks.append({"check": "colors", "status": "warning", "message": warning})

    theme_dir = DEFAULT_THEME_DIR
    if theme_dir.exists() and theme_dir.is_dir():
        try:
            next(theme_dir.iterdir(), None)
            checks.append({"check": "theme_path", "status": "applied", "message": f"readable theme path: {theme_dir}"})
        except OSError as exc:
            checks.append({"check": "theme_path", "status": "error", "message": f"unreadable theme path {theme_dir}: {exc}"})
    else:
        checks.append({"check": "theme_path", "status": "warning", "message": f"theme path not found: {theme_dir}"})

    for target in load_targets():
        allowed, reason = can_write_generated(target.output)
        checks.append({
            "check": "output",
            "target": target.id,
            "status": "applied" if allowed else "manual",
            "message": f"safe output: {target.output}" if allowed else f"{target.output}: {reason}",
        })
        parent = target.output.parent
        if parent.exists():
            try:
                owner = parent.stat().st_uid
                home_owner = Path.home().stat().st_uid
                if owner not in (home_owner, 0):
                    checks.append({
                        "check": "ownership",
                        "target": target.id,
                        "status": "error",
                        "message": f"unsafe output ownership: {parent}",
                    })
            except OSError as exc:
                checks.append({
                    "check": "ownership",
                    "target": target.id,
                    "status": "error",
                    "message": f"cannot inspect output ownership for {parent}: {exc}",
                })
    return checks
