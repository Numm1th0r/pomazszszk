# -*- coding: utf-8 -*-
"""
Statikus oldalgenerátor a pomázi Szociális Szolgáltatási Központ honlapjához.

Használat:
    python3 src/build.py              # a teljes, több oldalas honlap a site/ mappába
    python3 src/build.py --artifact   # egyetlen, önmagában futó HTML fájl (előnézet)
"""

import base64
import html
import mimetypes
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import (  # noqa: E402
    SITE, NAV, NAV_CTA, SERVICES, NEWS, GALLERY, DOC_GROUPS,
    CONTACT_UNITS, LEADERS, LAW_GROUPS, USEFUL_LINKS,
)
from icons import icon, LOGO  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
ASSETS = os.path.join(ROOT, "assets")          # forrás: képek, CSS, JS
ADMIN = os.path.join(ROOT, "src", "admin")     # forrás: a szerkesztőfelület

SINGLE_FILE = "--artifact" in sys.argv


def asset_version():
    """Rövid tartalom-lenyomat a style.css + app.js fájlokból.

    Ez kerül a hivatkozások végére (?v=...), hogy egy új változat után a
    böngésző soha ne párosíthasson friss HTML-t régi, gyorsítótárazott
    stíluslappal. A GitHub Pages 10 percig tárolja az eszközöket.
    """
    import hashlib
    h = hashlib.sha1()
    for name in ("style.css", "app.js"):
        path = os.path.join(ROOT, "assets", name)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                h.update(f.read())
    return h.hexdigest()[:8]


ASSET_V = asset_version()

# =============================================================================
# Segédfüggvények
# =============================================================================

def esc(s):
    return html.escape(str(s), quote=True)


def rel(target, depth):
    """Gyökérhez képesti hivatkozás átírása az oldal mélységéhez."""
    if SINGLE_FILE:
        return target
    if re.match(r"^(https?:|mailto:|tel:|#)", target):
        return target
    return ("../" * depth) + target


def is_external(href):
    return bool(re.match(r"^https?:", href))


def link_attrs(href):
    return ' target="_blank" rel="noopener"' if is_external(href) else ""


def phone_list(phones, depth=0, sep=" · "):
    return sep.join(f'<a href="{esc(h)}">{esc(t)}</a>' for t, h in phones)


# =============================================================================
# Sablonelemek
# =============================================================================

def utility_bar(depth):
    return f"""
<div class="utility">
  <div class="container utility__row">
    <span class="utility__item">{icon("phone")}<a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a></span>
    <span class="utility__item">{icon("mail")}<a href="mailto:{SITE['email']}">{esc(SITE['email'])}</a></span>
    <span class="utility__item">{icon("clock")}{esc(SITE['office_hours'])}</span>
    <div class="utility__spacer"></div>
    <div class="a11y" role="group" aria-label="Megjelenítési beállítások">
      <span class="a11y__label">{icon("accessibility")}<span class="visually-hidden">Betűméret</span></span>
      <button type="button" data-textsize-btn="m" aria-pressed="true" title="Alap betűméret"><span class="a11y__a-sm" aria-hidden="true">A</span><span class="visually-hidden">Alap betűméret</span></button>
      <button type="button" data-textsize-btn="l" aria-pressed="false" title="Nagyobb betűméret"><span class="a11y__a-md" aria-hidden="true">A</span><span class="visually-hidden">Nagyobb betűméret</span></button>
      <button type="button" data-textsize-btn="xl" aria-pressed="false" title="Legnagyobb betűméret"><span class="a11y__a-lg" aria-hidden="true">A</span><span class="visually-hidden">Legnagyobb betűméret</span></button>
      <button type="button" data-contrast-btn aria-pressed="false" title="Nagy kontrasztú megjelenítés">Kontraszt</button>
    </div>
  </div>
</div>"""


def masthead(depth, active):
    items = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        items.append(f'<li><a class="nav__link" href="{rel(href, depth)}"{cur}>{esc(label)}</a></li>')
    cta_cur = ' aria-current="page"' if NAV_CTA[1] == active else ""
    return f"""
<header class="masthead">
  <div class="container masthead__row">
    <a class="brand" href="{rel('index.html', depth)}">
      {LOGO}
      <span class="brand__text">
        <span class="brand__name">Szociális Szolgáltatási Központ</span>
        <span class="brand__place">Pomáz</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="fomenu">
      {icon("menu")}<span>Menü</span>
    </button>
    <nav class="nav" id="fomenu" aria-label="Főmenü">
      <button class="nav-close" type="button" data-nav-close aria-label="Menü bezárása">{icon("close")}</button>
      <ul class="nav__list">
        {''.join(items)}
        <li><a class="nav__cta" href="{rel(NAV_CTA[1], depth)}"{cta_cur}>{esc(NAV_CTA[0])}</a></li>
      </ul>
      <div class="nav__extra">
        <p class="nav__extra-title">Elérhetőség</p>
        <p class="nav__extra-line">{icon("phone")}<a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a></p>
        <p class="nav__extra-line">{icon("mail")}<a href="mailto:{SITE['email']}">{esc(SITE['email'])}</a></p>
        <p class="nav__extra-line">{icon("clock")}<span>{esc(SITE['office_hours'])}</span></p>
        <p class="nav__extra-title">Megjelenítés</p>
        <div class="a11y a11y--drawer" role="group" aria-label="Megjelenítési beállítások">
          <button type="button" data-textsize-btn="m" aria-pressed="true" title="Alap betűméret"><span class="a11y__a-sm" aria-hidden="true">A</span><span class="visually-hidden">Alap betűméret</span></button>
          <button type="button" data-textsize-btn="l" aria-pressed="false" title="Nagyobb betűméret"><span class="a11y__a-md" aria-hidden="true">A</span><span class="visually-hidden">Nagyobb betűméret</span></button>
          <button type="button" data-textsize-btn="xl" aria-pressed="false" title="Legnagyobb betűméret"><span class="a11y__a-lg" aria-hidden="true">A</span><span class="visually-hidden">Legnagyobb betűméret</span></button>
          <button type="button" data-contrast-btn aria-pressed="false" title="Nagy kontrasztú megjelenítés">Kontraszt</button>
        </div>
      </div>
    </nav>
    <!-- A sötétítő rétegnek a fejléc rétegkontextusán BELÜL kell lennie,
         különben a fölé kerül a menüfióknak (a .masthead z-index-e miatt). -->
    <div class="nav-scrim" data-nav-scrim></div>
  </div>
</header>"""


def footer(depth):
    svc = "".join(
        f'<li><a href="{rel("szolgaltatasok/" + s["slug"] + ".html", depth)}">{esc(s["nav_title"])}</a></li>'
        for s in SERVICES
    )
    return f"""
<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <div class="footer__brand">
          {LOGO}
          <span class="footer__name">Szociális Szolgáltatási<br>Központ, Pomáz</span>
        </div>
        <p>{esc(SITE['address'])}<br>
        <a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a><br>
        <a href="mailto:{SITE['email']}">{esc(SITE['email'])}</a></p>
        <p>Ügyfélfogadás: {esc(SITE['office_hours'])}</p>
      </div>
      <div>
        <h2>Szolgáltatásaink</h2>
        <ul>{svc}</ul>
      </div>
      <div>
        <h2>Intézményünk</h2>
        <ul>
          <li><a href="{rel('intezmenyunk.html', depth)}">Bemutatkozás és köszöntő</a></li>
          <li><a href="{rel('intezmenyunk.html#szervezet', depth)}">Szervezeti felépítés</a></li>
          <li><a href="{rel('allaslehetoseg.html', depth)}">Álláslehetőség</a></li>
          <li><a href="{rel('hirek.html', depth)}">Hírek</a></li>
          <li><a href="{rel('kepgaleria.html', depth)}">Képgaléria</a></li>
        </ul>
      </div>
      <div>
        <h2>Közérdekű adatok</h2>
        <ul>
          <li><a href="{rel('kozzeteteli-lista.html', depth)}">Általános közzétételi lista</a></li>
          <li><a href="{rel('jogszabalyok.html', depth)}">Alkalmazandó jogszabályok</a></li>
          <li><a href="{rel('dokumentumok.html', depth)}">Nyomtatványok, ügyintézés</a></li>
          <li><a href="https://pomaz.hu" target="_blank" rel="noopener">Fenntartó: Pomáz Város Önkormányzata</a></li>
          <li><a href="https://kormanyhivatalok.hu/kormanyhivatalok/pest" target="_blank" rel="noopener">Pest Vármegyei Kormányhivatal</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <p>© 2026 Szociális Szolgáltatási Központ, Pomáz. Minden jog fenntartva.</p>
      <p class="footer__spacer">Fenntartó: Pomáz Város Önkormányzata</p>
    </div>
  </div>
</footer>"""


