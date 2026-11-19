"""news-image-20261119 entry: write the finished front page to /output/entry.png.

Standard library only. The image ships in the repository as entry.png; this
program copies it byte for byte, so two runs write identical bytes and no
network is needed. Run locally with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
from pathlib import Path


def main():
    repo = Path(__file__).resolve().parent
    source = repo / "entry.png"
    if not source.is_file():
        raise SystemExit("entry.png missing next to " + __file__)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SystemExit(f"cannot create output dir {out_dir}: {exc}")
    written = out_dir / "entry.png"
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    shutil.copyfile(source, written)
    if hashlib.sha256(written.read_bytes()).hexdigest() != source_hash:
        raise SystemExit("entry.png copy incomplete")
    print(f"wrote {written} ({written.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
