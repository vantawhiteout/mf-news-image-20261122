#!/usr/bin/env python3
"""Entry point: hand the day's finished front page to the grader.

The artwork is committed as entry.png (drawn by render.py during the build).
This program only copies those bytes into MAKEFUN_OUTPUT_DIR, so both graded
runs produce an identical file and no network or third-party package is used.
"""

import os
import shutil
from pathlib import Path

bot_dir = Path(os.environ.get("MAKEFUN_BOT_DIR", Path(__file__).resolve().parent))
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output")).resolve()

source = bot_dir / "entry.png"
if not source.is_file():
    raise SystemExit("entry.png is missing from the repository")

out_dir.mkdir(parents=True, exist_ok=True)
target = out_dir / "entry.png"
shutil.copyfile(source, target)
print(f"wrote {target} ({target.stat().st_size} bytes)")