def crumbs(items, depth):
    """items: [(label, href|None), ...] — az utolsó az aktuális oldal."""
    li = [f'<li><a href="{rel("index.html", depth)}">Főoldal</a></li>']
    for label, href in items:
        if href:
            li.append(f'<li><a href="{rel(href, depth)}">{esc(label)}</a></li>')
        else:
            li.append(f'<li aria-current="page">{esc(label)}</li>')
    return f'<nav aria-label="Morzsamenü"><ol class="crumbs">{"".join(li)}</ol></nav>'


def pagehead(title, lead, crumb_items, depth):
    return f"""
<section class="pagehead">
  <div class="container">
    {crumbs(crumb_items, depth)}
    <h1>{title}</h1>
    {f'<p class="pagehead__lead">{lead}</p>' if lead else ''}
  </div>
</section>"""


def layout(page):
    depth = page["path"].count("/")
    title = page["title"]
    full_title = title if title.endswith("Pomáz") else f"{title} – Szociális Szolgáltatási Központ, Pomáz"
    desc = page.get("description", SITE["description"])
    a = ("../" * depth) if not SINGLE_FILE else ""
    return f"""<!doctype html>
<html lang="hu" prefix="og: https://ogp.me/ns#">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#1d5b4f">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Szociális Szolgáltatási Központ, Pomáz">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='13' fill='%231d5b4f'/%3E%3Cpath d='M24 31.4s-5.1-3.3-5.1-6.3a2.9 2.9 0 0 1 5.1-1.9 2.9 2.9 0 0 1 5.1 1.9c0 3-5.1 6.3-5.1 6.3Z' fill='%23e08e5a'/%3E%3C/svg%3E">
<link rel="stylesheet" href="{a}assets/style.css?v={ASSET_V}">
<script>
/* A mentett megjelenítési beállítások alkalmazása még az első kirajzolás előtt. */
(function(){{try{{var p=JSON.parse(localStorage.getItem("szszk-prefs"))||{{}},r=document.documentElement;
if(p.textsize&&p.textsize!=="m")r.setAttribute("data-textsize",p.textsize);
if(p.contrast==="high")r.setAttribute("data-contrast","high");}}catch(e){{}}}})();
</script>
</head>
<body>
<a class="skip-link" href="#tartalom">Ugrás a tartalomra</a>
{utility_bar(depth)}
{masthead(depth, page.get("active"))}
<main id="tartalom">
{page["body"]}
</main>
{footer(depth)}
<script src="{a}assets/app.js?v={ASSET_V}"></script>
</body>
</html>
"""


# =============================================================================
# Újrahasznosítható blokkok
# =============================================================================

def service_card(s, depth):
    href = rel(f"szolgaltatasok/{s['slug']}.html", depth)
    fee_cls = "tag--free" if s["fee"] == "Ingyenes" else "tag--fee"
    return f"""
<article class="card card--link">
  <div class="card__media"><img src="{rel('assets/img/' + s['image'], depth)}" alt="{esc(s['image_alt'])}" loading="lazy" width="1100" height="825"></div>
  <div class="card__body">
    <div class="card__meta" style="margin:0 0 .7rem">
      <span class="tag {fee_cls}">{esc(s['fee'])}</span>
      <span class="tag">{icon('pin')}{esc(s['area'])}</span>
    </div>
    <h3 class="card__title"><a href="{href}">{esc(s['title'])}</a></h3>
    <p class="card__text">{esc(s['short'])}</p>
    <span class="card__more">Részletek {icon('arrow-right')}</span>
  </div>
</article>"""


def contact_panel(c, depth, title="Elérhetőség"):
    rows = []
    if c.get("person"):
        rows.append(("users", "Kapcsolattartó", esc(c["person"])))
    if c.get("address"):
        rows.append(("pin", "Cím", esc(c["address"])))
    if c.get("phones"):
        rows.append(("phone", "Telefon", phone_list(c["phones"])))
    if c.get("email"):
        rows.append(("mail", "E-mail", f'<a href="mailto:{c["email"]}">{esc(c["email"])}</a>'))
    for label, mail in c.get("extra_emails", []):
        rows.append(("mail", esc(label), f'<a href="mailto:{mail}">{esc(mail)}</a>'))
    body = "".join(
        f'<div class="dl__row"><span class="dl__ico">{icon(ic)}</span>'
        f'<span><span class="dl__k">{k}</span><br><span class="dl__v">{v}</span></span></div>'
        for ic, k, v in rows
    )
    note = f'<p style="margin:1rem 0 0;font-size:.92rem;color:var(--ink-2)">{esc(c["note"])}</p>' if c.get("note") else ""
    return f'<div class="panel"><p class="panel__title">{esc(title)}</p><div class="dl">{body}</div>{note}</div>'


def helpbar(depth):
    return f"""
<div class="helpbar">
  <a class="helpbar__item" href="{rel('dokumentumok.html', depth)}">
    <span class="helpbar__ico">{icon('file')}</span>
    <span><span class="helpbar__t">Ellátást szeretnék igényelni</span>
    <span class="helpbar__d">Nyomtatványok, szükséges iratok és a menet lépésről lépésre.</span></span>
  </a>
  <a class="helpbar__item helpbar__item--urgent" href="{rel('szolgaltatasok/jelzorendszeres-hazi-segitsegnyujtas.html', depth)}">
    <span class="helpbar__ico">{icon('bell')}</span>
    <span><span class="helpbar__t">Sürgős segítség kell</span>
    <span class="helpbar__d">Jelzőrendszeres segítség 0–24-ben, és a krízisvonalak számai.</span></span>
  </a>
  <a class="helpbar__item" href="{rel('kapcsolat.html', depth)}">
    <span class="helpbar__ico">{icon('chat')}</span>
    <span><span class="helpbar__t">Kérdésem van</span>
    <span class="helpbar__d">Minden szervezeti egység elérhetősége és ügyfélfogadási rendje.</span></span>
  </a>
</div>"""


def cta_band(depth, title="Kérdése van? Keresse munkatársainkat!",
             text="Felkészült kollégáink szívesen segítenek eligazodni az ellátások között, "
                  "és abban is, hogy melyik szolgáltatás illik leginkább az Ön élethelyzetéhez."):
    return f"""
<section class="band">
  <img src="{rel('assets/img/seta.jpg', depth)}" alt="" aria-hidden="true" loading="lazy" width="1800" height="600">
  <div class="container band__inner">
    <h2>{esc(title)}</h2>
    <p>{esc(text)}</p>
    <div class="btn-row" style="margin-top:1.6rem">
      <a class="btn btn--light" href="{SITE['phone_href']}">{icon('phone')} {esc(SITE['phone'])}</a>
      <a class="btn btn--outline-light" href="{rel('kapcsolat.html', depth)}">Összes elérhetőség</a>
    </div>
  </div>
</section>"""


# =============================================================================
# Oldalak
# =============================================================================

