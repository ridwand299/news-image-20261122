"""Entry program for make.fun bounty news-image-20261122.

Copies the bundled entry.png (1024x1024, 138724 bytes) to
/output/entry.png. Standard library only, no network, no clock,
no randomness -- both runs write identical bytes. This is the
"simplest program" the bounty brief explicitly allows: a program
that copies an image the repository holds.
The image itself was rendered locally by build_image.py (Pillow).
"""
import shutil
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent / "entry.png"
    out = Path("/output/entry.png") if Path("/output").is_dir() else Path(__file__).resolve().parent / "output" / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out)


if __name__ == "__main__":
    main()
