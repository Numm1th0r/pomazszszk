# -*- coding: utf-8 -*-
"""
Tartalom — Szociális Szolgáltatási Központ, Pomáz.

Minden szöveg és adat forrása a pomazszszk.hu jelenlegi tartalma.
A tartalom szerkesztéséhez elég ezt a fájlt módosítani, majd újra
lefuttatni a build.py-t.
"""

import os
import re

from markdown_mini import plain_text, render, split_front_matter

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = {
    "name": "Szociális Szolgáltatási Központ",
    "place": "Pomáz",
    "tagline": "Pomáz és Csobánka szociális ellátásai egy helyen",
    "description": "A pomázi Szociális Szolgáltatási Központ étkeztetést, házi segítségnyújtást, "
                   "jelzőrendszeres segítséget, idősek klubját, átmeneti gondozóházat, család- és "
                   "gyermekjóléti szolgálatot, valamint iskolavédőnői ellátást biztosít Pomáz és Csobánka lakóinak.",
    "address": "2013 Pomáz, Községház utca 2.",
    "phone": "+36 20 234 8004",
    "phone_href": "tel:+36202348004",
    "phone_alt": "+36 26 525 274",
    "phone_alt_href": "tel:+3626525274",
    "email": "szszk@szszk.pomaz.hu",
    "office_hours": "hétfő–péntek 8:30–15:00",
    "director": "dr. Király Eszter",
    "url": "https://pomazszszk.hu",
}

# --- Főmenü ---------------------------------------------------------------
NAV = [
    ("Intézményünk", "intezmenyunk.html"),
    ("Szolgáltatásaink", "szolgaltatasok.html"),
    ("Ügyintézés", "dokumentumok.html"),
    ("Hírek", "hirek.html"),
    ("Képgaléria", "kepgaleria.html"),
]
NAV_CTA = ("Kapcsolat", "kapcsolat.html")

