"""Claude Code status line for stockpile."""
import json
import os
import subprocess
import sys
from pathlib import Path

COLOR = "\033[38;2;6;182;212m"  # cyan-500
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
LABEL = "stockpile"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    cwd = data.get("cwd") or os.getcwd()
    model = (data.get("model") or {}).get("display_name") or "?"
    project_dir = (data.get("workspace") or {}).get("project_dir") or cwd
    output_style = (data.get("output_style") or {}).get("name") or "default"
    cost = (data.get("cost") or {}).get("total_cost_usd")

    try:
        rel = Path(cwd).relative_to(project_dir).as_posix() or "."
    except (ValueError, TypeError):
        rel = cwd

    branch = "?"
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=cwd, stderr=subprocess.DEVNULL, text=True, timeout=2,
        )
        branch = out.strip() or "?"
    except Exception:
        pass

    parts = [
        f"{BOLD}{COLOR}[{LABEL}]{RESET}",
        f"{DIM}({branch}){RESET}",
        model,
        f"{DIM}{rel}{RESET}",
    ]
    if output_style and output_style != "default":
        parts.append(f"{DIM}<{output_style}>{RESET}")
    if cost is not None:
        parts.append(f"{DIM}${cost:.3f}{RESET}")

    sys.stdout.write(" | ".join(parts))


if __name__ == "__main__":
    main()
