#!/usr/bin/env python3
"""Exporta ~/Projects/ad-astra/registro/fundamentos-niveles.md → data/ad-astra.json (lo usa el cerebro del lab)."""
import os, re, json, datetime
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
rows = []
for ln in open(os.path.expanduser("~/Projects/ad-astra/registro/fundamentos-niveles.md"), encoding="utf-8"):
    m = re.match(r"\|\s*(Inglés|Programación|Matemáticas|Paper IAC)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*/\s*(\d+)\s*\|\s*([^|]+)\|", ln)
    if m: rows.append({"ruta": m.group(1), "nivel": int(m.group(2)), "aprobados": int(m.group(3)), "total": int(m.group(4)), "tema": m.group(5).strip()})
json.dump({"actualizado": datetime.date.today().isoformat(), "rutas": rows}, open(os.path.join(ROOT, "data", "ad-astra.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"ad-astra.json · {len(rows)} rutas")
