#!/usr/bin/env bash
# clear-nbs.sh — strip outputs from all .ipynb under CWD (v3 & v4), with backups.
set -euo pipefail
shopt -s nullglob

mapfile -d '' files < <(find . -type f -name "*.ipynb" -print0)
((${#files[@]})) || { echo "No .ipynb files found."; exit 0; }

for nb in "${files[@]}"; do
  echo "Processing: $nb"

  python3 - "$nb" <<'PY'
import json, sys, os, shutil, time, pathlib

p = pathlib.Path(sys.argv[1])
ts = time.strftime("%Y%m%d-%H%M%S")

backup_root = pathlib.Path("backups")
rel = p
if rel.parts and rel.parts[0] == ".":
  rel = pathlib.Path(*rel.parts[1:])
elif rel.is_absolute():
  try:
    rel = rel.relative_to(pathlib.Path.cwd())
  except ValueError:
    rel = rel.name

backup_path = (backup_root / rel).with_suffix(p.suffix + f".bak.{ts}")
backup_path.parent.mkdir(parents=True, exist_ok=True)

shutil.copy2(p, backup_path)

with p.open("r", encoding="utf-8") as f:
  nb = json.load(f)

def clean_code_cell(c):
  # v4
  if "execution_count" in c:
    c["execution_count"] = None
  # v3
  if "prompt_number" in c:
    c["prompt_number"] = None
  # both
  c["outputs"] = []
  return c

def count_cells(n):
  if isinstance(n, dict) and "cells" in n:           # v4
    return len(n["cells"])
  if isinstance(n, dict) and "worksheets" in n:      # v3
    return sum(len(ws.get("cells", [])) for ws in n["worksheets"])
  return 0

before = count_cells(nb)

if "cells" in nb:  # v4
  nb["cells"] = [clean_code_cell(c) if c.get("cell_type")=="code" else c
                 for c in nb["cells"]]
elif "worksheets" in nb:  # v3
  for ws in nb["worksheets"]:
    ws["cells"] = [clean_code_cell(c) if c.get("cell_type")=="code" else c
                   for c in ws.get("cells", [])]
else:
  print(f"SKIP (unknown notebook format): {p}")
  sys.exit(0)

after = count_cells(nb)
if after != before:
  print(f"ABORT (cell count changed {before}->{after}): {p}. Backup at {backup_path}")
  sys.exit(1)

p_tmp = p.with_suffix(p.suffix + ".tmp")
with p_tmp.open("w", encoding="utf-8") as f:
  json.dump(nb, f, ensure_ascii=False, separators=(",", ":"))
os.replace(p_tmp, p)
print(f"Cleared outputs OK | cells: {after} | backup: {backup_path}")
PY

done

echo "✅ Done."
