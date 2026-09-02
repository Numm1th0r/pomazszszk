# -*- coding: utf-8 -*-
"""
Minimális Markdown-feldolgozó — külső könyvtár nélkül.

Azt a részhalmazt kezeli, amit a Sveltia/Decap CMS szövegszerkesztője előállít:
címsorok, bekezdések, felsorolások, idézet, vízszintes vonal, képek, linkek,
félkövér/dőlt/kódrészlet, valamint a nyers HTML-blokkok változatlan átengedése.

Két függvényt ad:
    split_front_matter(text) -> (meta: dict, body: str)
    render(markdown_text)    -> HTML
"""

import html
import re

__all__ = ["split_front_matter", "render"]


# --- YAML-szerű fejléc ----------------------------------------------------

def _coerce(value):
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    low = v.lower()
    if low in ("true", "igen", "yes"):
        return True
    if low in ("false", "nem", "no"):
        return False
    if low in ("", "null", "~"):
        return ""
    return v


def _parse_block(lines, pos, indent):
    """Egy behúzási szinthez tartozó kulcs-érték blokk beolvasása."""
    result = {}
    while pos < len(lines):
        raw = lines[pos]
        if not raw.strip() or raw.lstrip().startswith("#"):
            pos += 1
            continue
        cur = len(raw) - len(raw.lstrip())
        if cur < indent or raw.lstrip().startswith("- "):
            break
        if ":" not in raw:
            pos += 1
            continue
        key, _, value = raw.strip().partition(":")
        key = key.strip()
        if value.strip():
            result[key] = _coerce(value)
            pos += 1
            continue
        # Üres érték: alatta beágyazott lista következhet.
        items, pos = _parse_list(lines, pos + 1, cur)
        result[key] = items if items else ""
    return result, pos


def _parse_list(lines, pos, parent_indent):
    """`- ` kezdetű elemek: egyszerű értékek vagy kulcs-érték blokkok."""
    items = []
    while pos < len(lines):
        raw = lines[pos]
        if not raw.strip():
            pos += 1
            continue
        cur = len(raw) - len(raw.lstrip())
        stripped = raw.lstrip()
        if cur <= parent_indent or not stripped.startswith("- "):
            break
        rest = stripped[2:].strip()
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", rest)
        if m:
            entry = {m.group(1): _coerce(m.group(2))}
            pos += 1
            extra, pos = _parse_block(lines, pos, cur + 2)
            entry.update(extra)
            items.append(entry)
        else:
            items.append(_coerce(rest))
            pos += 1
    return items, pos


def split_front_matter(text):
    """A `---` közé zárt fejlécet szótárrá alakítja, és visszaadja a törzset is.

    A kulcs-érték párokon túl a beágyazott listákat is felismeri – ezt írja a
    tartalomkezelő, amikor egy albumhoz több képet rendelünk.
    """
    text = text.lstrip("﻿")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    head = text[3:end]
    body = text[end + 4:].lstrip("\n")
    meta, _ = _parse_block(head.splitlines(), 0, 0)
    return meta, body

# --- Sorközi elemek -------------------------------------------------------

_CODE = re.compile(r"`([^`]+)`")
_IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITAL = re.compile(r"(?<![*\w])[*_]([^*_\n]+)[*_](?![*\w])")


def _inline(text, media_prefix=""):
    out = html.escape(text, quote=False)

    placeholders = []

    def stash(markup):
        placeholders.append(markup)
        return "\x00%d\x00" % (len(placeholders) - 1)

    def img(m):
        alt, src, title = m.group(1), m.group(2), m.group(3)
        if media_prefix and not re.match(r"^(https?:|/|data:)", src):
            src = media_prefix + src
        t = ' title="%s"' % html.escape(title, quote=True) if title else ""
        return stash('<img src="%s" alt="%s"%s loading="lazy">'
                     % (html.escape(src, quote=True), html.escape(alt, quote=True), t))

    def link(m):
        label, href, title = m.group(1), m.group(2), m.group(3)
        extra = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        t = ' title="%s"' % html.escape(title, quote=True) if title else ""
        return stash('<a href="%s"%s%s>%s</a>'
                     % (html.escape(href, quote=True), t, extra, label))

    out = _CODE.sub(lambda m: stash("<code>%s</code>" % m.group(1)), out)
    out = _IMG.sub(img, out)
    out = _LINK.sub(link, out)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _ITAL.sub(r"<em>\1</em>", out)
    out = out.replace("  \n", "<br>\n")

    for i, markup in enumerate(placeholders):
        out = out.replace("\x00%d\x00" % i, markup)
    return out


# --- Blokkszintű elemek ---------------------------------------------------

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_ULI = re.compile(r"^\s*[-*+]\s+(.*)$")
_OLI = re.compile(r"^\s*\d+[.)]\s+(.*)$")
_HR = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")


def render(text, media_prefix="", heading_offset=1):
    """Markdown → HTML. A `#` alapból `<h2>` lesz (heading_offset=1)."""
    lines = (text or "").replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        # Nyers HTML-blokk: változatlanul átengedjük az üres sorig.
        if line.lstrip().startswith("<"):
            block = []
            while i < n and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append("\n".join(block))
            continue

        if _HR.match(line):
            out.append("<hr>")
            i += 1
            continue

        m = _HEADING.match(line)
        if m:
            level = min(len(m.group(1)) + heading_offset, 6)
            out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2).strip(), media_prefix), level))
            i += 1
            continue

        if line.lstrip().startswith(">"):
            quote = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote.append(lines[i].lstrip()[1:].lstrip())
                i += 1
            inner = render("\n".join(quote), media_prefix, heading_offset)
            out.append("<blockquote>%s</blockquote>" % inner)
            continue

        if _ULI.match(line) or _OLI.match(line):
            ordered = bool(_OLI.match(line))
            pattern = _OLI if ordered else _ULI
            items = []
            while i < n and pattern.match(lines[i]):
                items.append(pattern.match(lines[i]).group(1).strip())
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (
                tag, "".join("<li>%s</li>" % _inline(it, media_prefix) for it in items), tag))
            continue

        # Bekezdés
        para = []
        while i < n and lines[i].strip() and not (
            _HEADING.match(lines[i]) or _ULI.match(lines[i]) or _OLI.match(lines[i])
            or _HR.match(lines[i]) or lines[i].lstrip().startswith(">")
            or lines[i].lstrip().startswith("<")
        ):
            para.append(lines[i].strip())
            i += 1
        joined = "\n".join(para)
        rendered = _inline(joined, media_prefix)
        # Az önmagában álló kép ne kerüljön bekezdésbe.
        if re.fullmatch(r"<img [^>]+>", rendered.strip()):
            out.append('<figure class="post__figure">%s</figure>' % rendered.strip())
        else:
            out.append("<p>%s</p>" % rendered)

    return "\n".join(out)


def plain_text(markdown_text, limit=None):
    """Egyszerű szöveggé alakítás (kivonathoz, RSS-hez)."""
    s = re.sub(r"^---.*?\n---\n", "", markdown_text, flags=re.S)
    s = _IMG.sub("", s)
    s = _LINK.sub(r"\1", s)
    s = re.sub(r"[#>*_`]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    if limit and len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0] + "…"
    return s
