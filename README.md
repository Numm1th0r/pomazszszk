# Szociális Szolgáltatási Központ, Pomáz — honlap

A [pomazszszk.hu](https://pomazszszk.hu) tartalmának újratervezett változata.
Statikus honlap: nincs WordPress, PHP vagy adatbázis — a forrásból egy Python
szkript generálja, a GitHub pedig automatikusan közzéteszi.

---

## Mappaszerkezet

```
content/hirek/*.md       ← A HÍREK. Egy fájl = egy hír. Ezt szerkeszti a CMS is.
assets/                  ← Képek, stíluslap, JavaScript (forrás)
  img/hirek/             ← A hírekhez feltöltött képek helye
src/
  content.py             Minden állandó szöveg és adat (szolgáltatások, elérhetőségek…)
  build.py               Az oldalgenerátor
  markdown_mini.py       Markdown → HTML, külső könyvtár nélkül
  checklinks.py          Belső hivatkozások ellenőrzése
  icons.py               SVG ikonkészlet
  admin/                 A tartalomkezelő felület (Sveltia CMS)
.github/workflows/       A GitHub Action, ami építi és közzéteszi a honlapot

site/                    ← GENERÁLT KIMENET. Nincs verziókövetve, ne szerkeszd!
artifact.html            ← Egyfájlos előnézet (nincs verziókövetve)
```

## Építés helyben

```bash
python3 src/build.py              # legenerálja a site/ mappát
python3 src/checklinks.py         # ellenőrzi a belső hivatkozásokat
python3 src/build.py --artifact   # egyfájlos előnézet (minden oldal + kép egyben)
```

Csak Python 3 kell hozzá, semmilyen csomag nem szükséges.
Megnézni: nyisd meg a `site/index.html` fájlt böngészőben, vagy futtasd:

```bash
python3 -m http.server -d site 8000     # → http://localhost:8000
```

---

## Hír írása

Egy hír egy Markdown-fájl a `content/hirek/` mappában, `ÉÉÉÉ-HH-NN-cim.md`
névvel:

```markdown
---
title: Adventi készülődés a klubban
date: 2026-12-01
excerpt: Az első gyertya meggyújtása után közösen készítettük el az idei koszorúkat.
image: advent-2026.jpg
image_alt: Adventi koszorúk az asztalon
highlight: false
link_label: Képek a galériában
link_href: kepgaleria.html
---

Itt jön a hír szövege. Lehet **félkövér**, *dőlt*, [hivatkozás](https://pomaz.hu),
felsorolás és alcím is.

## Alcím

- első pont
- második pont
```

A `title` és a `date` kötelező, a többi mező elhagyható. A képek a
`assets/img/hirek/` mappába kerülnek, a fejlécben csak a fájlnevet kell megadni.

Minden hír kap saját oldalt (`/hirek/adventi-keszulodes.html`), bekerül a
hírlistába, a főoldal legfrissebb négy híre közé és az RSS-be (`/feed.xml`).

---

## 1. Közzététel — már be van állítva

| | |
|---|---|
| **Tároló** | https://github.com/Numm1th0r/pomazszszk (publikus) |
| **Honlap** | **https://numm1th0r.github.io/pomazszszk/** |
| **Tartalomkezelő** | https://numm1th0r.github.io/pomazszszk/admin/ |
| **RSS** | https://numm1th0r.github.io/pomazszszk/feed.xml |

A GitHub Pages forrása **GitHub Actions**. Minden `main`-re érkező módosítás után
a `.github/workflows/deploy.yml` lefuttatja a buildet, ellenőrzi a belső
hivatkozásokat, és közzéteszi az eredményt — nagyjából egy perc az egész.

Ha valami elromlik, a hivatkozás-ellenőrző megbuktatja a futást, és **a régi
honlap marad kint** — törött oldal nem kerül élesbe.

```bash
git add -A && git commit -m "Változtatás leírása" && git push
```

### Saját domain (pomazszszk.hu)

Hozz létre a tároló gyökerében egy `CNAME` nevű fájlt egyetlen sorral:

```
pomazszszk.hu
```

A build automatikusan bemásolja a kimenetbe. A domain DNS-ében a GitHub Pages
A/AAAA rekordjait (vagy `www` esetén CNAME-et) kell beállítani a
Settings → Pages oldalon látható útmutató szerint. Amíg ez nincs meg, a honlap
a fenti `github.io` címen érhető el.

## 2. Tartalomkezelő (CMS) beállítása

A `src/admin/` mappában **Sveltia CMS** van előkészítve. Ez a Decap CMS modern
újraírása, ugyanazt a `config.yml`-t használja — azért ezt választottuk, mert
**GitHub Pages-en OAuth-kiszolgáló nélkül is be lehet vele lépni.** (Az eredeti
Decap CMS GitHub-belépéshez külön OAuth-szolgáltatást kellene üzemeltetni.)

A `config.yml`-ben a tároló neve automatikusan kitöltődik (`Numm1th0r/pomazszszk`),
a GitHub Action a `GITHUB_REPOSITORY` változóból, helyben pedig a `git remote`-ból
olvassa ki.

### Belépés — legegyszerűbb út (személyes kulcs)

1. Nyisd meg: **https://numm1th0r.github.io/pomazszszk/admin/**
2. Kattints a **„Sign In with Token”** gombra.
3. A megjelenő ablakban lévő linken hozz létre egy GitHub *personal access
   token*-t (a jogosultságok előre ki vannak választva), másold be, kész.

A kulcs a böngésző tárolójában marad, tehát gépenként/emberenként egyszer kell
megadni. Ez 1–3 szerkesztőnek tökéletes, és semmilyen külön szolgáltatást nem
igényel.

### Belépés — „rendes” GitHub-bejelentkezés (több szerkesztőnek)

Ha jelszavas GitHub-belépést szeretnél gombnyomásra, egy kis OAuth-átjárót kell
telepíteni (ingyenes Cloudflare Workers fiókkal, kb. 15 perc):
[sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth). Utána a
`src/admin/config.yml`-be a `backend:` alá bekerül egy sor:

```yaml
  base_url: https://a-te-workered.workers.dev
```

### Mit tud a felület

- **Hírek** listázása, új hír írása, szerkesztése, törlése.
- Szövegszerkesztő (félkövér, dőlt, lista, alcím, link) — nem kell Markdownt tanulni.
- Képfeltöltés: a kép a `assets/img/hirek/` mappába kerül, a hivatkozás magától jó lesz.
- Mentéskor a CMS commitol a tárolóba → a GitHub Action újraépíti a honlapot →
  **1–2 percen belül élesben van.**

A mezők (cím, dátum, kivonat, borítókép, kiemelés, gomb) magyar felirattal és
súgószöveggel vannak beállítva a `src/admin/config.yml`-ben; ott bővíthetők.

> Az `/admin/` oldal `noindex`-szel van jelölve, a keresők nem indexelik.
> A tartalom írásához mindig GitHub-fiók és a tárolóhoz írási jog kell.

---

## Akadálymentesség

Az idős látogatókra tervezve:

- **Betűméret-váltó** a fejlécben (alap / nagyobb / legnagyobb), böngészőben megjegyezve.
- **Nagy kontrasztú mód** és **sötét mód**, a rendszerbeállítás automatikus követésével.
- Kb. 17 px-es alap betűméret, 1.68-as sorköz, nagy kattintható felületek.
- „Ugrás a tartalomra” link, látható fókuszjelölés, morzsamenü, teljes
  billentyűzetes kezelhetőség.
- Kattintható telefonszámok (`tel:`) és e-mail címek.
- Nyomtatási stíluslap: a menük eltűnnek, a linkek URL-je kiíródik.

## Amit a régi tartalomhoz képest javítottam

- A „Fenntartó” oldalon a `pomaz.hu` hivatkozás valójában a tatai kistérség
  oldalára mutatott — javítva.
- A Család- és Gyermekjóléti Szolgálat e-mail címe több helyen a 2025. szeptember
  1-jén megszűnt régi cím volt; mindenhol az új `csaladsegito@szszk.pomaz.hu` szerepel.
- A közzétételi listában az Idősek Klubja e-mail címe elgépelt volt — a
  csoportvezető hivatalos címére cserélve.
- A telefonszámok egységes, hívható formátumban szerepelnek.

## Képek

Saját fotók: az intézmény épülete, a kisbusz és a képgaléria borítóképei a
jelenlegi honlapról. Illusztrációk: [Unsplash](https://unsplash.com) (szabad
licenc). Ha van saját fotó egy szolgáltatásról, elég azonos néven felülírni a
fájlt az `assets/img/` mappában.
