# Szociális Szolgáltatási Központ, Pomáz — honlap

A [pomazszszk.hu](https://pomazszszk.hu) tartalmának újratervezett változata.
Statikus honlap: nincs WordPress, PHP vagy adatbázis — a forrásból egy Python
szkript generálja, a GitHub pedig automatikusan közzéteszi.

---

## Mappaszerkezet

```
content/hirek/*.md       ← A HÍREK. Egy fájl = egy hír. Ezt szerkeszti a CMS is.
content/galeria/*.md     ← A KÉPGALÉRIA ALBUMAI. Egy fájl = egy album.
content/adatok/*.json    ← ELÉRHETŐSÉGEK, MUNKATÁRSAK, NYOMTATVÁNYOK (CMS-ből)
assets/                  ← Képek, stíluslap, JavaScript (forrás)
  img/hirek/             ← A hírekhez feltöltött képek helye
  img/galeria/           ← A galéria eredeti fényképei (a build kicsinyíti)
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

A `highlight: true` jelölésű hírek **„Fontos” címkét kapnak, és a hírlista,
illetve a főoldal legelejére kerülnek**, a dátumuktól függetlenül. Ha már nem
aktuális, elég a jelölést levenni, és visszasorolódik a dátuma szerinti helyre.

---

## Képgaléria

Egy album egy Markdown-fájl a `content/galeria/` mappában:

```markdown
---
title: Adventi délután
year: 2026
date: 2026-12-05
cover: advent-01.jpg
photos:
  - /assets/img/galeria/advent-01.jpg
  - /assets/img/galeria/advent-02.jpg
  - /assets/img/galeria/advent-03.jpg
---
```

- **`photos`** — a fényképek listája. A tartalomkezelőben **egyszerre több képet
  is kijelölhetsz és feltölthetsz**: a fájlválasztóban `Ctrl+A`-val az összeset,
  `Shift`-tel egy tartományt, vagy egyszerűen rá is húzhatod a képeket a mezőre.
- **`cover`** — a galéria főoldalán látszó borító. Ha üres, az első fénykép lesz az.
- Minden fénykép automatikus szöveges leírást kap („Adventi délután – 2026, 3. kép”),
  hogy a felolvasóprogramok is használni tudják.

**A képek méretezése automatikus.** Az eredeti fájlok az `assets/img/galeria/`
mappában maradnak (akár telefonnal készült, több megabájtos fotók), a build
pedig két méretet gyárt belőlük a kimenetbe:

| | méret | mire jó |
|---|---|---|
| `thumb/` | 640 × 480 | a rácsban látható bélyegkép |
| `large/` | max. 1600 px | a nagyított nézet |

Az eredeti, nagy fájlok **nem kerülnek ki** a honlapra, tehát a látogató sosem
tölt le feleslegesen sok adatot. Ehhez a `Pillow` csomag kell; a GitHub Action
telepíti. Helyben enélkül is lefut a build, csak akkor az eredeti méretű képek
kerülnek ki (a `pip install Pillow` megoldja).

Minden album kap saját oldalt (`/kepgaleria/advent-delutan.html`), rajta
**nagyítható képnézegetővel**: kattintás/koppintás nagyít, a nyílbillentyűk és az
ujjal húzás lapoz, az `Esc` bezár.

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

## Mit lehet a tartalomkezelőből szerkeszteni?

A CMS-ben három csoport található:

**Hírek** és **Képgaléria** — új bejegyzés, album, képfeltöltés.

**Adatok** — négy űrlap, amely az egész honlapot érinti:

| Űrlap | Mit állít | Hol jelenik meg |
|---|---|---|
| **Elérhetőségek és nyitvatartás** | székhely, telefonszámok, e-mail, ügyfélfogadás, és az öt szervezeti egység összes adata | fejléc, lábléc, Kapcsolat oldal, közzétételi lista, mobilmenü |
| **Munkatársak** | vezetők és ügyfélkapcsolati kollégák neve, beosztása, telefonja, e-mailje | Intézményünk oldal, közzétételi lista |
| **Szolgáltatások kapcsolattartói** | a nyolc szolgáltatás aloldalán az oldalsávban látható elérhetőségi doboz | szolgáltatás-aloldalak |
| **Nyomtatványok** | az Ügyintézés oldal letölthető dokumentumai, csoportokba rendezve | Ügyintézés oldal |

A telefonszámokat elég egyszerűen beírni (`+36 20 234 8004`) — a hívható
`tel:` hivatkozást a build automatikusan előállítja belőlük.

Ezek az adatok `content/adatok/*.json` fájlokban élnek. Azért JSON és nem YAML,
mert a hosszabb szövegeket a szerkesztő többsoros blokként írná ki, amit a
projekt saját, függőségmentes értelmezője félreolvasna; JSON-nál ez a kockázat
nem áll fenn.

> A `src/checklinks.py` minden buildnél ellenőrzi, hogy a `config.yml` érvényes
> YAML-e és minden hivatkozott adatfájl létezik-e. Egy elrontott beállítás így
> nem juthat élesbe — a GitHub Action megbukik előtte.

## Biztonság — miért nem rés a tartalomkezelő?

Az `/admin/` oldal **statikus HTML és JavaScript, nem tartalmaz jelszót vagy
kulcsot.** A `config.yml` nyilvánosan olvasható, de csak a tároló nevét és a
mezők szerkezetét írja le — a tároló amúgy is publikus.

Az írás joga nem az oldalon múlik, hanem a GitHubon:

- A böngésző közvetlenül a GitHub API-val beszél; **nincs köztes kiszolgáló,
  amit meg lehetne támadni**, és nincs bejelentkezési végpont, amit lehetne
  törni. Ebben lényegesen kevésbé támadható, mint egy WordPress-adminfelület.
- Írni csak az tud, akinek **érvényes GitHub-tokenje és a tárolóhoz írási joga**
  van. Aki csak megnyitja az `/admin/` oldalt, semmit nem lát és semmit nem tehet.
- A CMS scriptje **verzióra rögzítve és SRI-ellenőrzéssel** (`integrity`) töltődik
  be: ha a CDN-en a fájl bármit változna, a böngésző nem futtatja le.

Amire viszont **érdemes figyelni**: a token a böngésző tárolójában marad. Ezért
ne klasszikus (`repo` jogú) tokent használj, hanem **fine-grained tokent**, amely
csak erre az egy tárolóra érvényes:

> GitHub → Settings → Developer settings → Personal access tokens →
> **Fine-grained tokens** → Generate new token → *Repository access:* **Only
> select repositories** → `pomazszszk` → *Permissions:* **Contents: Read and
> write** → lejárat: 90 nap.

Így ha a token mégis kikerülne, csak ezt az egy — amúgy is nyilvános — tárolót
érinti, és a lejárattal magától érvénytelenné válik.

## Akadálymentesség

Az idős látogatókra tervezve:

- **Betűméret-váltó** a fejlécben (alap / nagyobb / legnagyobb), böngészőben megjegyezve.
- **Nagy kontrasztú mód** (fekete-fehér, árnyék nélkül) a gyengénlátóknak.
- A honlap szándékosan **csak világos módban** jelenik meg, a rendszer sötét
  beállítása mellett is — így a megjelenés mindenkinél azonos és kiszámítható.
- Kb. 17 px-es alap betűméret, 1.68-as sorköz, nagy kattintható felületek.
- „Ugrás a tartalomra” link, látható fókuszjelölés, morzsamenü, teljes
  billentyűzetes kezelhetőség.
- Kattintható telefonszámok (`tel:`) és e-mail címek.
- A stíluslap és a szkript tartalom-lenyomatos verziószámot kap (`?v=...`),
  így egy frissítés után a böngésző soha nem párosít friss HTML-t régi,
  gyorsítótárazott stíluslappal.
- A képnézegető billentyűzetről is kezelhető (nyilak, `Esc`), a fókusz nem
  szökik ki belőle, és minden fényképnek van szöveges leírása.
- Mobilbarát: 320 px-től felfelé egyetlen oldalon sincs vízszintes görgetés
  (méréssel ellenőrizve). Telefonon a felső zöld sáv elrejtőzik, tartalma – az
  elérhetőség és a megjelenítési beállítások – a menüfiók aljára kerül.
  A táblázatok egymás alá rendeződnek, a gombok legalább 44 px-esek.
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