def page_index():
    d = 0
    cards = "".join(service_card(s, d) for s in SERVICES[:6])
    news_items = "".join(f"""
  <article class="news__item">
    <p class="news__date"><time datetime="{n['date']}">{esc(n['date_hu'])}</time></p>
    <div>
      <h3 class="news__title"><a href="hirek/{n['slug']}.html">{esc(n['title'])}</a></h3>
      <p class="news__excerpt">{esc(n['excerpt'])}</p>
    </div>
  </article>""" for n in NEWS[:4])

    body = f"""
<section class="hero">
  <div class="container hero__grid">
    <div>
      <p class="hero__eyebrow"><span class="hero__dot"></span><span>Pomáz és Csobánka szociális ellátásai <b>egy helyen</b></span></p>
      <h1>Segítség, amely elkíséri Önt otthonától a közösségig</h1>
      <p class="hero__lead">Étkeztetés, házi segítségnyújtás, jelzőrendszeres segítség, idősek klubja,
      átmeneti gondozóház, családsegítés és iskolavédőnő – nyolc szolgáltatás, egyetlen, jól ismert
      intézménytől. Nyitva állunk minden pomázi lakos előtt, a gyermekektől az idősekig.</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="szolgaltatasok.html">Szolgáltatásaink {icon('arrow-right')}</a>
        <a class="btn btn--ghost" href="{SITE['phone_href']}">{icon('phone')} {esc(SITE['phone'])}</a>
      </div>
    </div>
    <figure class="hero__figure" style="margin:0">
      <img src="assets/img/hero-kozosseg.jpg" alt="Idős emberek beszélgetnek és nevetnek egy világos klubhelyiségben" width="1800" height="1012" fetchpriority="high">
      <figcaption class="hero__badge">
        <strong>50+ év</strong>
        <span>tapasztalat Pomáz idős és rászoruló lakóinak gondozásában</span>
      </figcaption>
    </figure>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    {helpbar(0)}
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section__head">
      <span class="eyebrow">Szolgáltatásaink</span>
      <h2>Mindenre van megoldás – az otthoni segítségtől a bentlakásig</h2>
      <p class="section__lead">Az ellátások többsége Pomáz és Csobánka lakói számára egyaránt elérhető.
      Ha nem tudja, melyikre van szüksége, hívjon minket – együtt kitaláljuk.</p>
    </div>
    <div class="grid grid--3">{cards}</div>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--ghost" href="szolgaltatasok.html">Mind a nyolc szolgáltatás {icon('arrow-right')}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--reverse">
    <div class="split__media">
      <img src="assets/img/tamogatas-kezek.jpg" alt="Két kéz gyengéden összekulcsolva" loading="lazy" width="1200" height="900">
    </div>
    <div class="prose">
      <span class="eyebrow">Köszöntő</span>
      <h2>„Kérem, keresse felkészült munkatársaimat, hogy Önnek is segíthessünk!”</h2>
      <p>Intézményünk valamennyi Pomázon élő lakos előtt – a gyermekektől az idősekig – nyitva áll.
      Tapasztalt, szakképzett munkatársaink arra törekszenek, hogy a polgárok mind teljesebb és
      kiegyensúlyozottabb életet vallhassanak magukénak.</p>
      <p>Igyekszünk segíteni a család működési zavarainak megoldásában, a támogatásokhoz való
      hozzájutásban és a gyermekek szabadidejének hasznos eltöltésében.</p>
      <p style="font-weight:600;margin-bottom:0">dr. Király Eszter<br>
      <span style="font-weight:400;color:var(--ink-2)">intézményvezető</span></p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn--ghost" href="intezmenyunk.html">Intézményünkről bővebben</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="stats">
      <div class="stat"><span class="stat__n">8</span><span class="stat__l">szolgáltatás egy intézményben</span></div>
      <div class="stat"><span class="stat__n">2</span><span class="stat__l">település: Pomáz és Csobánka</span></div>
      <div class="stat"><span class="stat__n">18</span><span class="stat__l">férőhely az Átmeneti Gondozóházban</span></div>
      <div class="stat"><span class="stat__n">25</span><span class="stat__l">férőhely az Idősek Klubjában</span></div>
      <div class="stat"><span class="stat__n">0–24</span><span class="stat__l">jelzőrendszeres készenlét</span></div>
    </div>
  </div>
</section>

{cta_band(0)}

<section class="section">
  <div class="container">
    <div class="section__head">
      <span class="eyebrow">Hírek</span>
      <h2>Ami nálunk történik</h2>
    </div>
    <div class="news">{news_items}</div>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--ghost" href="hirek.html">Összes hír {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return {
        "path": "index.html", "active": None, "body": body,
        "title": "Szociális Szolgáltatási Központ, Pomáz",
        "description": SITE["description"],
    }


def page_intezmenyunk():
    d = 0
    leaders = "".join(f"""
    <div class="tile">
      <span class="tile__icon">{icon('users')}</span>
      <h3>{esc(name)}</h3>
      <p>{esc(role)}</p>
      <p style="margin-top:.8rem"><a href="{tel}">{esc(phone)}</a><br><a href="mailto:{mail}">{esc(mail)}</a></p>
    </div>""" for name, role, phone, tel, mail in LEADERS)

    body = pagehead(
        "Intézményünk",
        "Integrált szociális intézmény vagyunk: alap- és szakellátásokat egyaránt végzünk "
        "Pomáz és Csobánka lakói számára.",
        [("Intézményünk", None)], d) + f"""
<section class="section">
  <div class="container with-aside">
    <div class="prose">
      <blockquote>
        <p>Szeretettel köszöntöm a Pomázi Szociális Szolgáltatási Központ honlapján!</p>
        <p>Célunk, hogy Pomáz, illetve Csobánka részére biztosítsuk azokat a szolgáltatásokat, amelyekre
        a lakosságnak szüksége van. A honlapon tallózva megismerkedhet a Szociális Szolgáltatási Központ
        által nyújtott szolgáltatásokkal és azok tartalmával.</p>
        <p>Intézményünk valamennyi Pomázon élő lakos előtt – a gyermekektől az idősekig – nyitva áll.
        Tapasztalt, szakképzett munkatársaink arra törekszenek, hogy a polgárok mind teljesebb és
        kiegyensúlyozottabb életet vallhassanak magukénak. Igyekeznek segíteni a család működési
        zavarainak megoldásában, a támogatásokhoz való hozzájutásban, a gyermekek szabadidejének
        hasznos eltöltésében.</p>
        <p>Kérem, keresse felkészült munkatársaimat, hogy Önnek is segíthessünk!</p>
        <cite>dr. Király Eszter, intézményvezető</cite>
      </blockquote>

      <h2 id="szervezet">Szervezeti felépítés</h2>
      <p>Integrált intézményünk egy tagintézménnyel és két csoporttal működik. Az átszervezések után
      az iskolai védőnői feladatokat ellátó kolléganő is intézményünkhöz tartozik.</p>
      <ol>
        <li><strong>Család- és Gyermekjóléti Szolgálat</strong> – tagintézmény, alapellátásban végzi a feladatát.
        Vezetője: Benczik Orsolya.</li>
        <li><strong>Idősek Átmeneti Gondozóháza</strong> – csoport, 18 férőhelyes bentlakásos ellátás.
        Vezetője: Majoros Ferencné.</li>
        <li><strong>Idősek Napközbeni Ellátása</strong> – csoport, négy alapszolgáltatással: szociális
        étkeztetés, idősek nappali ellátása (Idősek Klubja), házi segítségnyújtás és jelzőrendszeres
        házi segítségnyújtás. Vezetője: Garai Péterné, a házi és jelzőrendszeres segítségnyújtás szakmai
        vezetője Letonai Gabriella.</li>
        <li><strong>Iskolavédőnői szolgálat</strong> – dr. Temesiné Estermann Andrea.</li>
      </ol>
      <p>Ezen felül idősek és betegek részére – akár kerekesszékkel is – személyszállítást biztosítunk a
      szentendrei és kiskovácsi rendelőintézetekbe.</p>

      <h2>Fenntartó és felügyeleti szerv</h2>
      <div class="grid grid--2" style="margin-top:1.4rem">
        <div class="tile">
          <span class="tile__icon">{icon('building')}</span>
          <h3>Fenntartó</h3>
          <p>Pomáz Város Önkormányzata<br>2013 Pomáz, Kossuth Lajos u. 23–25.</p>
          <p style="margin-top:.7rem"><a href="tel:+3626814300">+36 26 814 300</a><br>
          <a href="mailto:pomaz@pomaz.hu">pomaz@pomaz.hu</a><br>
          <a href="https://pomaz.hu" target="_blank" rel="noopener">pomaz.hu {icon('external')}</a></p>
        </div>
        <div class="tile tile--accent">
          <span class="tile__icon">{icon('shield')}</span>
          <h3>Felügyeleti szerv</h3>
          <p>Pest Vármegyei Kormányhivatal</p>
          <p style="margin-top:.7rem"><a href="https://kormanyhivatalok.hu/kormanyhivatalok/pest" target="_blank" rel="noopener">kormanyhivatalok.hu {icon('external')}</a></p>
        </div>
      </div>
    </div>

    <aside class="aside">
      <div class="panel panel--brand">
        <p class="panel__title">Központi elérhetőség</p>
        <div class="dl">
          <div class="dl__row"><span class="dl__ico">{icon('pin')}</span><span><span class="dl__k">Cím</span><br><span class="dl__v">{esc(SITE['address'])}</span></span></div>
          <div class="dl__row"><span class="dl__ico">{icon('phone')}</span><span><span class="dl__k">Telefon</span><br><span class="dl__v"><a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a> · <a href="{SITE['phone_alt_href']}">{esc(SITE['phone_alt'])}</a></span></span></div>
          <div class="dl__row"><span class="dl__ico">{icon('mail')}</span><span><span class="dl__k">E-mail</span><br><span class="dl__v"><a href="mailto:{SITE['email']}">{esc(SITE['email'])}</a></span></span></div>
          <div class="dl__row"><span class="dl__ico">{icon('clock')}</span><span><span class="dl__k">Ügyfélfogadás</span><br><span class="dl__v">{esc(SITE['office_hours'])}</span></span></div>
        </div>
      </div>
      <div class="panel">
        <p class="panel__title">Közérdekű adatok</p>
        <ul class="doclist">
          <li><a href="kozzeteteli-lista.html">{icon('file')}<span>Általános közzétételi lista</span></a></li>
          <li><a href="jogszabalyok.html">{icon('scale')}<span>Alkalmazandó jogszabályok</span></a></li>
          <li><a href="allaslehetoseg.html">{icon('briefcase')}<span>Álláslehetőség</span></a></li>
        </ul>
      </div>
      <figure style="margin:0">
        <img src="assets/img/intezmeny.jpg" alt="A Szociális Szolgáltatási Központ épülete Pomázon" loading="lazy" width="1600" height="900" style="border-radius:var(--radius);box-shadow:var(--shadow-s)">
        <figcaption style="font-size:.88rem;color:var(--ink-3);margin-top:.6rem">Intézményünk a Községház utca 2. szám alatt.</figcaption>
      </figure>
    </aside>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section__head">
      <span class="eyebrow">Munkatársaink</span>
      <h2>Vezetők és ügyfélkapcsolat</h2>
    </div>
    <div class="grid grid--3">{leaders}</div>
  </div>
