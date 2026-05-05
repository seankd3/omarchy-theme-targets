from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .colors import load_colors, read_theme_name
from .doctor import run_doctor
from .hooks import install_hook
from .palette import derive_palette
from .targets import apply_targets, list_targets, rollback_targets, target_statuses


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omarchy-theme-targets",
        description="Safely generate app theme artifacts from the active Omarchy theme.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--colors", type=Path, help="Override colors.toml path.")
    common.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", parents=[common])

    apply_parser = subparsers.add_parser("apply", parents=[common])
    apply_parser.add_argument("--dry-run", action="store_true", help="Preview writes without changing files.")

    subparsers.add_parser("doctor", parents=[common])

    rollback_parser = subparsers.add_parser("rollback", parents=[common])
    rollback_parser.add_argument("--dry-run", action="store_true", help="Preview removals without changing files.")

    hook_parser = subparsers.add_parser("install-hook", parents=[common])
    hook_parser.add_argument("--dry-run", action="store_true", help="Preview hook install without changing files.")

    subparsers.add_parser("list", parents=[common])
    subparsers.add_parser("palette", parents=[common])
    return parser


def _emit(payload, json_output: bool) -> None:
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    if isinstance(payload, list):
        for row in payload:
            target = row.get("target") or row.get("id") or row.get("check", "-")
            status = row.get("status") or row.get("safety_class", "-")
            message = row.get("message") or row.get("description") or row.get("output", "")
            print(f"{status:8} {target:12} {message}")
        return
    if isinstance(payload, dict):
        for key, value in payload.items():
            print(f"{key}: {value}")
        return
    print(payload)


def _load_palette(colors_path: Path | None) -> tuple[dict[str, str], dict[str, str], dict[str, object]]:
    colors = load_colors(colors_path)
    palette = derive_palette(colors)
    meta: dict[str, object] = {
        "theme_name": read_theme_name(),
        "colors_path": str(colors.path),
        "warnings": colors.warnings,
    }
    return palette, colors.colors, meta


def _exit_for_rows(rows: list[dict[str, str]]) -> int:
    if any(row.get("status") == "error" for row in rows):
        return 2
    if any(row.get("status") in {"warning", "manual"} for row in rows):
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            _emit(list_targets(), args.json)
            return 0
        if args.command == "status":
            _emit(target_statuses(), args.json)
            return 0
        if args.command == "rollback":
            rows = rollback_targets(dry_run=args.dry_run)
            _emit(rows, args.json)
            return _exit_for_rows(rows)
        if args.command == "install-hook":
            row = install_hook(dry_run=args.dry_run)
            _emit(row, args.json)
            return 2 if row["status"] == "error" else 1 if row["status"] in {"warning", "manual"} else 0

        colors = load_colors(args.colors)
        if args.command == "doctor":
            checks = run_doctor(colors)
            _emit(checks, args.json)
            return 2 if any(row["status"] == "error" for row in checks) else 1 if any(row["status"] == "warning" for row in checks) else 0
        if not colors.ok:
            _emit([{"status": "error", "target": "colors", "message": error} for error in colors.errors], args.json)
            return 2

        palette, raw_colors, meta = _load_palette(args.colors)
        if args.command == "palette":
            payload = {"palette": palette, **meta} if args.json else palette
            _emit(payload, args.json)
            return 0
        if args.command == "apply":
            rows = apply_targets(palette, raw_colors, dry_run=args.dry_run)
            _emit(rows, args.json)
            return _exit_for_rows(rows)
    except ValueError as exc:
        _emit([{"status": "error", "target": "palette", "message": str(exc)}], args.json)
        return 2
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
