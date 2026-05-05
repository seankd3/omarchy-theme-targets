from __future__ import annotations

from pathlib import Path

from .safety import write_generated

HOOK_PATH = Path.home() / ".config/omarchy/hooks/theme-set.d/90-omarchy-theme-targets.sh"


def install_hook(dry_run: bool = False) -> dict[str, str]:
    body = """#!/usr/bin/env bash
set -euo pipefail

if command -v omarchy-theme-targets >/dev/null 2>&1; then
  omarchy-theme-targets apply
fi
"""
    status, message = write_generated(HOOK_PATH, body, dry_run=dry_run)
    if status == "applied" and not dry_run:
        HOOK_PATH.chmod(0o755)
    return {"target": "hook", "status": status, "output": str(HOOK_PATH), "message": message}