# --- Szolgáltatások -------------------------------------------------------
# Mezők: slug, title, short, icon, image, fee, area, tags, lead, sections, contact
SERVICES = [
    {
        "slug": "etkeztetes",
        "title": "Szociális étkeztetés",
        "nav_title": "Étkeztetés",
        "short": "Napi egyszeri meleg ebéd helyben, elvitelre vagy házhoz szállítva – hétköznap és hétvégén is.",
        "icon": "soup",
        "image": "szolg-etkeztetes.jpg",
        "image_alt": "Gőzölgő zöldségleves egy fehér tálban, terített asztalon",
        "fee": "Térítési díj ellenében",
        "area": "Pomáz, Csobánka",
        "tags": ["Hétvégén is", "Házhoz szállítással", "Kb. 75 fő évente"],
        "lead": "Az étkeztetés keretében azoknak a szociálisan rászorulóknak biztosítjuk a napi egyszeri "
                "meleg étkezést, akik erről önmaguk – vagy önmaguk és eltartottjaik számára – tartósan "
                "vagy átmenetileg nem tudnak gondoskodni.",
        "sections": [
            ("Kinek szól?",
             "<p>Étkezést különösen azoknak biztosítunk, akik <strong>koruk, egészségi állapotuk, "
             "fogyatékosságuk, pszichiátriai vagy szenvedélybetegségük, illetve hajléktalanságuk miatt "
             "szociálisan rászorultak</strong>. A rászorultság feltételeit Pomáz Város Önkormányzata "
             "rendeletben határozza meg.</p>"),
            ("Hogyan kérheti?",
             "<p>Az ellátás igénybevétele önkéntes: az ellátást igénylő vagy törvényes képviselője "
             "szóbeli vagy írásbeli kérelmére indul. Az ebédet <strong>helyben elfogyaszthatja, "
             "elviheti, de a házhoz szállítást is vállaljuk.</strong> Az étkezés munkanapokon és "
             "hétvégén egyaránt igénybe vehető. Éves szinten átlagosan 75 fő étkeztetését látjuk el "
             "Pomázon és Csobánkán.</p>"),
            ("Egy kis történet",
             "<p>Az étkeztetés több évtizedes múltra tekint vissza városunkban. A hetvenes évektől a "
             "napközi ellátás keretében volt igénybe vehető – akkor még reggeli, ebéd és uzsonna is "
             "kérhető volt. A 2000-es évek elejétől az étkeztetés önálló ellátási formaként jelent meg "
             "a szociális ellátások rendszerében, így már nemcsak az időskorúak, hanem minden "
             "szociálisan rászorult számára elérhetővé vált.</p>"),
        ],
        "links": [
            ("Aktuális étlapjaink", "szolgaltatasok/etlapok.html", False),
            ("Térítési díjak – önkormányzati rendelet", "https://or.njt.hu/eli/731058/r/2024/6", True),
        ],
        "contact": {
            "person": "Garai Péterné, csoportvezető",
            "address": "2013 Pomáz, Községház utca 2.",
            "phones": [("+36 20 234 8004", "tel:+36202348004")],
            "email": "garai.peterne@szszk.pomaz.hu",
        },
    },
    {
        "slug": "hazi-segitsegnyujtas",
        "title": "Házi segítségnyújtás",
        "nav_title": "Házi segítségnyújtás",
        "short": "Gondozónőink az ellátott saját otthonában segítenek – ápolásban, háztartásban, ügyintézésben.",
        "icon": "home-heart",
        "image": "szolg-hazi-segitseg.jpg",
        "image_alt": "Gondozónő segít egy idős asszonynak a nappaliban",
        "fee": "Térítési díj ellenében",
        "area": "Pomáz, Csobánka",
        "tags": ["5 gondozónő", "32 ellátott", "Napi max. 4 óra"],
        "lead": "A házi segítségnyújtás keretében a szolgáltatást igénybe vevő <strong>saját "
                "lakókörnyezetében</strong> biztosítjuk mindazt az ellátást, amely az önálló életvitel "
                "fenntartásához szükséges.",
        "sections": [
            ("Miben segítünk?",
             "<ul class=\"checklist\">"
             "<li>Alapvető gondozási és ápolási feladatok elvégzése.</li>"
             "<li>Segítség a napi élelem biztosításában: bevásárlás, ebédszállítás, szükség esetén az "
             "étkezés segítése.</li>"
             "<li>A lakókörnyezet – konyha, fürdőszoba – rendben tartása, a higiénés körülmények megőrzése.</li>"
             "<li>Ágyban fekvő ellátott esetén kiemelt figyelem a személyi tisztálkodásra, az ágynemű "
             "tisztaságára és az egészségügyi gondozásra.</li>"
             "<li>Mentális gondozás, beszélgetés, a külvilággal való kapcsolattartás támogatása.</li>"
             "<li>Segítség a szociális ügyek intézésében.</li>"
             "<li>Veszélyhelyzetek megelőzése és elhárítása.</li>"
             "</ul>"),
            ("Hogyan indul az ellátás?",
             "<p>Az igénybevétel önkéntes, szóbeli vagy írásbeli kérelemre indul. Az ellátás megkezdése "
             "előtt <strong>gondozási szükségletvizsgálatot</strong> végzünk, amely alapján megállapítható "
             "a napi gondozási szükséglet időtartama – ez legfeljebb napi 4 óra lehet. Az ellátás "
             "megszervezésénél igazodunk az igénybe vevő személyes kéréseihez is.</p>"
             "<p>A szolgáltatást 5 gondozónővel látjuk el, egy-egy kolléganő naponta 6–7 főhöz jut el. "
             "Jelenleg 32 ellátottunk van, a központ koordinálásával Pomáz és Csobánka teljes területén.</p>"),
            ("Egy kis történet",
             "<p>A házi gondozás az 1970-es évek elején jött létre Pomázon, kezdetben egyetlen gondozónő "
             "látta el a feladatokat városszerte. A gondozók létszáma az igényekkel együtt folyamatosan "
             "bővült, ma már Csobánka lakóit is ellátjuk.</p>"),
        ],
        "staff": ("Kollégáink", ["Farkas Judit", "Kalauz Csilla", "Márkus Zita", "Mester Dóra", "Szatmári Annamária"]),
        "links": [
            ("Értékelő lap és szolgáltatási rend", "dokumentumok.html", False),
            ("Térítési díjak – önkormányzati rendelet", "https://or.njt.hu/eli/731058/r/2024/6", True),
        ],
        "contact": {
            "person": "Garai Péterné, csoportvezető · Letonai Gabriella, szakmai vezető",
            "address": "2013 Pomáz, Községház utca 2.",
            "phones": [("+36 20 234 8004", "tel:+36202348004")],
            "email": "letonai.gabriella@szszk.pomaz.hu",
            "extra_emails": [
                ("Garai Péterné", "garai.peterne@szszk.pomaz.hu"),
                ("Galyasi-Szécsi Alexandra, asszisztens", "galyasi.szecsi.a@szszk.pomaz.hu"),
            ],
        },
    },
    {
        "slug": "jelzorendszeres-hazi-segitsegnyujtas",
        "title": "Jelzőrendszeres házi segítségnyújtás",
        "nav_title": "Jelzőrendszeres segítség",
        "short": "Egyetlen gombnyomás – és 30 percen belül szakképzett segítség érkezik. Az év 365 napján.",
        "icon": "bell",
        "image": "szolg-jelzorendszer.jpg",
        "image_alt": "Gondozó mutat valamit egy mosolygó idős asszonynak a telefonján",
        "fee": "Ingyenes",
        "area": "Pomáz",
        "tags": ["0–24, egész évben", "30 percen belül", "40 készülék"],
        "lead": "A saját otthonukban élő, egészségi állapotuk és szociális helyzetük miatt rászoruló "
                "időskorú vagy fogyatékos személyek, illetve pszichiátriai betegek részére nyújtott "
                "ellátás – a váratlan krízishelyzetek elhárítására.",
        "sections": [
            ("Mi történik, ha baj van?",
             "<p>Ha az idős ember rosszul lesz, elesik, megszédül vagy egyszerűen bizonytalannak érzi "
             "magát, <strong>egyetlen gombnyomással segítséget kérhet</strong>. A jelzés a "
             "diszpécserközpontba fut be, ahonnan az ügyeletes, szakképzett gondozónő azonnali "
             "értesítést kap, és <strong>legkésőbb 30 percen belül</strong> megjelenik az ellátott "
             "otthonában.</p>"
             "<p>A helyszínen felmérjük a helyzetet, és megtesszük a szükséges intézkedéseket: "
             "orvost vagy mentőt hívunk, beszélgetünk, megnyugtatunk, ellátjuk a higiénés "
             "szükségleteket, gyógyszert adunk be, vagy egyéb gondozási tevékenységet végzünk.</p>"),
            ("Mit hoznak magukkal a kollégák?",
             "<p>Munkatársaink készenléti táskával érkeznek, amely többek között tartalmaz "
             "<strong>vérnyomásmérőt, pulzoximétert, vércukormérőt</strong>, valamint kisebb sérülések, "
             "horzsolások ellátásához szükséges eszközöket. Így azonnal tájékozódni tudunk az idős "
             "ember állapotáról, és szükség esetén megfelelő segítséget szervezünk.</p>"),
            ("Kinek ajánljuk?",
             "<ul class=\"checklist\">"
             "<li>Egyedül élő időseknek.</li>"
             "<li>Azoknak, akik elesésveszélynek vannak kitéve.</li>"
             "<li>Krónikus betegséggel élőknek.</li>"
             "<li>Olyan családoknak, akik munka vagy más elfoglaltság miatt nem tudnak azonnal a "
             "helyszínre érkezni.</li>"
             "<li>Azoknak, akik szeretnék tudni, hogy szerettük nincs egyedül, ha baj van.</li>"
             "</ul>"),
            ("Miért több, mint egy segélyhívó?",
             "<p>A jelzőrendszeres házi segítségnyújtás nem csupán egy eszköz: a jelzésre "
             "<strong>valódi, személyes segítség érkezik helybe</strong>. Nem a családtagra hárul a "
             "sürgős helyzet kezelése – szakképzett kolléga jön ki, felméri az idős ember állapotát, és "
             "szükség esetén értesíti a hozzátartozókat vagy a mentőszolgálatot.</p>"
             "<p>Miközben a családtag dolgozik, ügyeket intéz vagy távol van otthonától, nyugodt lehet "
             "abban, hogy szükség esetén szakképzett segítség érkezik a szerettéhez.</p>"),
            ("Egy kis történet",
             "<p>A szolgáltatást 2022 őszén indítottuk el – az engedélyek beszerzését és a technikai "
             "feltételek megteremtését követően kerültek kihelyezésre az első adó-vevő készülékeink. "
             "Jelenleg 40 készülék helyezhető ki. A rendszer folyamatos készenlétben működik: az "
             "ellátás az év 365 napján, a nap 24 órájában elérhető.</p>"),
        ],
        "staff": ("Kollégáink", ["Majoros Ferencné", "Szatmári Annamária"]),
        "contact": {
            "person": "Garai Péterné, csoportvezető · Letonai Gabriella, szakmai vezető",
            "address": "2013 Pomáz, Községház utca 2.",
            "phones": [("+36 20 234 8004", "tel:+36202348004"), ("+36 26 525 274", "tel:+3626525274")],
            "email": "letonai.gabriella@szszk.pomaz.hu",
        },
    },
    {
        "slug": "idosek-klubja",
        "title": "Idősek Klubja",
        "nav_title": "Idősek Klubja",
        "short": "Nappali ellátás a város központjában: közösség, programok, gyógytorna – ingyenesen, kisbusszal.",
        "icon": "users",
        "image": "szolg-idosek-klubja.jpg",
        "image_alt": "Idősek beszélgetnek és nevetnek egy klubhelyiségben",
        "fee": "Ingyenes",
        "area": "Pomáz, Csobánka",
        "tags": ["25 férőhely", "Ingyenes kisbusz", "Heti 2× gyógytorna"],
        "lead": "A Pomáz központjában elhelyezkedő nappali intézmény több mint negyven éves múltra "
                "tekint vissza. Lehetőséget ad az önmaguk ellátására részben képes időseknek, hogy "
                "közösségbe járjanak, társas kapcsolatokat építsenek és megőrizzék szellemi frissességüket.",
        "sections": [
            ("Ingyenes odautazás",
             "<p>Az időseket – aki igényli – az intézmény kisbuszával szállítjuk be reggel "
             "<strong>8 és 10 óra között</strong>, és visszük haza <strong>14:30 és 16 óra között</strong>, "
             "ingyenesen. A klub elhelyezkedése kedvező: a közelben élelmiszerbolt, háztartási bolt, "
             "gyógyszertár és orvosi rendelő is található.</p>"),
            ("Mit nyújtunk a klubtagoknak?",
             "<ul class=\"checklist\">"
             "<li>Hasznos időtöltés és közösségi együttlét, személyre szabott foglalkozásokkal.</li>"
             "<li>Személyi tisztálkodás és a személyes ruházat tisztításának lehetősége.</li>"
             "<li>Igény szerint meleg ebéd.</li>"
             "<li>Szabadidős programok, kirándulások, majális, szüreti mulatság.</li>"
             "<li>Névnapok, születésnapok és jeles napok közös megünneplése.</li>"
             "<li>Heti kétszer ingyenes gyógytorna.</li>"
             "<li>Térítés ellenében fodrász és pedikűrös szolgáltatás.</li>"
             "<li>Segítség a hivatalos ügyek intézésében, az egészségügyi alap- és szakellátáshoz jutásban.</li>"
             "<li>Életviteli és életvezetési tanácsadás, szükség szerint egyéni esetkezelés.</li>"
             "</ul>"),
            ("Férőhelyek és igénybevétel",
             "<p>A nappali ellátás keretében <strong>25 fő</strong> részére tudunk helyet biztosítani, "
             "Pomáz és Csobánka lakói számára. A klubszolgáltatás igénybevétele önkéntes és ingyenes, "
             "szóbeli vagy írásbeli kérelemre indul.</p>"),
        ],
        "staff": ("Kollégánk", ["Kohányi Miklósné"]),
        "links": [
            ("Az Idősek Klubja a Facebookon", "https://www.facebook.com/profile.php?id=100009345232457", True),
        ],
        "contact": {
            "person": "Garai Péterné, csoportvezető",
            "address": "2013 Pomáz, Községház utca 2.",
            "phones": [("+36 26 525 274", "tel:+3626525274"), ("+36 20 234 8004", "tel:+36202348004")],
            "email": "garai.peterne@szszk.pomaz.hu",
        },
    },
    {
        "slug": "idosek-atmeneti-gondozohaza",
        "title": "Idősek Átmeneti Gondozóháza",
        "nav_title": "Átmeneti Gondozóház",
        "short": "18 férőhelyes bentlakásos ellátás 24 órás gondozói felügyelettel, apartmanokban, pihenőkerttel.",
        "icon": "building",
        "image": "szolg-gondozohaz.jpg",
        "image_alt": "Gondozó és idős asszony mosolyogva beszélgetnek",
        "fee": "Térítési díj ellenében",
        "area": "Pomáz",
        "tags": ["18 férőhely", "24 órás felügyelet", "6 apartman"],
        "lead": "A Gondozóház átmenetet képez a saját otthonban történő gondozás és a tartós "
                "bentlakásos intézmény között. Azoknak nyújt megoldást, akik betegségük vagy más ok "
                "miatt otthonukban időlegesen nem tudnak magukról gondoskodni.",
        "sections": [
            ("Az ellátás tartalma",
             "<ul class=\"checklist\">"
             "<li>Lakhatás hat apartmanban – mindegyikhez egy egyágyas és egy kétágyas szoba, "
             "valamint külön fürdőszoba és konyha tartozik.</li>"
             "<li>24 órás gondozónői felügyelet.</li>"
             "<li>Napi háromszori étkeztetés, szükség esetén diétás étrenddel.</li>"
             "<li>Szükség szerint ruházattal, textíliával való ellátás, mosás.</li>"
             "<li>Orvosi és egészségügyi ellátás.</li>"
             "<li>Mentálhigiénés gondozás és foglalkoztatás.</li>"
             "<li>Csoportos és egyéni gyógytorna.</li>"
             "<li>Térítés ellenében fodrászat és pedikűr.</li>"
             "</ul>"
             "<p>Az intézmény tömegközlekedéssel és személygépkocsival egyaránt kiválóan megközelíthető, "
             "a gondozóháznak gondozott pihenőkertje van.</p>"),
            ("Kik vehetők fel?",
             "<p>Pomázi lakcímmel rendelkező időskorúak, valamint azok a 18. életévüket betöltött "
             "személyek, akik betegségük vagy más ok miatt otthonukban időlegesen nem tudnak "
             "magukról gondoskodni.</p>"
             "<p>Nem vehető fel az a személy, aki <strong>pszichiátriai vagy szenvedélybetegségben "
             "szenved, fertőző beteg, illetve akinek állapota kórházi ellátást igényel</strong>.</p>"),
            ("Az ellátás időtartama",
             "<p>Az ellátás időtartama <strong>egy év</strong>. Ha egy év elteltével a gondozott "
             "családi környezetbe nem helyezhető vissza, vagy ellátása az alapellátás keretein belül "
             "nem biztosítható, az intézmény orvosának szakvéleménye alapján egy alkalommal egy évvel "
             "meghosszabbítható.</p>"
             "<p>Az ellátás önkéntes, szóbeli vagy írásbeli kérelemre indul. A bekerülés időpontja a "
             "szabad férőhelyek számától függ.</p>"),
            ("Egy kis történet",
             "<p>Az Idősek Átmeneti Gondozóháza 2007-ben kezdte meg működését. Azt a lakossági igényt "
             "elégíti ki, amely azon idős emberek részéről merül fel, akiknek életkoruk, egészségi "
             "állapotuk vagy szociális helyzetük miatt már nem elegendők az alapszolgáltatás keretében "
             "biztosított ellátásaink.</p>"),
        ],
        "staff": ("Kollégáink", [
            "Bajtek Mihályné, gondozónő", "Leidinger Gáborné, gondozónő", "Mester Attiláné, gondozónő",
            "Örögné Schneider Szilvia, gondozónő", "Vindischné Bánfi Barbara, mentálhigiénés munkatárs",
        ]),
        "links": [
            ("Térítési díjak – önkormányzati rendelet",
             "https://or.njt.hu/download/403/resources/EJR_93233388-RM2_szocell_t_s_dijak.pdf", True),
        ],
        "contact": {
            "person": "Majoros Ferencné, csoportvezető",
            "address": "2013 Pomáz, Községház utca 2.",
            "phones": [("+36 26 525 275", "tel:+3626525275"), ("+36 20 236 0866", "tel:+36202360866")],
            "email": "atmeneti@szszk.pomaz.hu",
        },
    },
    {
        "slug": "csalad-es-gyermekjoleti-szolgalat",
        "title": "Család- és Gyermekjóléti Szolgálat",
        "nav_title": "Családsegítő szolgálat",
        "short": "Tanácsadás, mediáció és krízissegítség családoknak, gyermekeknek – ingyenesen, bizalmasan.",
        "icon": "hand-heart",
        "image": "szolg-csaladsegito.jpg",
        "image_alt": "Édesanya és három gyermek együtt mosolyognak a szabadban",
        "fee": "Ingyenes",
        "area": "Pomáz",
        "tags": ["Ingyenes", "Mediáció", "Pszichológiai tanácsadás"],
        "lead": "A gyermekjóléti szolgáltatás a gyermek testi és lelki egészségének, családban történő "
                "nevelkedésének elősegítését, a veszélyeztetettség megelőzését és megszüntetését "
                "szolgálja. A családsegítés pedig szociális vagy mentálhigiénés problémák, illetve "
                "krízishelyzet miatt segítségre szoruló személyeket, családokat támogat.",
        "sections": [
            ("Amiben számíthat ránk",
             "<ul class=\"checklist\">"
             "<li>Szociális, életvezetési és mentálhigiénés tanácsadás.</li>"
             "<li>Kríziskezelés és a nehéz élethelyzetben élő családokat segítő szolgáltatások.</li>"
             "<li>Tájékoztatás a gyermeki jogokról és a gyermek fejlődését biztosító támogatásokról, "
             "segítség a támogatásokhoz való hozzájutásban.</li>"
             "<li>Anyagi nehézségekkel küzdőknek a pénzbeli és természetbeni ellátásokhoz, szociális "
             "szolgáltatásokhoz való hozzájutás megszervezése.</li>"
             "<li>Családtervezési, pszichológiai, nevelési, egészségügyi és mentálhigiénés tanácsadás, "
             "illetve a káros szenvedélyek megelőzését célzó tanácsadás megszervezése.</li>"
             "<li>Válsághelyzetben lévő várandós anyák támogatása, tájékoztatás az inkubátorokról és az "
             "örökbefogadás lehetőségéről.</li>"
             "<li>Tanácsadás tartós és fiatal munkanélkülieknek, adósságterhekkel és lakhatási "
             "gondokkal küzdőknek, fogyatékossággal élőknek, krónikus, szenvedély- és pszichiátriai "
             "betegeknek, illetve családtagjaiknak.</li>"
             "<li>Szabadidő-szervezés, közösségfejlesztő programok, egyéni és csoportos készségfejlesztés.</li>"
             "<li>Környezettanulmány készítése felkérésre, a gyermek panaszának meghallgatása és orvoslása.</li>"
             "</ul>"),
            ("Szolgáltatásaink",
             "<ul class=\"checklist\">"
             "<li><strong>Mediáció és szülőkonzultáció</strong> a családon belüli problémák megoldására, "
             "előre egyeztetett időpontban.</li>"
             "<li><strong>Pszichológiai tanácsadás.</strong></li>"
             "<li><strong>Számítógép- és internethasználat</strong> – például álláskeresés vagy "
             "albérletkeresés céljából.</li>"
             "</ul>"),
            ("Észlelő- és jelzőrendszer",
             "<p>A családok segítése érdekében veszélyeztetettséget és krízishelyzetet észlelő "
             "jelzőrendszer működik. A jegyző, a járási hivatal, a szociális, egészségügyi és oktatási "
             "szolgáltatók, intézmények, egyesületek, alapítványok, vallási közösségek és "
             "<strong>magánszemélyek is jelezhetik</strong> a szolgálatnak, ha segítségre szoruló "
             "családról vagy személyről szereznek tudomást.</p>"),
        ],
        "office_hours": [
            ("Hétfő", "13:00 – 16:00"),
            ("Szerda", "8:00 – 12:00 és 13:00 – 17:00"),
            ("Péntek", "8:00 – 12:00"),
        ],
        "emergency": [
            ("Gyermekvédelmi jelzőrendszeri készenléti szolgálat",
             "Munkanapokon 16:00-tól reggel 8:00-ig, hétvégén és munkaszüneti napokon 0–24 órában.",
             "+36 20 364 0827", "tel:+36203640827"),
            ("Országos Gyermekvédő Hívószám",
             "A nap 24 órájában ingyenesen hívható.",
             "+36 80 21 20 21", "tel:+3680212021"),
        ],
        "links": [
            ("A Családsegítő Szolgálat a Facebookon", "https://www.facebook.com/csaladsegito.pomaz.7", True),
        ],
        "contact": {
            "person": "Benczik Orsolya, tagintézmény-vezető",
            "address": "2013 Pomáz, Kossuth Lajos utca 21/A",
            "phones": [("+36 20 808 7075", "tel:+36208087075"), ("+36 26 322 370", "tel:+3626322370")],
            "email": "csaladsegito@szszk.pomaz.hu",
            "note": "Időpontot telefonon és e-mailben is lehet foglalni.",
        },
    },
    {
        "slug": "iskolavedono",
        "title": "Iskolavédőnői szolgálat",
        "nav_title": "Iskolavédőnő",
        "short": "A 6–18 évesek egészségének megőrzése: szűrővizsgálatok, védőoltások, tanácsadás – ingyenesen.",
        "icon": "stethoscope",
        "image": "szolg-vedono.jpg",
        "image_alt": "Védőnő sztetoszkóppal vizsgál egy kisgyermeket",
        "fee": "Ingyenes",
        "area": "Pomáz",
        "tags": ["6–18 évesek", "Az alapellátás része", "Mindenkinek ingyenes"],
        "lead": "Az iskolai védőnő a 6–18 éveseket látja el. Feladata az egészségmegőrzés érdekében "
                "való tevékenykedés: közreműködik az előírt szűrővizsgálatok, valamint a védőoltások "
                "megszervezésében és lebonyolításában.",
        "sections": [
            ("Együttműködés",
             "<p>A védőnő az orvoson kívül szorosan együttműködik a <strong>pedagógusokkal, szülőkkel, "
             "szakemberekkel és civil szervezetekkel</strong>. A védőnői ellátás az alapellátás része, "
             "mindenki számára ingyenes szolgáltatás. Pomázon egy iskolavédőnő és két területi védőnő "
             "látja el a feladatokat.</p>"),
        ],
        "contact": {
            "person": "dr. Temesiné Estermann Andrea, iskolavédőnő",
            "address": "2013 Pomáz, Kossuth Lajos utca 38/B",
            "phones": [("+36 26 327 244", "tel:+3626327244"), ("+36 20 228 2045", "tel:+36202282045")],
            "email": "vedonok@pomaz.hu",
            "note": "Fogadóórák körzetenként, a Védőnői Szolgálat tájékoztatása szerint.",
        },
    },
    {
        "slug": "szallitas",
        "title": "Betegszállítás",
        "nav_title": "Szállítás",
        "short": "Idősek és betegek szállítása a szentendrei és kiskovácsi rendelőintézetekbe – kerekesszékkel is.",
        "icon": "bus",
        "image": "szolg-szallitas.jpg",
        "image_alt": "Az intézmény fehér kisbusza",
        "fee": "Előzetes időpontfoglalással",
        "area": "Szentendre, Kiskovácsi",
        "tags": ["Kerekesszékkel is", "Hétköznap 10–14 óra", "Előzetes egyeztetés"],
        "lead": "Idősek és betegek személyszállítása a kiskovácsi és szentendrei egészségügyi "
                "intézményekbe. A szállítás kerekesszékkel is igénybe vehető.",
        "sections": [
            ("Mikor kérhető?",
             "<p>A szállítás <strong>hétköznapokon 10 és 14 óra között</strong> lehetséges, előzetes "
             "időpontfoglalás esetén. Kérjük, hívja munkatársainkat a szállítás egyeztetéséhez.</p>"),
        ],
        "contact": {
            "person": "Garai Péterné, csoportvezető",
            "address": "2013 Pomáz, Községház utca 2.",
            "phones": [("+36 20 234 8004", "tel:+36202348004")],
            "email": "garai.peterne@szszk.pomaz.hu",
        },
    },
]

