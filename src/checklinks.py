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


def check_cms_config():
    """A tartalomkezelő beállításfájljának ellenőrzése.

    Egy elrontott config.yml az egész szerkesztőfelületet megbénítja, ezért
    a build már azelőtt elbukik, hogy élesbe kerülne.
    """
    path = os.path.join(OUT, "admin", "config.yml")
    if not os.path.isfile(path):
        return 0
    try:
        import yaml
    except ImportError:
        print("A PyYAML nincs telepítve — a CMS-beállítás ellenőrzése kimarad.")
        return 0
    try:
        data = yaml.safe_load(open(path, encoding="utf-8"))
    except yaml.YAMLError as exc:
        print("HIBÁS CMS-BEÁLLÍTÁS (admin/config.yml):")
        print(exc)
        return 1
    problems = []
    if not data.get("backend", {}).get("repo"):
        problems.append("hiányzik a backend.repo")
    elif "__REPO__" in str(data["backend"]["repo"]):
        print("  Megjegyzés: a tároló neve még nincs kitöltve (nincs git origin).")
    for col in data.get("collections", []):
        if "files" in col:
            for f in col["files"]:
                target = os.path.join(ROOT, f.get("file", ""))
                if not os.path.isfile(target):
                    problems.append("hiányzó adatfájl: %s" % f.get("file"))
        elif col.get("folder"):
            if not os.path.isdir(os.path.join(ROOT, col["folder"])):
                problems.append("hiányzó mappa: %s" % col["folder"])
    if problems:
        print("HIBÁS CMS-BEÁLLÍTÁS:")
        for p in problems:
            print("  -", p)
        return 1
    print("✓ A tartalomkezelő beállítása érvényes.")
    return 0


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
            target = href.split("#")[0].split("?")[0]
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
    return check_cms_config()


if __name__ == "__main__":
    sys.exit(main())