</section>

{cta_band(0)}
"""
    return {"path": "intezmenyunk.html", "active": "intezmenyunk.html", "body": body,
            "title": "Intézményünk",
            "description": "A pomázi Szociális Szolgáltatási Központ bemutatkozása: köszöntő, "
                           "szervezeti felépítés, vezetők, fenntartó és felügyeleti szerv."}


def page_szolgaltatasok():
    d = 0
    cards = "".join(service_card(s, d) for s in SERVICES)
    body = pagehead(
        "Szolgáltatásaink",
        "Nyolc ellátási forma az otthoni segítségtől a bentlakásos gondozásig. "
        "Az igénybevétel minden esetben önkéntes, kérelemre indul.",
        [("Szolgáltatásaink", None)], d) + f"""
<section class="section">
  <div class="container">
    <div class="grid grid--3">{cards}</div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <div class="section__head section__head--center">
      <span class="eyebrow">Ügyintézés</span>
      <h2>Hogyan igényelhető az ellátás?</h2>
      <p class="section__lead">Az ellátások igénybevétele önkéntes: az igénylő vagy törvényes képviselője
      szóbeli vagy írásbeli kérelmére indul.</p>
    </div>
    <div class="grid grid--4">
      <div class="tile"><span class="tile__icon">{icon('chat')}</span><h3>1. Érdeklődés</h3><p>Hívjon minket vagy jöjjön be személyesen a Községház utca 2. alá – közösen tisztázzuk, melyik ellátás segít Önnek.</p></div>
      <div class="tile"><span class="tile__icon">{icon('file')}</span><h3>2. Kérelem</h3><p>Kitöltjük a kérelmet, a jövedelemnyilatkozatot és az egészségi állapotra vonatkozó igazolást.</p></div>
      <div class="tile"><span class="tile__icon">{icon('check')}</span><h3>3. Szükségletvizsgálat</h3><p>Házi segítségnyújtásnál gondozási szükségletvizsgálat készül, amely meghatározza a napi óraszámot.</p></div>
      <div class="tile"><span class="tile__icon">{icon('heart')}</span><h3>4. Az ellátás indul</h3><p>Megállapodást kötünk, és az egyeztetett időponttól kezdődik a gondozás.</p></div>
    </div>
    <div class="btn-row" style="margin-top:2rem;justify-content:center">
      <a class="btn btn--primary" href="dokumentumok.html">{icon('download')} Nyomtatványok letöltése</a>
    </div>
  </div>
</section>

{cta_band(0)}
"""
    return {"path": "szolgaltatasok.html", "active": "szolgaltatasok.html", "body": body,
            "title": "Szolgáltatásaink",
            "description": "A pomázi Szociális Szolgáltatási Központ nyolc szolgáltatása: étkeztetés, "
                           "házi segítségnyújtás, jelzőrendszer, idősek klubja, átmeneti gondozóház, "
                           "családsegítés, iskolavédőnő és betegszállítás."}


def page_service(s):
    d = 1
    sections = "".join(f"<h2>{esc(t)}</h2>{h}" for t, h in s["sections"])

    staff = ""
    if s.get("staff"):
        label, names = s["staff"]
        staff = (f'<h2>{esc(label)}</h2><ul class="checklist">'
                 + "".join(f"<li>{esc(n)}</li>" for n in names) + "</ul>")

    hours = ""
    if s.get("office_hours"):
        rows = "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in s["office_hours"])
        hours = (f'<div class="panel"><p class="panel__title">Ügyfélfogadás</p>'
                 f'<table class="hours"><tbody>{rows}</tbody></table></div>')

    emergency = ""
    if s.get("emergency"):
        items = "".join(f"""
        <div class="note note--urgent">
          {icon('alert')}
          <p><strong>{esc(t)}</strong><br>{esc(desc)}<br>
          <a href="{href}" style="font-size:1.1rem;font-weight:700">{esc(num)}</a></p>
        </div>""" for t, desc, num, href in s["emergency"])
        emergency = f"<h2>Krízishelyzetben, munkaidőn kívül</h2>{items}"

    links = ""
    if s.get("links"):
        items = "".join(
            f'<li><a href="{rel(href, d) if not ext else href}"{link_attrs(href) if ext else ""}>'
            f'{icon("external") if ext else icon("file")}<span>{esc(label)}</span>'
            f'{"<em>külső oldal</em>" if ext else ""}</a></li>'
            for label, href, ext in s["links"])
        links = f'<div class="panel"><p class="panel__title">Kapcsolódó</p><ul class="doclist">{items}</ul></div>'

    fee_cls = "tag--free" if s["fee"] == "Ingyenes" else "tag--fee"
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in s["tags"])

    body = pagehead(s["title"], s["short"],
                    [("Szolgáltatásaink", "szolgaltatasok.html"), (s["nav_title"], None)], d) + f"""
<section class="section">
  <div class="container">
    <figure style="margin:0 0 clamp(2rem,4vw,3rem)">
      <img src="{rel('assets/img/' + s['image'], d)}" alt="{esc(s['image_alt'])}"
           style="width:100%;aspect-ratio:21/8;object-fit:cover;border-radius:var(--radius-l);box-shadow:var(--shadow-m)"
           width="1100" height="825">
    </figure>
    <div class="with-aside">
      <div class="prose">
        <div class="card__meta" style="margin-bottom:1.6rem">
          <span class="tag {fee_cls}">{esc(s['fee'])}</span>
          <span class="tag">{icon('pin')}{esc(s['area'])}</span>
          {tags}
        </div>
        <p class="lead">{s['lead']}</p>
        {sections}
        {staff}
        {emergency}
      </div>
      <aside class="aside">
        {contact_panel(s['contact'], d)}
        {hours}
        {links}
        <div class="panel panel--brand">
          <p class="panel__title">Igényléshez</p>
          <p style="margin-bottom:1rem;font-size:.96rem">A kérelem, a jövedelemnyilatkozat és az
          egészségi állapotra vonatkozó igazolás minden ellátáshoz szükséges.</p>
          <a class="btn btn--primary" href="{rel('dokumentumok.html', d)}" style="width:100%">{icon('download')} Nyomtatványok</a>
        </div>
      </aside>
    </div>
  </div>
</section>

{cta_band(d)}
"""
    return {"path": f"szolgaltatasok/{s['slug']}.html", "active": "szolgaltatasok.html", "body": body,
            "title": s["title"], "description": s["short"]}


def page_etlapok():
    d = 1
    body = pagehead("Étlapok", "A szociális étkeztetés aktuális heti étlapjai.",
                    [("Szolgáltatásaink", "szolgaltatasok.html"),
                     ("Étkeztetés", "szolgaltatasok/etkeztetes.html"), ("Étlapok", None)], d) + f"""
<section class="section">
  <div class="container container--narrow">
    <div class="note note--brand">
      {icon('info')}
      <p>Az aktuális étlapokat munkatársaink hetente frissítik. Ha a lap még nem jelent meg, kérjük,
      érdeklődjön a <a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a> telefonszámon.</p>
    </div>
    <div class="panel" style="margin-top:1.6rem">
      <p class="panel__title">Étkeztetés – elérhetőség</p>
      <div class="dl">
        <div class="dl__row"><span class="dl__ico">{icon('users')}</span><span><span class="dl__k">Kapcsolattartó</span><br><span class="dl__v">Garai Péterné, csoportvezető</span></span></div>
        <div class="dl__row"><span class="dl__ico">{icon('phone')}</span><span><span class="dl__k">Telefon</span><br><span class="dl__v"><a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a></span></span></div>
        <div class="dl__row"><span class="dl__ico">{icon('mail')}</span><span><span class="dl__k">E-mail</span><br><span class="dl__v"><a href="mailto:garai.peterne@szszk.pomaz.hu">garai.peterne@szszk.pomaz.hu</a></span></span></div>
      </div>
    </div>
    <div class="btn-row" style="margin-top:1.6rem">
      <a class="btn btn--ghost" href="{rel('szolgaltatasok/etkeztetes.html', d)}">Vissza az étkeztetéshez</a>
    </div>
  </div>