# --- Hírek ---------------------------------------------------------------
# A hírek külön Markdown-fájlokban élnek a content/hirek/ mappában, hogy a
# szerkesztőfelületről (Sveltia/Decap CMS) is írhatók legyenek. Egy fájl = egy
# bejegyzés; a fájlnév dátumelőtagja csak rendezést segít, a slug a maradék.

_HU_HONAPOK = ["január", "február", "március", "április", "május", "június",
               "július", "augusztus", "szeptember", "október", "november", "december"]


def _hu_datum(iso):
    """2026-07-15 -> 2026. július 15."""
    try:
        ev, ho, nap = (int(x) for x in str(iso).split("-")[:3])
        return "%d. %s %d." % (ev, _HU_HONAPOK[ho - 1], nap)
    except (ValueError, IndexError):
        return str(iso)


def load_news(folder=None):
    """A content/hirek/*.md fájlok beolvasása, legfrissebb elöl."""
    folder = folder or os.path.join(_ROOT, "content", "hirek")
    posts = []
    if not os.path.isdir(folder):
        return posts
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md") or name.startswith("_"):
            continue
        raw = open(os.path.join(folder, name), encoding="utf-8").read()
        meta, body = split_front_matter(raw)
        stem = name[:-3]
        m = re.match(r"^(\d{4}-\d{2}-\d{2})-(.+)$", stem)
        date = str(meta.get("date") or (m.group(1) if m else ""))
        slug = str(meta.get("slug") or (m.group(2) if m else stem))
        if not meta.get("title"):
            continue
        image = str(meta.get("image") or "")
        if image and "/" in image:          # a CMS teljes útvonalat is írhat
            image = image.rsplit("/", 1)[1]
        posts.append({
            "slug": slug,
            "date": date,
            "date_hu": _hu_datum(date),
            "title": str(meta["title"]),
            "excerpt": str(meta.get("excerpt") or plain_text(body, 190)),
            "image": image,
            "image_alt": str(meta.get("image_alt") or ""),
            "highlight": bool(meta.get("highlight")),
            "link": ((str(meta["link_label"]), str(meta["link_href"]))
                     if meta.get("link_label") and meta.get("link_href") else None),
            "body_html": render(body, media_prefix="assets/img/hirek/"),
        })
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


