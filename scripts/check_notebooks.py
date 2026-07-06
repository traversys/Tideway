#!/usr/bin/env python3
"""Check notebooks for Dismal-era architecture patterns."""

from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_ROOT = ROOT / "notebooks"

RULES = {
    "core import": re.compile(r"\bfrom core\b|\bimport core\b"),
    "Dismal XML": re.compile(r"dismal_queries\.xml|DisMAL"),
    "direct requests session": re.compile(r"requests\.Session\("),
}

# Custom notebooks still scheduled for a focused analysis pass.
ALLOWLIST = {
    Path("notebooks/health/device_analysis.ipynb"),
    Path("notebooks/deep_dive/app_model_explore.ipynb"),
}


def notebook_text(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    parts = []
    for cell in data.get("cells", []):
        parts.extend(cell.get("source", []))
    return "".join(parts)


def main() -> int:
    failures = []
    for path in sorted(NOTEBOOK_ROOT.rglob("*.ipynb")):
        rel = path.relative_to(ROOT)
        if rel in ALLOWLIST:
            continue
        text = notebook_text(path)
        for label, pattern in RULES.items():
            if pattern.search(text):
                failures.append((str(rel), label))

    if failures:
        print("Notebook architecture check failed:")
        for rel, label in failures:
            print(f"  {rel}: {label}")
        return 1

    print("Notebook architecture check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
