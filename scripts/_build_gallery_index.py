#!/usr/bin/env python3
"""扫描 ~/hermes 下所有图片，生成 _gallery_index.json（含 mtime）。"""
import os, json, time
from pathlib import Path

BASE = Path("/Users/mac/hermes")
OUT = BASE / "_gallery_index.json"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", "$RECYCLE.BIN"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}

def walk(base):
    items = []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in files:
            if f in EXCLUDE_FILES: continue
            ext = os.path.splitext(f)[1].lower()
            if ext not in IMG_EXTS: continue
            full = Path(root) / f
            rel = str(full.relative_to(base))
            stat = full.stat()
            items.append({"path": rel, "mtime": stat.st_mtime, "size": stat.st_size})
    return items

items = walk(BASE)
items.sort(key=lambda x: x["mtime"], reverse=True)
out = {
    "version": "1.0",
    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime()),
    "base": "~/hermes",
    "count": len(items),
    "items": items,
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK: {len(items)} 张 → {OUT}")
print("Top 5 (mtime 倒序):")
for it in items[:5]:
    ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(it["mtime"]))
    print(f"  {ts}  {it['path']}")