NEWS = load_news()

# --- Képgaléria -----------------------------------------------------------
# Az albumok külön Markdown-fájlokban élnek a content/galeria/ mappában, hogy a
# tartalomkezelőből is létrehozhatók legyenek. Egy fájl = egy album; a képeket a
# CMS az assets/img/galeria/ mappába tölti fel.


def _basename(path):
    return str(path).replace("\\", "/").rsplit("/", 1)[-1]


def load_gallery(folder=None):
    """A content/galeria/*.md albumok beolvasása, legfrissebb elöl."""
    folder = folder or os.path.join(_ROOT, "content", "galeria")
    albums = []
    if not os.path.isdir(folder):
        return albums
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md") or name.startswith("_"):
            continue
        raw = open(os.path.join(folder, name), encoding="utf-8").read()
        meta, body = split_front_matter(raw)
        if not meta.get("title"):
            continue

        photos = []
        raw_photos = meta.get("photos")
        if not isinstance(raw_photos, list):     # üres vagy "[]" érték
            raw_photos = []
        for item in raw_photos:
            if isinstance(item, dict):
                src, caption = item.get("image"), item.get("caption") or ""
            else:
                src, caption = item, ""
            if src:
                photos.append({"file": _basename(src), "caption": str(caption)})

        cover = _basename(meta.get("cover") or "")
        if not cover and photos:
            cover = photos[0]["file"]

        albums.append({
            "slug": str(meta.get("slug") or name[:-3]),
            "title": str(meta["title"]),
            "year": str(meta.get("year") or str(meta.get("date", ""))[:4]),
            "date": str(meta.get("date") or ""),
            "cover": cover,
            "photos": photos,
            "external_url": str(meta.get("external_url") or ""),
            "description_html": render(body) if body.strip() else "",
        })
    albums.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    return albums


