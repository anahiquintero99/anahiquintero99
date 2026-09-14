#!/bin/bash
# Regenera lab.svg con el token local de gh (ve repos privados) y lo sube a la rama output.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/ad-astra-export.py
python3 scripts/annie_lab.py dist/annie-lab.svg
if ! git diff --quiet -- data; then git add data && git commit -qm "data: foto de estadísticas, misiones y Ad Astra $(date '+%F %H:%M')" && git push -q origin master; fi
git worktree prune; git branch -D output -q 2>/dev/null || true
if git fetch -q origin output 2>/dev/null; then git branch -q output origin/output; else W0="$(mktemp -d)"; git worktree add -q --detach "$W0"; (cd "$W0" && git checkout -q --orphan output && git rm -rfq . && git commit -q --allow-empty -m "output"); git worktree remove -f "$W0"; fi
W="$(mktemp -d)"; git worktree add -q "$W" output
cp dist/annie-lab.svg "$W/"; (cd "$W" && git add annie-lab.svg && git commit -qm "lab.svg $(date +%F)" && git push -q origin output)
git worktree remove -f "$W"; echo "lab.svg publicado"