</section>
"""
    return {"path": "szolgaltatasok/etlapok.html", "active": "szolgaltatasok.html", "body": body,
            "title": "Étlapok", "description": "A pomázi szociális étkeztetés aktuális étlapjai."}


def page_dokumentumok():
    d = 0
    groups = []
    for g in DOC_GROUPS:
        docs = "".join(
            f'<li><a href="{href}"{link_attrs(href)}>{icon("file")}<span>{esc(label)}</span>'
            f'<em>{esc(kind)}</em>{icon("download") if is_external(href) else ""}</a></li>'
            for label, kind, href in g["docs"])
        extra = ""
        if g.get("list"):
            extra = "".join(
                f'<h3 style="margin-top:1.6rem">{esc(k)}</h3><ul class="checklist">'
                + "".join(f"<li>{esc(i)}</li>" for i in v) + "</ul>"
                for k, v in g["list"].items())
        groups.append(f"""
    <section style="margin-bottom:clamp(2.2rem,4vw,3.2rem)">
      <h2>{esc(g['title'])}</h2>
      <p style="color:var(--ink-2)">{esc(g['note'])}</p>
      {f'<ul class="doclist" style="margin-top:1.2rem">{docs}</ul>' if docs else ''}
      {extra}
    </section>""")

    body = pagehead(
        "Ügyintézés és nyomtatványok",
        "Minden dokumentum, amely az ellátások igényléséhez szükséges – letölthető formában.",
        [("Ügyintézés", None)], d) + f"""
<section class="section">
  <div class="container with-aside">
    <div class="prose">
      <div class="note note--brand">
        {icon('info')}
        <p>Ha a nyomtatványok kitöltésében segítségre van szüksége, keresse munkatársainkat
        ügyfélfogadási időben ({esc(SITE['office_hours'])}) a Községház utca 2. szám alatt –
        szívesen segítünk személyesen is.</p>
      </div>
      {''.join(groups)}
    </div>
    <aside class="aside">
      <div class="panel panel--brand">
        <p class="panel__title">Segítünk kitölteni</p>
        <p style="font-size:.96rem">Hívja munkatársainkat, vagy jöjjön be személyesen ügyfélfogadási időben.</p>
        <div class="btn-row" style="margin-top:1rem">
          <a class="btn btn--primary" href="{SITE['phone_href']}" style="width:100%">{icon('phone')} {esc(SITE['phone'])}</a>
        </div>
      </div>
      <div class="panel">
        <p class="panel__title">Kapcsolódó</p>
        <ul class="doclist">
          <li><a href="szolgaltatasok.html">{icon('heart')}<span>Szolgáltatásaink</span></a></li>
          <li><a href="kapcsolat.html">{icon('phone')}<span>Elérhetőségek</span></a></li>
          <li><a href="jogszabalyok.html">{icon('scale')}<span>Alkalmazandó jogszabályok</span></a></li>
        </ul>
      </div>
    </aside>
  </div>
</section>
"""
    return {"path": "dokumentumok.html", "active": "dokumentumok.html", "body": body,
            "title": "Ügyintézés és nyomtatványok",
            "description": "Kérelem, jövedelemnyilatkozat, egészségi állapotra vonatkozó igazolás és "
                           "szolgáltatási rendek a pomázi szociális ellátások igényléséhez."}


def page_hirek():
    d = 0
    items = []
    for n in NEWS:
        img = ""
        if n.get("image"):
            img = (f'<a href="hirek/{n["slug"]}.html" class="news__thumb">'
                   f'<img src="assets/img/hirek/{n["image"]}" alt="{esc(n.get("image_alt",""))}" '
                   f'loading="lazy" width="1100" height="619"></a>')
        badge = ' <span class="tag tag--fee">Fontos</span>' if n.get("highlight") else ""
        items.append(f"""
  <article class="news__item">
    <p class="news__date"><time datetime="{n['date']}">{esc(n['date_hu'])}</time></p>
    <div>
      <h2 class="news__title" style="font-size:1.22rem"><a href="hirek/{n['slug']}.html">{esc(n['title'])}</a></h2>
      <p class="news__excerpt">{esc(n['excerpt'])}</p>
      <p style="margin-top:.6rem"><a class="card__more" href="hirek/{n['slug']}.html">Tovább a hírhez {icon("arrow-right")}</a></p>
      {img}
    </div>
  </article>""")

    body = pagehead("Hírek", "Programok, változások és események az intézmény életéből.",
                    [("Hírek", None)], d) + f"""
<section class="section">
  <div class="container">
    <div class="news">{''.join(items)}</div>
  </div>
</section>
{cta_band(0)}
"""
    return {"path": "hirek.html", "active": "hirek.html", "body": body,
            "title": "Hírek",
            "description": "Aktuális hírek, programok és tájékoztatások a pomázi Szociális Szolgáltatási Központtól."}


def page_news_item(post, index):
    d = 1
    body_html = post["body_html"]
    if not SINGLE_FILE:
        body_html = body_html.replace('src="assets/', 'src="../assets/')
    hero = ""
    if post.get("image"):
        hero = (f'<figure style="margin:0 0 2rem"><img src="{rel("assets/img/hirek/" + post["image"], d)}" '
                f'alt="{esc(post.get("image_alt", ""))}" width="1100" height="619" '
                f'style="width:100%;border-radius:var(--radius-l);box-shadow:var(--shadow-m)"></figure>')

    prev_post = NEWS[index + 1] if index + 1 < len(NEWS) else None
    next_post = NEWS[index - 1] if index > 0 else None
    nav = []
    if next_post:
        nav.append(f'<a class="btn btn--ghost" href="{rel("hirek/" + next_post["slug"] + ".html", d)}">Újabb hír</a>')
    if prev_post:
        nav.append(f'<a class="btn btn--ghost" href="{rel("hirek/" + prev_post["slug"] + ".html", d)}">Korábbi hír</a>')

    badge = '<span class="tag tag--fee">Fontos</span>' if post.get("highlight") else ""
    extra = ""
    if post.get("link"):
        label, href = post["link"]
        extra = (f'<p style="margin-top:2rem"><a class="btn btn--ghost" href="{rel(href, d)}">'
                 f'{esc(label)} {icon("arrow-right")}</a></p>')

    body = pagehead(esc(post["title"]), "", [("Hírek", "hirek.html"), (post["title"], None)], d)
    body = body.replace("</h1>", f'</h1><p class="pagehead__lead"><time datetime="{post["date"]}">'
                                 f'{esc(post["date_hu"])}</time> {badge}</p>')
    body += f"""
<section class="section">
  <div class="container container--narrow">
    {hero}
    <div class="prose post">{body_html}</div>
    {extra}
    <div class="btn-row" style="margin-top:2.5rem">
      <a class="btn btn--ghost" href="{rel('hirek.html', d)}">{icon('arrow-right')} Összes hír</a>
      {''.join(nav)}
    </div>
  </div>
