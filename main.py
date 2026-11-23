#!/usr/bin/env python3
# news-image-20261122 entry: emit the bundled picture, byte for byte.
#
# The bounty asks for a program that writes one image. Ours keeps the
# finished picture in the repository and hands it over unchanged.
# Pure standard library, no network access, no clock reads, no
# randomness, so running it twice gives the same file both times.
# The picture was drawn by build_image.py in this same folder.

from pathlib import Path as _P


def _picture_bytes():
    here = _P(__file__).parent
    return (here / "entry.png").read_bytes()


def _destination():
    out_dir = _P("/output")
    if out_dir.is_dir():
        return out_dir / "entry.png"
    local = _P(__file__).parent / "output"
    local.mkdir(parents=True, exist_ok=True)
    return local / "entry.png"


def run():
    target = _destination()
    target.write_bytes(_picture_bytes())


if __name__ == "__main__":
    run()
