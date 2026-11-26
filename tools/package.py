"""Check that no firmware is in the repository, and package the source.

Elektron's stock OS is not ours to share, and every image this project builds
contains it, so neither may ever be committed or packaged. What is shared is
the patcher: the mods' sources, the registry and the tools that build an image
from a stock file the user downloads from Elektron.

    python3 tools/package.py --check            # every tracked file
    python3 tools/package.py --check --staged   # what is about to be committed
    python3 tools/package.py                    # the zip, from HEAD

The zip is `git archive` of HEAD, so it holds tracked files only (no build/,
stock/*.syx, .venv or vendor/), and is checked again after it is written. It
goes to build/package/, never into the repository.

Refused: firmware and build file types, any file with an Elektron SysEx header
(F0 00 20 3C) in it, any binary file, any file over 1 MB. Standard library only.

To run the staged check before every commit:

    git config core.hooksPath tools/hooks
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "package"
NAME = "rytm-mods-lite"

BANNED_EXT = {".syx", ".bin", ".hex", ".elf", ".o", ".img", ".zip", ".mid"}
ELEKTRON_SYSEX = bytes([0xF0, 0x00, 0x20, 0x3C])
MAX_BYTES = 1 << 20


def git(*args: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True,
                          capture_output=True).stdout


def problems(path: str, data: bytes) -> list[str]:
    out = []
    if Path(path).suffix.lower() in BANNED_EXT:
        out.append("firmware or build file type")
    if ELEKTRON_SYSEX in data:
        out.append("contains an Elektron SysEx header (F0 00 20 3C)")
    if b"\x00" in data:
        out.append("binary file")
    if len(data) > MAX_BYTES:
        out.append(f"{len(data)} bytes, over {MAX_BYTES}")
    return out


def tracked() -> dict[str, bytes]:
    names = git("ls-files", "-z").decode().split("\0")
    return {n: (ROOT / n).read_bytes() for n in names if n and (ROOT / n).is_file()}


def staged() -> dict[str, bytes]:
    names = git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR").decode().split("\0")
    return {n: git("show", f":{n}") for n in names if n}


def check(files: dict[str, bytes], what: str) -> bool:
    bad = {p: problems(p, d) for p, d in files.items()}
    bad = {p: r for p, r in bad.items() if r}
    for p, r in sorted(bad.items()):
        print(f"REFUSED {p}: {'; '.join(r)}", file=sys.stderr)
    if bad:
        print(f"{what}: {len(bad)} file(s) refused. Firmware stays with Elektron: "
              "share the mods and the tools, never a .syx.", file=sys.stderr)
        return False
    print(f"{what}: {len(files)} files, no firmware")
    return True


def package() -> Path:
    if git("status", "--porcelain", "--untracked-files=no").strip():
        print("note: uncommitted changes are not in the zip, it is made from HEAD",
              file=sys.stderr)
    rev = git("rev-parse", "--short", "HEAD").decode().strip()
    OUT.mkdir(parents=True, exist_ok=True)
    zpath = OUT / f"{NAME}-{rev}.zip"
    git("archive", "--format=zip", f"--prefix={NAME}/", "-o", str(zpath), "HEAD")
    with zipfile.ZipFile(zpath) as z:
        files = {i.filename: z.read(i) for i in z.infolist() if not i.is_dir()}
    if not check(files, zpath.name):
        zpath.unlink()
        raise SystemExit(1)
    return zpath


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="check only, write nothing")
    ap.add_argument("--staged", action="store_true", help="with --check: the index, not the tree")
    a = ap.parse_args()
    if a.check:
        ok = check(staged() if a.staged else tracked(), "staged" if a.staged else "tracked")
        raise SystemExit(0 if ok else 1)
    if not check(tracked(), "tracked"):
        raise SystemExit(1)
    print(f"wrote {package().relative_to(ROOT)}")


if __name__ == "__main__":
    main()