</section>
{cta_band(d)}
"""
    return {"path": f"hirek/{post['slug']}.html", "active": "hirek.html", "body": body,
            "title": post["title"], "description": post["excerpt"][:300]}


def write_feed(posts):
    def item(p):
        link = f"{SITE['url']}/hirek/{p['slug']}.html"
        return (f"    <item>\n      <title>{esc(p['title'])}</title>\n"
                f"      <link>{link}</link>\n      <guid isPermaLink=\"true\">{link}</guid>\n"
                f"      <description>{esc(p['excerpt'])}</description>\n"
                f"      <pubDate>{p['date']}</pubDate>\n    </item>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<rss version="2.0"><channel>\n'
           f"  <title>Szociális Szolgáltatási Központ, Pomáz – Hírek</title>\n"
           f"  <link>{SITE['url']}/hirek.html</link>\n"
           f"  <description>{esc(SITE['description'])}</description>\n"
           "  <language>hu</language>\n"
           + "\n".join(item(p) for p in posts) +
           "\n</channel></rss>\n")
    with open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


# --- Képgaléria: bélyegképek és albumoldalak ------------------------------

GALLERY_SRC = os.path.join(ASSETS, "img", "galeria")
GALLERY_OUT = "assets/img/galeria"
THUMB_SIZE = (640, 480)      # 4:3 bélyegkép a rácshoz
LARGE_MAX = 1600             # a nagy nézet leghosszabb oldala


def _gallery_files(albums):
    names = []
    for a in albums:
        if a["cover"]:
            names.append(a["cover"])
        names.extend(p["file"] for p in a["photos"])
    return sorted(set(names))


def build_gallery_images(albums):
    """A feltöltött fotókból bélyegkép és nagy nézet készítése.

    Pillow nélkül is működik: ilyenkor az eredeti fájlt másoljuk mindkét
    helyre, csak nagyobb lesz a letöltendő méret.
    """
    names = _gallery_files(albums)
    if not names:
        return
    thumb_dir = os.path.join(OUT, "assets", "img", "galeria", "thumb")
    large_dir = os.path.join(OUT, "assets", "img", "galeria", "large")
    os.makedirs(thumb_dir, exist_ok=True)
    os.makedirs(large_dir, exist_ok=True)

    try:
        from PIL import Image, ImageOps
    except ImportError:
        Image = None
        print("  ! A Pillow nincs telepítve — az eredeti méretű képek kerülnek ki.")
        print("    Telepítés:  pip install Pillow")

    made = skipped = 0
    for name in names:
        src = os.path.join(GALLERY_SRC, name)
        if not os.path.isfile(src):
            skipped += 1
            continue
        base = os.path.splitext(name)[0] + ".jpg"
        thumb_path = os.path.join(thumb_dir, base)
        large_path = os.path.join(large_dir, base)
        if Image is None:
            shutil.copy2(src, os.path.join(thumb_dir, name))
            shutil.copy2(src, os.path.join(large_dir, name))
            made += 1
            continue
        try:
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im).convert("RGB")
                thumb = ImageOps.fit(im, THUMB_SIZE, Image.LANCZOS, centering=(0.5, 0.42))
                thumb.save(thumb_path, "JPEG", quality=78, optimize=True, progressive=True)
                large = im.copy()
                large.thumbnail((LARGE_MAX, LARGE_MAX), Image.LANCZOS)
                large.save(large_path, "JPEG", quality=82, optimize=True, progressive=True)
            made += 1
        except Exception as exc:                      # sérült vagy ismeretlen fájl
            print("  ! Nem sikerült feldolgozni: %s (%s)" % (name, exc))
            skipped += 1
    print("  Galéria: %d kép feldolgozva%s." % (made, ", %d kihagyva" % skipped if skipped else ""))


def gallery_asset(name, kind, depth):
    """Egy galériakép útvonala (kind: 'thumb' vagy 'large')."""
    if not name:
        return ""
    jpg = os.path.splitext(name)[0] + ".jpg"
    candidate = f"{GALLERY_OUT}/{kind}/{jpg}"
    if not os.path.isfile(os.path.join(OUT, candidate)):
        candidate = f"{GALLERY_OUT}/{kind}/{name}"
    return rel(candidate, depth)


def album_href(album, depth):
    return rel(f"kepgaleria/{album['slug']}.html", depth)


def page_album(album):
    d = 1
    photos = album["photos"]
    tiles = []
    for i, photo in enumerate(photos, 1):
        caption = photo["caption"] or f"{album['title']} – {album['year']}, {i}. kép"
        tiles.append(
            f'<a class="album__item" href="{gallery_asset(photo["file"], "large", d)}" '
            f'data-caption="{esc(photo["caption"])}">'
            f'<img src="{gallery_asset(photo["file"], "thumb", d)}" alt="{esc(caption)}" '
            f'loading="lazy" width="640" height="480">'
            f'<span class="album__zoom" aria-hidden="true">{icon("image")}</span></a>')

    if photos:
        grid = f'<div class="album" data-lightbox>{"".join(tiles)}</div>'
        note = ""
    else:
        grid = ""
        note = f"""
    <div class="note note--brand">{icon('info')}
      <p>Ebbe az albumba még nem töltöttünk fel képeket. Nézzen vissza hamarosan!</p>
    </div>"""

    outlink = ""

    lead = f"{album['year']} · {len(photos)} kép" if photos else album["year"]
    body = pagehead(esc(album["title"]), lead,
                    [("Képgaléria", "kepgaleria.html"), (album["title"], None)], d) + f"""
<section class="section">
  <div class="container">
    {album['description_html']}
    {note}
    {grid}
    {outlink}
    <div class="btn-row" style="margin-top:2.5rem">
      <a class="btn btn--ghost" href="{rel('kepgaleria.html', d)}">{icon('arrow-right')} Összes album</a>
    </div>
  </div>
</section>
"""
    return {"path": f"kepgaleria/{album['slug']}.html", "active": "kepgaleria.html", "body": body,
            "title": f"{album['title']} – {album['year']}",
            "description": f"Képek a(z) {album['title']} ({album['year']}) albumból – "
                           f"Szociális Szolgáltatási Központ, Pomáz."}


def page_kepgaleria():
    d = 0
    cards = []
    for a in GALLERY:
        href = album_href(a, d)
        count = len(a["photos"])
        meta = f"{count} kép" if count else "hamarosan"
        cards.append(f"""
    <a class="gallery__card" href="{href}">
      <span class="gallery__media"><img src="{gallery_asset(a['cover'], 'thumb', d)}"
        alt="{esc(a['title'])} – {esc(a['year'])}" loading="lazy" width="640" height="480"></span>
      <span class="gallery__label">
        <span class="gallery__name">{esc(a['title'])}</span>
        <span class="gallery__meta">{esc(a['year'])} · {esc(meta)}</span>
      </span>
    </a>""")

    body = pagehead("Képgaléria", "Ünnepeink, kirándulásaink és mindennapjaink képekben.",
                    [("Képgaléria", None)], d) + f"""
<section class="section">
  <div class="container">
    <div class="note note--brand" style="margin-bottom:2rem">
      {icon('info')}
      <p>A gyermekekről az adatvédelmi előírások betartása miatt nem teszünk közzé fényképeket.</p>
    </div>
    <div class="gallery">{''.join(cards)}</div>
  </div>
</section>
{cta_band(0, "Csatlakozzon programjainkhoz!",
   "Az Idősek Klubja tagjainak rendszeresen szervezünk kirándulásokat, majálist, szüreti mulatságot "
   "és ünnepi alkalmakat – a beszállítás kisbusszal ingyenes.")}
"""
    return {"path": "kepgaleria.html", "active": "kepgaleria.html", "body": body,
            "title": "Képgaléria",
            "description": "Képek a pomázi Szociális Szolgáltatási Központ programjairól és ünnepeiről."}


def page_kapcsolat():
    d = 0
    units = "".join(f"""
    <article class="tile">
      <span class="tile__icon">{icon(u['icon'])}</span>
      <h3>{esc(u['name'])}</h3>
      <p>{esc(u['role'])}</p>
      <div class="dl" style="margin-top:1.1rem">
        <div class="dl__row"><span class="dl__ico">{icon('pin')}</span><span><span class="dl__k">Cím</span><br><span class="dl__v">{esc(u['address'])}</span></span></div>
        <div class="dl__row"><span class="dl__ico">{icon('phone')}</span><span><span class="dl__k">Telefon</span><br><span class="dl__v">{phone_list(u['phones'])}</span></span></div>
        <div class="dl__row"><span class="dl__ico">{icon('mail')}</span><span><span class="dl__k">E-mail</span><br><span class="dl__v"><a href="mailto:{u['email']}">{esc(u['email'])}</a></span></span></div>
        <div class="dl__row"><span class="dl__ico">{icon('clock')}</span><span><span class="dl__k">Ügyfélfogadás</span><br><span class="dl__v">{esc(u['hours'])}</span></span></div>
      </div>
    </article>""" for u in CONTACT_UNITS)

    links = "".join(
        f'<li><a href="{href}" target="_blank" rel="noopener">{icon("external")}'
        f'<span>{esc(title)}</span><em>{esc(desc)}</em></a></li>'
        for title, desc, href in USEFUL_LINKS)

    body = pagehead("Kapcsolat", "Minden szervezeti egységünk elérhetősége és ügyfélfogadási rendje.",
                    [("Kapcsolat", None)], d) + f"""
