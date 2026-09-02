# -*- coding: utf-8 -*-
"""
A legenerált honlap belső hivatkozásainak ellenőrzése.

Hibás hivatkozás esetén nem nullás kilépési kóddal áll le, így a
GitHub Action megbukik, mielőtt törött oldal kerülne ki élesbe.

    python3 src/checklinks.py
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")

EXTERNAL = re.compile(r"^(https?:|mailto:|tel:|data:|#)")


def main():
    pages = sorted(glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True))
    if not pages:
        print("Nincs legenerált oldal — előbb futtasd: python3 src/build.py")
        return 1

    broken = []
    for page in pages:
        base = os.path.dirname(page)
        html = open(page, encoding="utf-8").read()
        for href in re.findall(r'(?:href|src)="([^"]+)"', html):
            if EXTERNAL.match(href):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                broken.append((os.path.relpath(page, ROOT), href))

    print("Ellenőrzött oldalak: %d" % len(pages))
    if broken:
        print("HIBÁS HIVATKOZÁSOK (%d):" % len(broken))
        for page, href in broken:
            print("  %s  ->  %s" % (page, href))
        return 1

    print("✓ Minden belső hivatkozás létező fájlra mutat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