GALLERY = load_gallery()

# --- Dokumentumok ---------------------------------------------------------
DOC_GROUPS = [
    {
        "title": "Minden szolgáltatáshoz szükséges",
        "note": "Étkeztetés, Idősek Klubja, házi segítségnyújtás és jelzőrendszeres házi segítségnyújtás "
                "igényléséhez mindhárom nyomtatvány kitöltése szükséges.",
        "docs": [
            ("Kérelem a személyes gondoskodást nyújtó szociális ellátás igénybevételéhez", "Nyomtatvány",
             "https://drive.google.com/file/d/1GOVel61SYe6thaCh2LJZBTxxvdr3Ub53/view?usp=sharing"),
            ("Jövedelemnyilatkozat", "Nyomtatvány",
             "https://drive.google.com/file/d/1yFeKKUYVW0b0CpkHq0GZaJaHd8Ce3kjm/view?usp=sharing"),
            ("Egészségi állapotra vonatkozó igazolás", "Nyomtatvány",
             "https://drive.google.com/file/d/1zpR5--PD9YT5v51lb--Zaui9m8ywJdfu/view?usp=sharing"),
        ],
    },
    {
        "title": "Házi segítségnyújtáshoz külön",
        "note": "A fenti három nyomtatványon felül kitöltendő.",
        "docs": [
            ("Értékelő lap", "Nyomtatvány",
             "https://drive.google.com/file/d/1woTRKGXHAII3vcAnRNyRsx7SbRyvz6a2/view?usp=sharing"),
        ],
    },
    {
        "title": "Átmeneti Gondozóházba jelentkezéshez",
        "note": "A kérelem, a jövedelemnyilatkozat és az egészségi állapotra vonatkozó igazolás mellett "
                "az alábbi személyes iratokat kérjük bemutatni.",
        "docs": [],
        "list": {
            "Személyes iratok": ["Személyi igazolvány", "Lakcímkártya", "TAJ-kártya",
                                 "A Magyar Államkincstár Nyugdíjfolyósító Igazgatóságának tárgyévi igazolása"],
            "Szükség esetén": ["ORSZI határozat (Országos Rehabilitációs és Szociális Szakértői Intézet igazolása)",
                               "Kórházi zárójelentés", "Egyéb igazolások (például pszichiátriai igazolás)"],
        },
    },
    {
        "title": "Szolgáltatási rendek és térítési díjak",
        "note": "Tájékoztató dokumentumok az ellátások működéséről és költségeiről.",
        "docs": [
            ("Házi segítségnyújtás – szolgáltatási rend", "Tájékoztató",
             "https://drive.google.com/file/d/1FyqY_rnBrECcni3dccJG9R1qGi2YTUmq/view?usp=sharing"),
            ("Étkeztetés – szolgáltatási rend", "Tájékoztató",
             "https://drive.google.com/file/d/1TFSxGu4bMXU3MJKhkC4bGHKSCOgbmiHr/view?usp=sharing"),
            ("Idősek Klubja – szolgáltatási rend", "Tájékoztató",
             "https://drive.google.com/file/d/1LAO_YJr4fzYOJBQbtzYht14Mk04UQsLT/view?usp=sharing"),
            ("Tájékoztató a térítési díjakról", "Tájékoztató",
             "https://drive.google.com/file/d/18xlE7ViJGnpXQFCF5ddl4LxwNlFTsSMc/view?usp=sharing"),
            ("Pomáz Város Önkormányzatának szociális rendelete", "Jogszabály",
             "https://or.njt.hu/eli/731058/r/2024/6"),
        ],
    },
]