<section class="section">
  <div class="container">
    <div class="panel panel--brand" style="margin-bottom:clamp(2rem,4vw,3rem)">
      <div class="grid grid--3" style="gap:1.4rem">
        <div>
          <p class="panel__title">Központi telefonszám</p>
          <p style="font-size:1.32rem;font-weight:700;margin:0"><a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a></p>
          <p style="margin:.3rem 0 0;color:var(--ink-2)"><a href="{SITE['phone_alt_href']}">{esc(SITE['phone_alt'])}</a></p>
        </div>
        <div>
          <p class="panel__title">E-mail</p>
          <p style="font-size:1.06rem;font-weight:600;margin:0"><a href="mailto:{SITE['email']}">{esc(SITE['email'])}</a></p>
        </div>
        <div>
          <p class="panel__title">Székhely</p>
          <p style="margin:0;font-weight:600">{esc(SITE['address'])}</p>
          <p style="margin:.3rem 0 0;color:var(--ink-2)">Ügyfélfogadás: {esc(SITE['office_hours'])}</p>
        </div>
      </div>
    </div>

    <div class="section__head">
      <span class="eyebrow">Szervezeti egységeink</span>
      <h2>Hol keressen minket?</h2>
    </div>
    <div class="grid grid--2">{units}</div>

    <div class="note note--urgent" style="margin-top:2.4rem">
      {icon('alert')}
      <p><strong>Krízishelyzetben, munkaidőn kívül:</strong>
      Gyermekvédelmi jelzőrendszeri készenléti szolgálat – <a href="tel:+36203640827">+36 20 364 0827</a>
      (munkanapokon 16:00–8:00, hétvégén és munkaszüneti napokon 0–24 órában) ·
      Országos Gyermekvédő Hívószám – <a href="tel:+3680212021">+36 80 21 20 21</a> (ingyenes, 0–24).</p>
    </div>

    <div style="margin-top:clamp(2.2rem,4vw,3rem)">
      <h2>Hasznos weboldalak</h2>
      <ul class="doclist" style="margin-top:1.2rem">{links}</ul>
    </div>
  </div>
</section>
"""
    return {"path": "kapcsolat.html", "active": "kapcsolat.html", "body": body,
            "title": "Kapcsolat",
            "description": "A pomázi Szociális Szolgáltatási Központ és szervezeti egységeinek címe, "
                           "telefonszáma, e-mail címe és ügyfélfogadási rendje."}


def page_jogszabalyok():
    d = 0
    groups = "".join(f"""
    <details class="acc"{' open' if i == 0 else ''}>
      <summary>{esc(title)}</summary>
      <div class="acc__body"><ul>{''.join(f'<li>{esc(x)}</li>' for x in items)}</ul></div>
    </details>""" for i, (title, items) in enumerate(LAW_GROUPS))

    body = pagehead("Alkalmazandó jogszabályok",
                    "Az intézményben folyó tevékenységet döntően az alábbi jogszabályok határozzák meg.",
                    [("Intézményünk", "intezmenyunk.html"), ("Jogszabályok", None)], d) + f"""
<section class="section">
  <div class="container container--narrow">
    {groups}
    <div class="note note--brand" style="margin-top:2rem">
      {icon('info')}
      <p>A jogszabályok hatályos szövege a <a href="https://njt.hu" target="_blank" rel="noopener">Nemzeti
      Jogszabálytárban</a> érhető el.</p>
    </div>
  </div>
</section>
"""
    return {"path": "jogszabalyok.html", "active": "intezmenyunk.html", "body": body,
            "title": "Alkalmazandó jogszabályok",
            "description": "Az intézmény működését meghatározó törvények, kormány- és miniszteri rendeletek."}


def page_allas():
    d = 0
    body = pagehead("Álláslehetőség", "Csatlakozzon csapatunkhoz!", [("Álláslehetőség", None)], d) + f"""
<section class="section">
  <div class="container container--narrow prose">
    <h2>Nyitott pozíciók</h2>
    <div class="tile" style="margin-top:1.2rem">
      <span class="tile__icon">{icon('briefcase')}</span>
      <h3>Gondozó / ápoló</h3>
      <p>Idősek Átmeneti Gondozóháza · 2013 Pomáz, Községház utca 2.</p>
    </div>
    <h2>Jelentkezés</h2>
    <p>A pályázatokat az <a href="mailto:szszk@szszk.pomaz.hu">szszk@szszk.pomaz.hu</a> e-mail címre várjuk.
    Érdeklődni a <a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a> telefonszámon lehet.</p>
    <div class="btn-row" style="margin-top:1.6rem">
      <a class="btn btn--primary" href="mailto:szszk@szszk.pomaz.hu">{icon('mail')} Pályázat küldése</a>
      <a class="btn btn--ghost" href="{SITE['phone_href']}">{icon('phone')} {esc(SITE['phone'])}</a>
    </div>
  </div>
</section>
"""
    return {"path": "allaslehetoseg.html", "active": "intezmenyunk.html", "body": body,
            "title": "Álláslehetőség",
            "description": "Nyitott pozíciók a pomázi Szociális Szolgáltatási Központban."}


def page_kozzeteteli():
    d = 0
    units = "".join(f"""
      <div class="tile">
        <span class="tile__icon">{icon(u['icon'])}</span>
        <h3>{esc(u['name'])}</h3>
        <p>{esc(u['address'])}<br>{phone_list(u['phones'])}<br>
        <a href="mailto:{u['email']}">{esc(u['email'])}</a><br>
        <span style="color:var(--ink-3)">Ügyfélfogadás: {esc(u['hours'])}</span></p>
      </div>""" for u in CONTACT_UNITS)

    leaders = "".join(
        f'<tr><th style="width:auto">{esc(n)}</th><td>{esc(r)}<br>'
        f'<a href="{tel}">{esc(p)}</a> · <a href="mailto:{m}">{esc(m)}</a></td></tr>'
        for n, r, p, tel, m in LEADERS)

    body = pagehead("Általános közzétételi lista",
                    "Az információs önrendelkezési jogról és az információszabadságról szóló törvény "
                    "szerinti közérdekű adatok.",
                    [("Intézményünk", "intezmenyunk.html"), ("Közzétételi lista", None)], d) + f"""
<section class="section">
  <div class="container">
    <details class="acc" open>
      <summary>I. Szervezeti, személyzeti adatok</summary>
      <div class="acc__body prose">
        <h3>1. Elérhetőségi adatok</h3>
        <p><strong>Szociális Szolgáltatási Központ</strong><br>
        Székhely: {esc(SITE['address'])}<br>
        Telefon: <a href="{SITE['phone_alt_href']}">{esc(SITE['phone_alt'])}</a> ·
        <a href="{SITE['phone_href']}">{esc(SITE['phone'])}</a><br>
        E-mail: <a href="mailto:{SITE['email']}">{esc(SITE['email'])}</a><br>
        Honlap: <a href="{SITE['url']}">{esc(SITE['url'])}</a></p>

        <h3>2. Szervezeti egységek elérhetőségei</h3>
        <div class="grid grid--2" style="margin-top:1.2rem">{units}</div>

        <h3 style="margin-top:2rem">3. Vezetők és ügyfélkapcsolat</h3>
        <table class="hours"><tbody>{leaders}</tbody></table>

        <h3 style="margin-top:2rem">4. Egyéb</h3>
        <ul>
          <li>Felügyelt költségvetési szervek: <strong>nemleges</strong></li>
          <li>Gazdálkodó szervezetek: <strong>nemleges</strong></li>
          <li>Közalapítványok: <strong>nemleges</strong></li>
        </ul>
      </div>
    </details>

    <details class="acc">
      <summary>II. Tevékenységre, működésre vonatkozó adatok</summary>
      <div class="acc__body prose">
        <p>Az intézmény integrált szociális intézmény, amely alap- és szakellátásokat végez Pomáz és
        Csobánka településeken. Szervezeti felépítését és szolgáltatásait az
        <a href="intezmenyunk.html">Intézményünk</a>, illetve a
        <a href="szolgaltatasok.html">Szolgáltatásaink</a> oldalon részletezzük.</p>
        <p>A működést meghatározó jogszabályok felsorolása az
        <a href="jogszabalyok.html">Alkalmazandó jogszabályok</a> oldalon található.</p>
        <p>A szolgáltatási rendek és a térítési díjakról szóló tájékoztató az
        <a href="dokumentumok.html">Ügyintézés</a> oldalról tölthető le.</p>
      </div>
    </details>

    <details class="acc">
      <summary>III. Gazdálkodási adatok</summary>
      <div class="acc__body prose">
        <p>Fenntartó: <strong>Pomáz Város Önkormányzata</strong> (2013 Pomáz, Kossuth Lajos u. 23–25.,
        <a href="tel:+3626814300">+36 26 814 300</a>,
        <a href="mailto:pomaz@pomaz.hu">pomaz@pomaz.hu</a>,
        <a href="https://pomaz.hu" target="_blank" rel="noopener">pomaz.hu</a>).</p>
        <p>Felügyeleti szerv: <strong>Pest Vármegyei Kormányhivatal</strong>
        (<a href="https://kormanyhivatalok.hu/kormanyhivatalok/pest" target="_blank" rel="noopener">kormanyhivatalok.hu</a>).</p>
        <p>A térítési díjakat Pomáz Város Önkormányzata rendeletben szabályozza:
        <a href="https://or.njt.hu/eli/731058/r/2024/6" target="_blank" rel="noopener">a hatályos szociális rendelet</a>.</p>
      </div>
    </details>
  </div>
