"""`vqe-bench` CLI entry point."""

from __future__ import annotations

import argparse
import sys

from vqe_bench.runner import run_from_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vqe-bench", description="VQE Benchmark Suite")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run an experiment from a YAML config")
    run_parser.add_argument("--config", required=True, type=str, help="Path to YAML config")

    args = parser.parse_args(argv)
    if args.command == "run":
        try:
            run_from_config(args.config)
        except Exception as exc:  # noqa: BLE001
            print(f"[vqe-bench] ERROR: {exc}", file=sys.stderr)
            return 1
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())