# --- Elérhetőségek --------------------------------------------------------
CONTACT_UNITS = [
    {
        "name": "Szociális Szolgáltatási Központ",
        "role": "Székhely, központi ügyintézés",
        "address": "2013 Pomáz, Községház utca 2.",
        "phones": [("+36 20 234 8004", "tel:+36202348004"), ("+36 26 525 274", "tel:+3626525274")],
        "email": "szszk@szszk.pomaz.hu",
        "hours": "hétfő–péntek 8:30–15:00",
        "icon": "building",
    },
    {
        "name": "Idősek Napközbeni Ellátása",
        "role": "Étkeztetés · Idősek Klubja · házi segítségnyújtás · jelzőrendszer · szállítás",
        "address": "2013 Pomáz, Községház utca 2.",
        "phones": [("+36 20 234 8004", "tel:+36202348004"), ("+36 26 525 274", "tel:+3626525274")],
        "email": "garai.peterne@szszk.pomaz.hu",
        "hours": "hétfő–péntek 9:00–15:00",
        "icon": "users",
    },
    {
        "name": "Idősek Átmeneti Gondozóháza",
        "role": "Bentlakásos átmeneti elhelyezés",
        "address": "2013 Pomáz, Községház utca 2.",
        "phones": [("+36 26 525 275", "tel:+3626525275"), ("+36 20 236 0866", "tel:+36202360866")],
        "email": "atmeneti@szszk.pomaz.hu",
        "hours": "hétfő–péntek 9:00–15:00",
        "icon": "building",
    },
    {
        "name": "Család- és Gyermekjóléti Szolgálat",
        "role": "Családsegítés, gyermekjóléti szolgáltatás",
        "address": "2013 Pomáz, Kossuth Lajos utca 21/A",
        "phones": [("+36 20 808 7075", "tel:+36208087075"), ("+36 26 322 370", "tel:+3626322370")],
        "email": "csaladsegito@szszk.pomaz.hu",
        "hours": "hétfő 13–16 · szerda 8–12 és 13–17 · péntek 8–12",
        "icon": "hand-heart",
    },
    {
        "name": "Védőnői Szolgálat",
        "role": "Iskolavédőnői és területi védőnői ellátás",
        "address": "2013 Pomáz, Kossuth Lajos utca 38/B",
        "phones": [("+36 26 327 244", "tel:+3626327244"), ("+36 20 228 2045", "tel:+36202282045")],
        "email": "vedonok@pomaz.hu",
        "hours": "körzetenként, a Szolgálat tájékoztatása szerint",
        "icon": "stethoscope",
    },
]