</section>
"""
    return {"path": "kozzeteteli-lista.html", "active": "intezmenyunk.html", "body": body,
            "title": "Általános közzétételi lista",
            "description": "A pomázi Szociális Szolgáltatási Központ közérdekű adatai: elérhetőségek, "
                           "vezetők, fenntartó és gazdálkodási adatok."}


def all_pages():
    pages = [page_index(), page_intezmenyunk(), page_szolgaltatasok()]
    pages += [page_service(s) for s in SERVICES]
    pages += [page_etlapok(), page_dokumentumok(), page_hirek(), page_kepgaleria(),
              page_kapcsolat(), page_jogszabalyok(), page_allas(), page_kozzeteteli()]
    pages += [page_news_item(p, i) for i, p in enumerate(NEWS)]
    pages += [page_album(a) for a in GALLERY]
    return pages


# =============================================================================
# Kiírás
# =============================================================================

def git_repo_slug():
    """A GitHub-tároló azonosítója (tulajdonos/név).

    GitHub Actions alatt a GITHUB_REPOSITORY környezeti változóból, helyben a
    git távoli címéből olvassuk ki.
    """
    env = os.environ.get("GITHUB_REPOSITORY")
    if env and "/" in env:
        return env
    try:
        import subprocess
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                             capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        return None
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return m.group(1) if m else None


def _fill_repo(config_path):
    """A tartalomkezelő config.yml-jében kitölti a tároló nevét."""
    if not os.path.isfile(config_path):
        return
    text = open(config_path, encoding="utf-8").read()
    if "__REPO__" not in text:
        return
    slug = git_repo_slug()
    if slug:
        open(config_path, "w", encoding="utf-8").write(text.replace("__REPO__", slug))
    else:
        print("  ! A tartalomkezelő tárolóneve még nincs kitöltve (nincs git origin).")
        print("    Állítsd be: git remote add origin git@github.com:FELHASZNALO/TAROLO.git")


def copy_assets():
    """A forrás assets/ és a szerkesztőfelület átmásolása a kimenetbe."""
    dest = os.path.join(OUT, "assets")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    # A galéria eredeti (nagy) fájljai nem kerülnek ki: helyettük a build
    # bélyegképet és webre méretezett nagy nézetet állít elő.
    shutil.copytree(ASSETS, dest, ignore=shutil.ignore_patterns("galeria"))
    if os.path.isdir(ADMIN):
        admin_dest = os.path.join(OUT, "admin")
        if os.path.isdir(admin_dest):
            shutil.rmtree(admin_dest)
        shutil.copytree(ADMIN, admin_dest)
        _fill_repo(os.path.join(admin_dest, "config.yml"))
    cname = os.path.join(ROOT, "CNAME")
    if os.path.isfile(cname):
        shutil.copy2(cname, os.path.join(OUT, "CNAME"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()


def clean_output(pages):
    """A már nem generált HTML-fájlok törlése a kimenetből.

    Enélkül egy átnevezett vagy törölt hír/album régi oldala kint maradna.
    """
    keep = {os.path.normpath(os.path.join(OUT, p["path"])) for p in pages}
    keep.add(os.path.normpath(os.path.join(OUT, "admin", "index.html")))
    removed = 0
    for root, _dirs, files in os.walk(OUT):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.normpath(os.path.join(root, name))
            if path not in keep:
                os.remove(path)
                removed += 1
    if removed:
        print("  %d elavult oldal törölve a kimenetből." % removed)


def write_multipage(pages):
    os.makedirs(OUT, exist_ok=True)
    copy_assets()
    clean_output(pages)
    build_gallery_images(GALLERY)
    for p in pages:
        dest = os.path.join(OUT, p["path"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(layout(p))
    # robots + sitemap
    urls = "".join(f"  <url><loc>{SITE['url']}/{p['path']}</loc></url>\n" for p in pages)
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    write_feed(NEWS)
    print(f"✓ {len(pages)} oldal elkészült: {OUT}")
    for p in pages:
        print("   ", p["path"])


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii")


def write_singlefile(pages):
    os.makedirs(OUT, exist_ok=True)
    build_gallery_images(GALLERY)          # a bélyegképeknek meg kell lenniük
    css = open(os.path.join(ASSETS, "style.css"), encoding="utf-8").read()
    js = open(os.path.join(ASSETS, "app.js"), encoding="utf-8").read()

    routes = []
    for p in pages:
        active = ' data-active-nav="%s"' % (p.get("active") or "")
        routes.append(f'<div class="route" data-route="{p["path"]}"{active} hidden>\n{p["body"]}\n</div>')
    doc = "\n".join(routes)

    # Képek beágyazása — minden kép pontosan egyszer, futásidőben behelyettesítve,
    # hogy a többször felhasznált fotók ne duplikálódjanak a fájlban.
    cache = {}
    def repl(m):
        name = m.group(1)
        if name not in cache:
            # A galéria bélyegképei a kimenetben készülnek, a többi kép a forrásban van.
            generated = os.path.join(OUT, "assets", "img", name)
            source = os.path.join(ASSETS, "img", name)
            cache[name] = data_uri(generated if os.path.isfile(generated) else source)
        return 'data-img="%s" src="data:image/svg+xml,%%3Csvg xmlns=\'http://www.w3.org/2000/svg\'/%%3E"' % name
    doc = re.sub(r'src="assets/img/([^"]+)"', repl, doc)
    img_map = "{" + ",".join('"%s":"%s"' % (k, v) for k, v in cache.items()) + "}"
    img_script = ("var IMG=" + img_map + ";"
                  "document.querySelectorAll('img[data-img]').forEach(function(i){i.src=IMG[i.dataset.img];});")

    header = utility_bar(0) + masthead(0, None)
    foot = footer(0)

    router = """
(function(){
  var routes = {};
  document.querySelectorAll('.route').forEach(function(r){ routes[r.dataset.route] = r; });
  var titles = {};
  function show(name, push){
    if(!routes[name]) name = 'index.html';
    Object.keys(routes).forEach(function(k){ routes[k].hidden = (k !== name); });
    var active = routes[name].dataset.activeNav || '';
    document.querySelectorAll('.nav__link, .nav__cta').forEach(function(a){
      var href = a.getAttribute('href');
      if(href === active && active) a.setAttribute('aria-current','page');
      else a.removeAttribute('aria-current');
    });
    if(push) history.replaceState(null, '', '#' + name);
    window.scrollTo({top:0, behavior:'auto'});
    var nav = document.getElementById('fomenu');
    if(nav && nav.dataset.open === 'true'){ nav.dataset.open='false'; document.body.style.overflow=''; }
    var scrim = document.querySelector('[data-nav-scrim]'); if(scrim) scrim.dataset.open='false';
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href]');
    if(!a) return;
    var href = a.getAttribute('href');
    if(!href || /^(https?:|mailto:|tel:)/.test(href)) return;
    if(href.charAt(0) === '#'){
      var el = document.getElementById(href.slice(1));
      if(el){ e.preventDefault(); el.scrollIntoView({behavior:'smooth'}); }
      return;
    }
    var base = href.split('#')[0];
    if(routes[base]){
      e.preventDefault();
      show(base, true);
      var hash = href.split('#')[1];
      if(hash){ var t = document.getElementById(hash); if(t) t.scrollIntoView(); }
    }
  });
  show((location.hash || '').replace('#','') || 'index.html', false);
})();
"""

    out = f"""<title>Szociális Szolgáltatási Központ Pomáz</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<style>
{css}
.route[hidden] {{ display: none !important; }}
</style>
<a class="skip-link" href="#tartalom">Ugrás a tartalomra</a>
{header}
<main id="tartalom">
{doc}
</main>
{foot}
<script>
{img_script}
{js}
{router}
</script>
"""
    dest = os.path.join(ROOT, "artifact.html")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"✓ Egyfájlos előnézet: {dest} ({round(len(out.encode('utf-8'))/1024)} kB)")


if __name__ == "__main__":
    pages = all_pages()
    if SINGLE_FILE:
        write_singlefile(pages)
    else:
        write_multipage(pages)
