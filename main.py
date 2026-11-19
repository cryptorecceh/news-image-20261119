"""Write the 19 November 2026 front page to the output directory.

The finished picture ships in this repository as ``entry.png``. This script
is the graded entry: it needs nothing but the Python standard library, it
touches no network, and it writes exactly the same bytes every time it runs.

Usage (the way the grader runs it, from a fresh checkout):

    python3 main.py

By default the picture lands at ``/output/entry.png``. Set
``MAKEFUN_OUTPUT_DIR`` to point it somewhere else while testing, e.g.::

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _looks_like_picture(blob):
    return blob.startswith(PNG_MAGIC) or blob.startswith(JPEG_MAGIC)


def run():
    here = Path(__file__).resolve().parent
    picture = here / "entry.png"
    if not picture.exists():
        sys.exit("entry.png is missing next to " + __file__)
    blob = picture.read_bytes()
    if not _looks_like_picture(blob):
        sys.exit("entry.png does not start with a PNG or JPEG magic")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        sys.exit("cannot create output directory %s: %s" % (target_dir, exc))
    target = target_dir / "entry.png"
    target.write_bytes(blob)
    if _digest(target) != _digest(picture):
        sys.exit("entry.png was not copied completely")
    sys.stdout.write("wrote %s (%d bytes)\n" % (target, len(blob)))


if __name__ == "__main__":
    run()