LEADERS = [
    ("dr. Király Eszter", "intézményvezető", "+36 20 234 8004", "tel:+36202348004", "szszk@szszk.pomaz.hu"),
    ("Garai Péterné", "intézményvezető-helyettes, az Idősek Napközbeni Ellátása csoport vezetője",
     "+36 20 225 9114", "tel:+36202259114", "garai.peterne@szszk.pomaz.hu"),
    ("Majoros Ferencné", "az Idősek Átmeneti Gondozóháza csoportvezetője",
     "+36 20 236 0866", "tel:+36202360866", "atmeneti@szszk.pomaz.hu"),
    ("Benczik Orsolya", "a Család- és Gyermekjóléti Szolgálat tagintézmény-vezetője",
     "+36 20 541 8914", "tel:+36205418914", "csaladsegito@szszk.pomaz.hu"),
    ("Letonai Gabriella", "a házi segítségnyújtás és a jelzőrendszeres segítségnyújtás szakmai vezetője",
     "+36 20 234 8004", "tel:+36202348004", "letonai.gabriella@szszk.pomaz.hu"),
    ("dr. Temesiné Estermann Andrea", "iskolavédőnő",
     "+36 20 228 2045", "tel:+36202282045", "vedonok@pomaz.hu"),
]

# --- Jogszabályok ---------------------------------------------------------
LAW_GROUPS = [
    ("Működés és gazdálkodás", [
        "Az államháztartásról szóló 2011. évi CXCV. törvény",
        "A Munka Törvénykönyvéről szóló 2012. évi I. törvény",
        "A közalkalmazottak jogállásáról szóló 1992. évi XXXIII. törvény",
        "Az egészségügyi szolgálati jogviszonyról szóló 2020. évi C. törvény",
        "A Polgári Törvénykönyvről szóló 2013. évi V. törvény",
        "A számvitelről szóló 2000. évi C. törvény",
        "Az államháztartás szervezetei beszámolási és könyvvezetési kötelezettségének sajátosságairól "
        "szóló 249/2000. (XII. 24.) Korm. rendelet",
        "A költségvetési szervek belső kontrollrendszeréről és belső ellenőrzéséről szóló "
        "370/2011. (XII. 31.) Korm. rendelet",
    ]),
    ("Szociális ellátások és szolgáltatások", [
        "A szociális igazgatásról és szociális ellátásokról szóló 1993. évi III. törvény",
        "Egyes pénzbeli szociális ellátások folyósításának és elszámolásának szabályairól szóló "
        "62/2006. (III. 27.) Korm. rendelet",
        "A személyes gondoskodást nyújtó szociális ellátások térítési díjáról szóló "
        "29/1993. (II. 17.) Korm. rendelet",
        "Az egyes szociális szolgáltatásokat végzők képzéséről és vizsgakövetelményeiről szóló "
        "81/2004. (IX. 18.) ESzCsM rendelet",
        "A fogyatékos személyek alapvizsgálatáról, a rehabilitációs alkalmassági vizsgálatról, továbbá "
        "a szociális intézményekben ellátott személyek állapotának felülvizsgálatáról szóló "
        "92/2008. (IV. 23.) Korm. rendelet",
        "A személyes gondoskodást nyújtó szociális intézmények szakmai feladatairól és működésük "
        "feltételeiről szóló 1/2000. (I. 7.) SzCsM rendelet",
        "A személyes gondoskodást végző személyek adatainak működési nyilvántartásáról szóló "
        "8/2000. (VIII. 4.) SzCsM rendelet",
        "A személyes gondoskodást végző személyek továbbképzéséről és a szociális szakvizsgáról szóló "
        "9/2000. (VIII. 4.) SzCsM rendelet",
    ]),
    ("Gyermekvédelem, gyermeki jogok", [
        "A gyermekek védelméről és a gyámügyi igazgatásról szóló 1997. évi XXXI. törvény",
        "A Gyermek jogairól szóló, New Yorkban, 1989. november 20-án kelt Egyezmény kihirdetéséről "
        "szóló 1991. évi LXIV. törvény",
        "A nevelőszülői, a hivatásos nevelőszülői és a helyettes szülői jogviszony egyes kérdéseiről "
        "szóló 261/2002. (XII. 18.) Korm. rendelet",
        "A gyermekjóléti és gyermekvédelmi szolgáltatótevékenység engedélyezéséről, valamint a "
        "gyermekjóléti és gyermekvédelmi vállalkozói engedélyről szóló 259/2002. (XII. 18.) Korm. rendelet",
        "A gyámhatóságok, a területi gyermekvédelmi szakszolgálatok, a gyermekjóléti szolgálatok és a "
        "személyes gondoskodást nyújtó szervek és személyek által kezelt személyes adatokról szóló "
        "235/1997. (XII. 17.) Korm. rendelet",
        "A gyámhatóságokról, valamint a gyermekvédelmi és gyámügyi eljárásról szóló "
        "149/1997. (IX. 10.) Korm. rendelet",
        "A személyes gondoskodást nyújtó gyermekjóléti alapellátások és gyermekvédelmi szakellátások "
        "térítési díjáról és az igénylésükhöz felhasználható bizonyítékokról szóló "
        "328/2011. (XII. 29.) Korm. rendelet",
        "A pénzbeli és természetbeni szociális ellátások igénylésének és megállapításának, valamint "
        "folyósításának részletes szabályairól szóló 63/2006. (III. 27.) Korm. rendelet",
        "A személyes gondoskodást nyújtó gyermekjóléti, gyermekvédelmi intézmények, valamint személyek "
        "szakmai feladatairól és működésük feltételeiről szóló 15/1998. (IV. 30.) NM rendelet",
    ]),
    ("Védőnői tevékenység", [
        "Az egészségügyi és a hozzájuk kapcsolódó személyes adatok kezeléséről és védelméről szóló "
        "1997. évi XLVII. törvény",
        "Az iskola-egészségügyi ellátásról szóló 26/1997. (IX. 3.) NM rendelet",
        "Az egészségügyről szóló 1997. évi CLIV. törvény",
        "Az egészségügyi tevékenység végzésének egyes kérdéseiről szóló 2003. évi LXXXIV. törvény",
        "Az egészségügyi szolgáltatások Egészségbiztosítási Alapból történő finanszírozásának részletes "
        "szabályairól szóló 43/1999. (III. 3.) Korm. rendelet 20. § és 21. §",
        "Az egészségügyi szolgáltatás gyakorlásának általános feltételeiről, valamint a működési "
        "engedélyezési eljárásról szóló 96/2003. (VII. 15.) Korm. rendelet",
    ]),
]

USEFUL_LINKS = [
    ("Pomáz Város Önkormányzata", "A fenntartó önkormányzat hivatalos oldala", "https://pomaz.hu"),
    ("Pest Vármegyei Kormányhivatal", "Az intézmény felügyeleti szerve",
     "https://kormanyhivatalok.hu/kormanyhivatalok/pest"),
    ("Nemzeti Jogszabálytár", "Hatályos jogszabályok és önkormányzati rendeletek", "https://njt.hu"),
]
