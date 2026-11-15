#!/usr/bin/env python3
"""Build Tsumego Dojo's built-in library from a folder of SGF problems.

Usage:
    python3 tools/build_data.py path/to/sgf [--out data] [--chunk 400]

The input folder holds one subfolder per rank, named like the app's ranks
(30k ... 1k, 1d ... 9d). Each problem is one .sgf file inside its rank folder:

    sgf/
      25k/101.sgf
      25k/102.sgf
      3d/7.sgf

A file's id is the number in its file name (101.sgf -> 101); files without a
number get the next free id. Mark correct end positions with RIGHT in the move's
comment (C[RIGHT ...]) and failing lines with WRONG.

The script writes:
    data/index.json            ranks -> chunk files and problem ids (Practice, Ladder)
    data/<rank>-<n>.json       chunks of [id, sgf] pairs, loaded on demand
    data/rush/index.json       one chunk per rank for Tsumego Rush

Only build from problems you have the right to publish.
"""
import argparse
import json
import re
import sys
from pathlib import Path

RANKS = [f"{k}k" for k in range(30, 0, -1)] + [f"{d}d" for d in range(1, 10)]
TYPES = ["life_and_death", "tesuji", "joseki", "fuseki", "endgame", "best_move", "elementary", "other"]


def problem_type(sgf: str) -> int:
    """Read an optional 'Type: <name>' line from the root comment."""
    m = re.search(r"Type:\s*([a-z_]+)", sgf)
    if m and m.group(1) in TYPES:
        return TYPES.index(m.group(1))
    return TYPES.index("other")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path, help="folder with one subfolder per rank")
    ap.add_argument("--out", type=Path, default=Path("data"), help="output folder (default: data)")
    ap.add_argument("--chunk", type=int, default=400, help="problems per chunk file (default: 400)")
    args = ap.parse_args()

    if not args.src.is_dir():
        print(f"error: {args.src} is not a folder", file=sys.stderr)
        return 1

    out = args.out
    (out / "rush").mkdir(parents=True, exist_ok=True)
    index = {"ranks": [], "types": TYPES}
    rush = {"ranks": [], "types": TYPES}
    total = 0

    for n, rank in enumerate(RANKS):
        folder = args.src / rank
        if not folder.is_dir():
            continue
        problems, used = [], set()
        files = sorted(folder.glob("*.sgf"), key=lambda p: (not p.stem.isdigit(), int(p.stem) if p.stem.isdigit() else 0, p.name))
        for f in files:
            text = f.read_text(encoding="utf-8", errors="replace").strip()
            if not text.startswith("("):
                print(f"skip {f}: not an SGF", file=sys.stderr)
                continue
            m = re.search(r"(\d+)$", f.stem)
            pid = int(m.group(1)) if m else None
            if pid is None or pid in used:
                pid = max(used, default=0) + 1
            used.add(pid)
            problems.append((pid, text))
        if not problems:
            continue

        chunks = []
        for c in range(0, len(problems), args.chunk):
            part = problems[c:c + args.chunk]
            name = f"{rank}-{c // args.chunk}.json"
            (out / name).write_text(json.dumps([[pid, sgf] for pid, sgf in part], ensure_ascii=False), encoding="utf-8")
            chunks.append({"file": f"data/{name}", "ids": [pid for pid, _ in part], "t": [problem_type(sgf) for _, sgf in part]})
        index["ranks"].append({"rank": rank, "n": n, "chunks": chunks})
        rush["ranks"].append({"rank": rank, "n": n, **chunks[0]})
        total += len(problems)
        print(f"{rank:>4}: {len(problems)} problems in {len(chunks)} chunk(s)")

    (out / "index.json").write_text(json.dumps(index), encoding="utf-8")
    (out / "rush" / "index.json").write_text(json.dumps(rush), encoding="utf-8")
    print(f"done: {total} problems written to {out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
