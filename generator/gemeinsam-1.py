# -*- coding: utf-8 -*-
"""Gemeinsame Bausteine für simonmonu.at.

Alles, was vor dem Livegang noch von Simon kommen muss, steht als Konstante
in diesem Kopf. bau.py meldet beim Bauen, was noch fehlt.
"""
import os, json, html, re

BASIS = os.path.dirname(os.path.abspath(__file__))
WURZEL = os.path.abspath(os.path.join(BASIS, ".."))
AUS = os.environ.get("SM_AUS") or os.path.join(WURZEL, "website")
DOMAIN = "https://simonmonu.at"
NAME = "Simon Monu"


def _wortmarke():
    """Wortmarke „Simon Monu.“ aus _quelle/marke/logo.svg, inline: Buchstaben in der Textfarbe, das Quadrat in Signalfarbe.
    So passt sie sich hellem und dunklem Grund an, ohne zweite Datei."""
    import re as _re
    pfad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_quelle", "marke", "logo.svg")
    if not os.path.exists(pfad):
        return "Simon Monu"
    svg = open(pfad, encoding="utf-8").read()
    svg = _re.sub(r'(<rect x="584[^>]*?) fill="[^"]*"', r'\1 class="wm-punkt"', svg)
    svg = _re.sub(r' fill="#[0-9A-Fa-f]{6}"', ' fill="currentColor"', svg)
    return svg.replace("<svg ", '<svg class="wortmarke" aria-hidden="true" focusable="false" ', 1)


MAIL = "office@simonmonu.at"

# Stand von CSS/JS. Bei jeder Änderung an css/ oder js/ hochzählen, sonst zeigen
# Browser bis zu einer Woche lang die alte Fassung (Cache-Regel in _headers).
VERSION = "19"

# --- Noch offen (bis zum Livegang eintragen) ----------------------------------
TELEFON = "+43 676 561 8098"            # z. B. "+43 660 1234567"; leer = Telefon wird nirgends angezeigt
FORMSPREE = "https://formspree.io/f/xwlpyyoq"          # z. B. "https://formspree.io/f/abcdwxyz"; leer = mailto-Formular
NAECHSTER_START = os.environ.get("SM_START", "")   # z. B. "November"; leer = Ring entfällt
ANSCHRIFT = {"strasse": "Eichetstrasse 51", "plz": "5071", "ort": "Wals-Siezenheim"}   # Pflicht nach § 5 ECG
UID = ""                # nur eintragen, wenn es eine gibt (z. B. "ATU12345678")
GEWERBE = {"wortlaut": "Werbeagentur", "behoerde": "Bezirkshauptmannschaft Salzburg-Umgebung", "fachgruppe": "Fachgruppe Werbung und Marktkommunikation"}   # genau laut GISA-Auszug
INSTAGRAM = ""          # optional, volle Adresse
LINKEDIN = ""           # optional, volle Adresse

EINFUEHRUNG = False     # Einführungsangebot gibt es nicht mehr (Preisspannen laut Geschäftsplan)
MONATE = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]
KURZ = ["Jän", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MONATE_EN = ["January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December"]
KURZ_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# --- Sprache ------------------------------------------------------------------
# bau.py setzt LANG vor jeder Seite auf "de" oder "en". Die englische Fassung liegt unter /en/.
LANG = "de"

# deutsche Adresse -> englische Adresse
PFAD_EN = {"/": "/en/", "/arbeiten/": "/en/work/", "/leistungen/": "/en/services/", "/handwerk/": "/en/trades/",
           "/ueber-mich/": "/en/about/", "/kontakt/": "/en/contact/", "/danke/": "/en/thanks/",
           "/impressum/": "/en/legal-notice/", "/datenschutz/": "/en/privacy/",
           "/arbeiten/nickmonu/": "/en/work/nickmonu/", "/arbeiten/hallwirth/": "/en/work/hallwirth/",
           "/arbeiten/lindtner/": "/en/work/lindtner/"}
PFAD_DE = {v: k for k, v in PFAD_EN.items()}


def tr(de, en):
    """Text je nach Sprache der Seite, die gerade gebaut wird."""
    return en if LANG == "en" else de


def P(href):
    """Interne Adresse in die Sprache der aktuellen Seite übersetzen. Fremde Adressen, Anker und Dateien bleiben unverändert."""
    if LANG != "en" or not href.startswith("/"):
        return href
    m = re.match(r"^([^?#]*)(.*)$", href)
    return PFAD_EN.get(m.group(1), m.group(1)) + m.group(2)


def gegenstueck(pfad):
    """(deutsche Adresse, englische Adresse) einer Seite, oder None, wenn es keine zweite Sprache gibt."""
    if pfad in PFAD_EN:
        return pfad, PFAD_EN[pfad]
    if pfad in PFAD_DE:
        return PFAD_DE[pfad], pfad
    return None


e = html.escape


def csp(meta=False):
    """Content-Security-Policy der Hauptseite. meta=True: Fassung für <meta>, dort sind frame-ancestors nicht erlaubt."""
    form = f" {FORMSPREE}" if FORMSPREE else ""
    fa = f"'self'{form}" if FORMSPREE else "'self' mailto:"
    teile = ["default-src 'none'", "script-src 'self'", "style-src 'self'", "img-src 'self'", "font-src 'self'",
             f"connect-src 'self'{form}", "media-src 'self'", "frame-src 'self'", f"form-action {fa}", "base-uri 'self'", "object-src 'none'",
             "manifest-src 'self'"]
    if not meta:
        teile += ["frame-ancestors 'none'", "upgrade-insecure-requests"]
    return "; ".join(teile)


def telefon_href():
    return "tel:" + re.sub(r"[^+\d]", "", TELEFON)


def anschrift_fehlt():
    return not (ANSCHRIFT["strasse"] and ANSCHRIFT["plz"])


def gewerbe_fehlt():
    return not all(GEWERBE.values())


def offen():
    """Liste dessen, was vor dem Livegang noch fehlt (für bau.py)."""
    o = []
    if not TELEFON: o.append("TELEFON (Telefon wird nirgends angezeigt)")
    if not FORMSPREE: o.append("FORMSPREE (Formular fällt auf mailto zurück)")
    if not NAECHSTER_START: o.append("NAECHSTER_START (Verfügbarkeits-Ring entfällt)")
    if anschrift_fehlt(): o.append("ANSCHRIFT (Straße und PLZ, Pflicht im Impressum)")
    if gewerbe_fehlt(): o.append("GEWERBE (Wortlaut, Behörde, Fachgruppe laut GISA-Auszug)")
    return o


def nbsp(s):
    return s.replace(" €", " €").replace(" %", " %")


def eur(n):
    if LANG == "en":
        return f"€{n:,}"
    return f"{n:,}".replace(",", ".") + " €"


# --- Leistungen (aus dem Geschäftsplan Oktober 2026: fünf Angebote mit Preisspannen) ----------------------
# von/bis: Spanne in Euro. einheit "monat" = pro Monat. Der Festpreis steht erst im Angebot nach dem Erstgespräch.

PAKETE = [
    {"id": "check", "name": "Website-Check", "von": 150, "bis": 300, "einheit": "",
     "fuer": "Sie haben eine Website, aber sie bringt kaum Anfragen",
     "seiten": "Analyse Ihrer bestehenden Seite, ohne Umsetzung",
     "nutzen": "Ich prüfe Ihre bestehende Website und schreibe auf, wo Besucher hängen bleiben: Verständlichkeit, Aufbau, Botschaft und Kontaktwege. Sortiert nach Wirkung, damit Sie wissen, was zuerst kommt.",
     "umfang": ["Prüfung von Bedienung, Botschaft und Kontaktwegen", "Probleme nach Priorität sortiert", "Ergebnis schriftlich",
                "keine Umsetzung: Was Sie damit machen, entscheiden Sie"],
     "zahlung": "50 % bei Beauftragung, 50 % bei Übergabe des Ergebnisses"},
    {"id": "website", "name": "B2B-Website", "von": 1500, "bis": 3000, "einheit": "",
     "fuer": "Beratungs- und Dienstleistungsunternehmen, die erklären müssen, was sie tun",
     "seiten": "bis ca. 5–7 Kernseiten",
     "nutzen": "Eine Website, die Ihr Angebot verständlich macht, Vertrauen aufbaut und den Weg zur Anfrage kurz hält. Von der Strategie bis zur Übergabe aus einer Hand.",
     "umfang": ["Strategie-Workshop zu Zielgruppe, Angebot und Botschaft", "Sitemap und Seitenaufbau", "eigenes Designsystem statt Vorlage",
                "bis ca. 5–7 Kernseiten", "responsive Umsetzung in Code", "Basis-SEO: Titel, Beschreibungen, Struktur, Sitemap",
                "Prüfung vor dem Livegang und Übergabe"],
     "zahlung": "40 % zum Start, 30 % nach der Designfreigabe, 30 % vor der Übergabe"},
    {"id": "motion", "name": "Website + Motion", "von": 2500, "bis": 4000, "einheit": "",
     "fuer": "Tech- und SaaS-Unternehmen mit einem Produkt, das man zeigen muss",
     "seiten": "B2B-Website plus Animation",
     "nutzen": "Alles aus der B2B-Website, dazu Bewegung dort, wo sie etwas erklärt: ein Produktablauf, ein Launch-Moment, ein Detail, das man sonst übersieht. Keine Animation als Selbstzweck.",
     "umfang": ["alles aus der B2B-Website", "ausgewählte Animationen auf der Seite", "erklärende Visuals oder Launch-Elemente",
                "Motion im Umfang, der im Angebot steht, keine unbegrenzte Produktion"],
     "zahlung": "40 % zum Start, 30 % nach der Designfreigabe, 30 % vor der Übergabe"},
    {"id": "care", "name": "Care", "von": 100, "bis": 250, "einheit": "monat",
     "fuer": "Für Websites, die nach dem Livegang weiter arbeiten sollen",
     "seiten": "laufende Betreuung mit festem Umfang",
     "nutzen": "Ihre Website bleibt technisch in Ordnung, und kleine Änderungen sind schnell erledigt. Was genau dazugehört, steht im Vertrag.",
     "umfang": ["monatlicher technischer Check", "Updates und Sicherungen nach vereinbartem Setup", "Prüfung von Erreichbarkeit und Formular",
                "kleine Inhaltsänderungen im vereinbarten Umfang", "kurzes Protokoll jeden Monat", "keine Bereitschaft rund um die Uhr"],
     "zahlung": "monatlich im Voraus"},
    {"id": "addons", "name": "Add-ons", "von": 150, "bis": 600, "einheit": "",
     "fuer": "Erweiterungen mit klarem Umfang, auch für bestehende Seiten",
     "seiten": "einzeln, nach Umfang",
     "nutzen": "Kleine, klar umrissene Erweiterungen. Jede bekommt einen eigenen Preis, bevor ich anfange.",
     "umfang": ["zusätzliche Landingpage", "einzelnes Motion-Asset", "weitere Sprache", "eine gezielte Verbesserung, die mehr Anfragen bringen soll"],
     "zahlung": "50 % bei Beauftragung, 50 % vor dem Livegang"},
]

AUSSCHLUESSE = [
    ("Unbegrenzte Änderungsrunden.", "Wie viele Runden enthalten sind, steht im Angebot. Weitere rechne ich gesondert ab."),
    ("Texte, Integrationen und Shop-Funktionen ohne Vereinbarung.", "Was davon gebraucht wird, kommt als eigener Posten ins Angebot."),
    ("Kosten von Dritten.", "Hosting, Lizenzen, Stockfotos, Übersetzung und laufende SEO-Arbeit weise ich getrennt aus."),
    ("Wartezeit auf Inhalte.", "Sie liefern Inhalte und Feedback zu den vereinbarten Terminen. Kommt etwas später, verschiebt sich der Livegang."),
]

ABLAUF = [
    ("Erstgespräch", "30 Minuten, kostenlos. Anlass, Ziel, Zeitrahmen und Budget. Wenn es nicht passt, sage ich das offen."),
    ("Angebot und Vertrag", "Ein Festpreis mit schriftlichem Umfang. Mit der Anzahlung startet das Projekt."),
    ("Workshop und Struktur", "Wir klären Zielgruppe, Angebot und Botschaft. Daraus entstehen Sitemap und Inhalte."),
    ("Design zur Freigabe", "Sie sehen die Gestaltung, bevor ich programmiere. Ohne Ihr Okay geht es nicht weiter."),
    ("Umsetzung und Prüfung", "Ich baue in Code und prüfe auf echten Geräten: Links, Formulare, Ladezeit, Barrierefreiheit."),
    ("Livegang und Übergabe", "Nach Ihrer Abnahme geht die Seite online. Sie bekommen alle Zugänge."),
]

ZAHLUNG_TEXT = ("Website-Projekte: 40 % zum Start, 30 % nach der Designfreigabe, 30 % vor der Übergabe. "
                "Website-Check und Add-ons: 50 % bei Beauftragung, 50 % bei Übergabe. Care wird monatlich im Voraus verrechnet.")
PREIS_HINWEIS = ("Alle Preise sind Endpreise. Als Kleinunternehmer (§ 6 Abs. 1 Z 27 UStG) verrechne ich keine Umsatzsteuer.")

# Seiten, die in Navigation und Fuß vorkommen: (Pfad, Text)
NAV = [("/arbeiten/", "Arbeiten"), ("/leistungen/", "Leistungen & Preise"), ("/ueber-mich/", "Über mich"), ("/kontakt/", "Kontakt")]
FUSS_SEITEN = [("/arbeiten/", "Arbeiten"), ("/leistungen/", "Leistungen & Preise"), ("/ueber-mich/", "Über mich"), ("/kontakt/", "Kontakt")]

# --- Englische Fassung der Leistungen (Preise und Bedingungen wie oben) ------------
_EN = {
    "check": {"name": "Website check", "fuer": "You have a website, but it hardly brings in enquiries",
              "seiten": "Analysis of your existing site, no implementation",
              "nutzen": "I review your existing website and write down where visitors get stuck: clarity, structure, message and ways to get in touch. Sorted by impact, so you know what comes first.",
              "umfang": ["Review of usability, message and contact paths", "Problems sorted by priority", "Results in writing",
                         "No implementation: what you do with it is your call"],
              "zahlung": "50 % on order, 50 % on delivery of the results"},
    "website": {"name": "B2B website", "fuer": "Consulting and service firms that need to explain what they do",
                "seiten": "up to approx. 5–7 core pages",
                "nutzen": "A website that makes your offer clear, builds trust and keeps the path to an enquiry short. From strategy to handover, from one person.",
                "umfang": ["Strategy workshop on audience, offer and message", "Sitemap and page structure", "Your own design system instead of a template",
                           "up to approx. 5–7 core pages", "Responsive build in code", "Basic SEO: titles, descriptions, structure, sitemap",
                           "Testing before launch and handover"],
                "zahlung": "40 % at start, 30 % after design approval, 30 % before handover"},
    "motion": {"name": "Website + Motion", "fuer": "Tech and SaaS companies with a product that needs showing",
               "seiten": "B2B website plus animation",
               "nutzen": "Everything in the B2B website, plus motion where it explains something: a product flow, a launch moment, a detail you would otherwise miss. No animation for its own sake.",
               "umfang": ["Everything in the B2B website", "Selected animations on the site", "Explanatory visuals or launch elements",
                          "Motion in the scope set out in the quote, no unlimited production"],
               "zahlung": "40 % at start, 30 % after design approval, 30 % before handover"},
    "care": {"name": "Care", "fuer": "For websites that should keep working after launch",
             "seiten": "ongoing care with a fixed scope",
             "nutzen": "Your website stays in good technical shape, and small changes are done quickly. What exactly is included is set out in the contract.",
             "umfang": ["Monthly technical check", "Updates and backups for the agreed setup", "Uptime and form check",
                        "Small content changes within the agreed scope", "Short report every month", "No 24/7 on-call service"],
             "zahlung": "monthly in advance"},
    "addons": {"name": "Add-ons", "fuer": "Extensions with a clear scope, also for existing sites",
               "seiten": "one by one, by scope",
               "nutzen": "Small, clearly defined extensions. Each gets its own price before I start.",
               "umfang": ["Additional landing page", "Single motion asset", "Another language", "A targeted improvement meant to bring more enquiries"],
               "zahlung": "50 % on order, 50 % before launch"},
}
PAKETE_EN = [dict(p, **_EN[p["id"]]) for p in PAKETE]


def pakete():
    return PAKETE_EN if LANG == "en" else PAKETE


AUSSCHLUESSE_EN = [
    ("Unlimited revision rounds.", "The quote states how many rounds are included. Further rounds are billed separately."),
    ("Copy, integrations and shop features without agreement.", "Whatever is needed goes into the quote as its own item."),
    ("Third-party costs.", "Hosting, licences, stock photos, translation and ongoing SEO work are listed separately."),
    ("Waiting for content.", "You deliver content and feedback on the agreed dates. If something comes later, the launch moves."),
]

ABLAUF_EN = [
    ("Intro call", "30 minutes, free. Occasion, goal, timeframe and budget. If it is not a fit, I will say so openly."),
    ("Quote and contract", "A fixed price with a written scope. The project starts with the deposit."),
    ("Workshop and structure", "We clarify audience, offer and message. The sitemap and content come out of that."),
    ("Design for approval", "You see the design before I code. Nothing moves on without your OK."),
    ("Build and testing", "I build in code and test on real devices: links, forms, load time, accessibility."),
    ("Launch and handover", "After your sign-off the site goes live. You get all access details."),
]

ZAHLUNG_TEXT_EN = ("Website projects: 40 % at start, 30 % after design approval, 30 % before handover. "
                   "Website check and add-ons: 50 % on order, 50 % on delivery. Care is billed monthly in advance.")
PREIS_HINWEIS_EN = ("All prices are final prices. As a small business under § 6 (1) no. 27 of the Austrian VAT Act (UStG) I do not charge VAT.")

NAV_EN = [("/arbeiten/", "Work"), ("/leistungen/", "Services & pricing"), ("/ueber-mich/", "About"), ("/kontakt/", "Contact")]
FUSS_SEITEN_EN = [("/arbeiten/", "Work"), ("/leistungen/", "Services & pricing"), ("/ueber-mich/", "About"), ("/kontakt/", "Contact")]

# --- Bilder --------------------------------------------------------------------

_MANIFEST = None


def manifest():
    global _MANIFEST
    if _MANIFEST is None:
        p = os.path.join(BASIS, "_bilder.json")
        _MANIFEST = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _MANIFEST


def bild(name, alt, sizes, lazy=True, prio=False, klasse="", plat=True):
    """<picture> mit AVIF, WebP und JPEG. Unterhalb des ersten Schirms mit Platzhalter (siehe stil.css)."""
    m = manifest()[name]
    br = m["breiten"]
    def ss(ext):
        return ", ".join(f"/assets/img/{name}-{b}.{ext} {b}w" for b in br)
    jb = m["jpg"]
    h = round(jb * m["h"] / m["w"])
    a = f' loading="lazy"' if lazy and not prio else ""
    a += ' fetchpriority="high"' if prio else ""
    marke = f"{name}-{br[-1]}.webp, {br[-1]}×{round(br[-1] * m['h'] / m['w'])}"
    dat = f' data-bild="{e(marke)}"' if plat and lazy and not prio else ""
    k = "bild" + (f" {klasse}" if klasse else "")
    return (f'<picture class="{k}"{dat}>'
            f'<source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="/assets/img/{name}-{jb}.jpg" width="{jb}" height="{h}" alt="{e(alt)}"{a} decoding="async">'
            f'</picture>')


def bild_werk(name, alt, sizes, prio=False):
    """Aufnahme einer Arbeit: am Handy die Handy-Fassung (4:5), sonst die Desktop-Fassung (16:10).
    Breite und Höhe stehen am img, damit beim Laden nichts verrutscht; CSS setzt das Seitenverhältnis je Bildschirm."""
    m = manifest()
    d, h = m[name + "-d"], m[name + "-m"]
    def ss(mm, nm, ext):
        return ", ".join(f"/assets/img/{nm}-{b}.{ext} {b}w" for b in mm["breiten"])
    a = ' fetchpriority="high"' if prio else ' loading="lazy"'
    jb = d["jpg"]
    hh = round(jb * d["h"] / d["w"])
    return (f'<picture class="bild werk-aufnahme">'
            f'<source media="(max-width: 767px)" type="image/avif" srcset="{ss(h, name + "-m", "avif")}" sizes="calc(100vw - 40px)">'
            f'<source media="(max-width: 767px)" type="image/webp" srcset="{ss(h, name + "-m", "webp")}" sizes="calc(100vw - 40px)">'
            f'<source type="image/avif" srcset="{ss(d, name + "-d", "avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss(d, name + "-d", "webp")}" sizes="{sizes}">'
            f'<img src="/assets/img/{name}-d-{jb}.jpg" width="{jb}" height="{hh}" alt="{e(alt)}"{a} decoding="async">'
            f'</picture>')


def schieber(alt_roh, alt_fertig, marke_roh, marke_fertig, regler):
    """Vorher/Nachher: unten die fertige Seite, darüber die Rohfassung, links von der Linie sichtbar.
    Die Linie sitzt bei --x (ohne JS 50 %). Gezogen wird mit Maus oder Finger, die Tastatur bedient den Regler."""
    sizes = "(min-width: 1440px) 1312px, (min-width: 1024px) calc(100vw - 128px), calc(100vw - 80px)"
    return (f'<figure class="schieber" data-schieber>'
            f'<div class="sch-flaeche">'
            f'<div class="sch-bild sch-fertig">{bild_werk("vn-fertig", alt_fertig, sizes)}'
            f'<span class="sch-marke sch-m-fertig" aria-hidden="true">{e(marke_fertig)}</span></div>'
            f'<div class="sch-bild sch-roh">{bild_werk("vn-roh", alt_roh, sizes)}'
            f'<span class="sch-marke sch-m-roh" aria-hidden="true">{e(marke_roh)}</span></div>'
            f'<div class="sch-linie" aria-hidden="true"><span class="sch-griff"></span></div>'
            f'</div>'
            f'<input class="sch-regler" type="range" min="0" max="100" value="50" step="1" aria-label="{e(regler)}">'
            f'</figure>')


def werke(liste, titel_id, kopf_html, mehr_html=""):
    """Die Arbeiten als große Aufnahmen auf der dunklen Fläche. liste: [{id, titel, echt, art, beleg, href, oeffnen, oeffnen_url,
    paket (Paket-Dict), alt}]. Die erste Arbeit steht in voller Breite, die zwei anderen versetzt nebeneinander."""
    ab = tr("ab", "from")
    groessen = ["(min-width: 1440px) 1312px, (min-width: 1024px) calc(100vw - 128px), calc(100vw - 80px)",
                "(min-width: 1440px) 760px, (min-width: 1024px) 53vw, calc(100vw - 80px)",
                "(min-width: 1440px) 540px, (min-width: 1024px) 38vw, calc(100vw - 80px)"]
    teile = ""
    for i, k in enumerate(liste):
        marke = tr("Echtes Projekt", "Real project") if k["echt"] else tr("Konzept-Demo", "Concept demo")
        beleg = f'<p class="werk-beleg">{k["beleg"]}</p>' if k.get("beleg") else ""
        teile += f'''<article class="werk werk-{i + 1}" aria-labelledby="werk-{k["id"]}">
    <a class="werk-bild" href="{P(k["href"])}" tabindex="-1" aria-hidden="true">{bild_werk("werk-" + k["id"], k["alt"], groessen[min(i, 2)])}</a>
    <div class="werk-info">
      <h3 class="werk-name" id="werk-{k["id"]}"><a href="{P(k["href"])}">{e(k["titel"])}</a></h3>
      <p class="werk-art">{e(k["art"])}</p>
      {beleg}
      <dl class="werk-daten"><div><dt>{tr("Art", "Type")}</dt><dd>{marke}</dd></div></dl>
      <p class="werk-wege">{textlink(k["oeffnen"], k["oeffnen_url"], extern=True)} {textlink(tr("Wie ich sie gebaut habe", "How I built it"), k["href"])}</p>
    </div>
  </article>'''
    return f'''<div class="wrap">
  <header class="werke-kopf">{kopf_html}</header>
  <div class="werke">{teile}</div>
  {mehr_html}
</div>'''


# --- Bausteine -----------------------------------------------------------------

def knopf(text, href, art="", pfeil=False, extern=False):
    """Pfeil nur, wenn der Knopf die Seite verlässt (↗); interne Ziele bekommen keinen."""
    k = "knopf" + (f" {art}" if art else "")
    ziel = ' target="_blank" rel="noopener noreferrer"' if extern else ""
    p = ' <span class="pfeil" aria-hidden="true">↗</span>' if extern else ""
    return f'<a class="{k}" href="{P(href)}"{ziel}>{text}{p}</a>'


def textlink(text, href, extern=False, etikett=""):
    z = ' target="_blank" rel="noopener noreferrer"' if extern else ""
    et = f' data-zeiger="{e(etikett)}"' if etikett else ""
    return f'<a class="tl" href="{P(href)}"{z}{et}>{text}</a>'


def preis_text(p):
    """Preisspanne, z. B. „1.500–3.000 €“ oder „100–250 €/Monat“ (geschützte Leerzeichen, damit nichts umbricht)."""
    if LANG == "en":
        t = f"€{p['von']:,}–{p['bis']:,}"
    else:
        t = f"{p['von']:,}–{p['bis']:,}".replace(",", ".") + "\u00a0€"
    if p.get("einheit") == "monat":
        t += tr("/Monat", "/month")
    return t


def paket_karte(p, detail=False):
    """Karte mit Preisspanne. Mit detail=True klappt „Dafür bekommen Sie“ auf (details, geht ohne JavaScript)."""
    kopf = f'''<h3 class="karte-name">{e(p["name"])}</h3>
      <p class="karte-preis">{preis_text(p)}</p>
      <p class="karte-fuer">{e(p["fuer"])}</p>
      <ul class="karte-liste"><li>{e(p["seiten"])}</li></ul>'''
    if detail:
        umf = "".join(f"<li>{e(x)}</li>" for x in p["umfang"])
        return f'''<article class="karte" id="{p["id"]}">
      {kopf}
      <details class="karte-auf"><summary><span>{tr("Dafür bekommen Sie", "What you get")}</span></summary>
        <div class="karte-auf-inhalt">
          <p>{e(p["nutzen"])}</p>
          <h4>{tr("Enthalten", "Included")}</h4>
          <ul>{umf}</ul>
          <p class="klein">{tr("Zahlung", "Payment")}: {e(p["zahlung"])}.</p>
        </div>
      </details>
      {knopf(tr("Erstgespräch anfragen", "Book an intro call"), "/kontakt/?paket=" + p["id"], "knopf-2")}
    </article>'''
    return f'''<article class="karte" id="{p["id"]}">
      {kopf}
    </article>'''


def datenblatt(pk):
    """Leistungen als Datenblatt: eine Zeile je Leistung. Am Handy wird jede Zeile ein Block mit Beschriftungen."""
    L = {"p": tr("Leistung", "Service"), "u": tr("Umfang", "Scope"), "pr": tr("Preis", "Price")}
    zeilen = ""
    for p in pk:
        zeilen += (f'<tr id="{p["id"]}-zeile"><th scope="row"><a class="db-name" href="{P("/leistungen/#" + p["id"])}">{e(p["name"])}</a>'
                   f'<span class="db-fuer">{e(p["fuer"])}</span></th>'
                   f'<td data-l="{L["u"]}">{e(p["seiten"])}</td>'
                   f'<td class="db-preis" data-l="{L["pr"]}"><span>{preis_text(p)}</span></td></tr>')
    cap = tr("Die Leistungen im Überblick", "The services at a glance")
    return (f'<div class="tab-wrap"><table class="datenblatt datenblatt-drei"><caption class="nur-leser">{cap}</caption><thead><tr>'
            f'<th scope="col">{L["p"]}</th><th scope="col">{L["u"]}</th>'
            f'<th scope="col">{L["pr"]}</th></tr></thead><tbody>{zeilen}</tbody></table></div>')


def ausschluesse():
    li = "".join(f"<li><strong>{e(t)}</strong> {e(x)}</li>" for t, x in (AUSSCHLUESSE_EN if LANG == "en" else AUSSCHLUESSE))
    return f'<ul class="betreuung-liste">{li}</ul>'


def reel():
    """Motion-Reel: lädt erst, wenn es in die Nähe kommt (JS setzt src), spielt stumm in Schleife, Ton auf Knopfdruck.
    Am Handy die kleinere Datei. Ohne JS: Poster, Steuerelemente und beide Quellen."""
    m = manifest().get("reel-poster")
    poster = f"/assets/img/reel-poster-{m['jpg']}.jpg" if m else ""
    return f'''<figure class="reel" data-reel>
      <div class="reel-rahmen">
        <video class="reel-video" muted loop playsinline preload="none" tabindex="0" role="button" poster="{poster}" width="1656" height="932"
               data-src-gross="/assets/video/reel-1656.mp4" data-src-klein="/assets/video/reel-960.mp4"
               aria-label="{tr("Motion-Reel von Simon Monu, 15 Sekunden. Klicken für Vollbild mit Ton", "Motion reel by Simon Monu, 15 seconds. Click for full screen with sound")}">
          <source src="/assets/video/reel-960.mp4" type="video/mp4">
        </video>
        <button class="reel-ton" type="button" data-reel-ton aria-pressed="false">{tr("Ton an", "Sound on")}</button>
      </div>
    </figure>'''


def ablauf_schiene():
    """Schritte des Ablaufs als Liste."""
    li = "".join(f'''<li><h3>{e(t)}</h3><p>{e(x)}</p></li>'''
                 for t, x in (ABLAUF_EN if LANG == "en" else ABLAUF))
    return f'<ol class="schiene" data-stagger>{li}</ol>'


def ring_svg(monat):
    """Zwölf Monate im Kreis, der nächste freie Start markiert. Nur SVG-Attribute (keine Inline-Styles).
    monat steht immer deutsch in NAECHSTER_START; angezeigt wird der Monat in der Sprache der Seite."""
    import math
    if monat not in MONATE:
        return ""
    idx = MONATE.index(monat)
    kurz = KURZ_EN if LANG == "en" else KURZ
    name = (MONATE_EN if LANG == "en" else MONATE)[idx]
    cx = cy = 150
    r = 112
    teile = []
    for i, k in enumerate(kurz):
        w = math.radians(-90 + i * 30)
        x = cx + r * math.cos(w)
        y = cy + r * math.sin(w)
        cls = "ring-m ring-jetzt" if i == idx else "ring-m"
        teile.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="central">{k}</text>')
        if i == idx:
            teile.append(f'<circle class="ring-punkt" cx="{cx + (r + 26) * math.cos(w):.1f}" cy="{cy + (r + 26) * math.sin(w):.1f}" r="4"/>')
    teile.append(f'<circle class="ring-kreis" cx="{cx}" cy="{cy}" r="{r + 26}" fill="none"/>')
    return f'''<figure class="ring" data-ring>
      <svg class="ring-svg" viewBox="0 0 300 300" role="img" aria-label="{tr("Nächster freier Projektstart", "Next free project start")}: {e(name)}">
        <g class="ring-drehen" data-drehen>{"".join(teile)}</g>
        <text class="ring-klein" x="150" y="138" text-anchor="middle">{tr("Nächster freier Start", "Next free start")}</text>
        <text class="ring-gross" x="150" y="168" text-anchor="middle">{e(name)}</text>
      </svg>
    </figure>'''


def fenster(eintraege, titel_id=""):
    """Schaufenster: die Arbeiten laufen live in einem Fenster und lassen sich darin bedienen.
    eintraege: [{id, name, marke, src, url_anzeige, text, case}]. Mehrere Einträge werden zu Reitern.
    Das iframe bekommt seine Adresse erst per JavaScript (data-src): Es lädt nur, was sichtbar ist, und die
    Adresse passt auch, wenn die Seite per Doppelklick geöffnet wurde."""
    mehrere = len(eintraege) > 1
    ab = tr("ab", "from")
    reiter = ""
    if mehrere:
        knoepfe = "".join(
            f'<button class="reiter" type="button" role="tab" id="reiter-{x["id"]}" aria-controls="tafel-{x["id"]}" '
            f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-reiter>'
            f'<span class="reiter-name">{e(x["name"])}</span>'
            f'<span class="reiter-marke">{e(x["marke"])}</span></button>'
            for i, x in enumerate(eintraege))
        lab = f' aria-labelledby="{titel_id}"' if titel_id else f' aria-label="{tr("Arbeiten zum Ausprobieren", "Work to try out")}"'
        reiter = f'<div class="reiter-liste" role="tablist"{lab}>{knoepfe}</div>'
    tafeln = ""
    for i, x in enumerate(eintraege):
        rolle = f' role="tabpanel" id="tafel-{x["id"]}" aria-labelledby="reiter-{x["id"]}"' if mehrere else ""
        versteckt = " hidden" if (mehrere and i > 0) else ""
        ziel = x.get("oeffnen_url") or x["src"]
        neu = textlink(x["oeffnen"] if ziel.startswith("http") else tr("In neuem Tab öffnen ↗", "Open in a new tab ↗"), ziel, extern=True,
                       etikett=tr("Öffnet neu ↗", "Opens in a new tab ↗"))
        case = f' {textlink(tr("Wie ich sie gebaut habe", "How I built it"), x["case"])}' if x.get("case") else ""
        # Paket: bei Reitern steht es im Reiter, bei einem einzelnen Fenster darüber. Unten jeweils der Weg zum Paket.
        paket_oben = (f'<p class="fenster-paket">{tr("Entspricht dem Paket", "Corresponds to the package")} <a href="{P("/leistungen/#" + x["paket_id"])}">'
                      f'{e(x["paket"])}, {ab} {x["paket_ab"]}</a></p>') if (x.get("paket") and not mehrere) else ""
        paket_link = (f' {textlink(tr("Was im Paket " + x["paket"] + " drin ist", "What is in the " + x["paket"] + " package"), "/leistungen/#" + x["paket_id"])}'
                      if (x.get("paket") and mehrere) else "")
        tafeln += f'''<div class="tafel"{rolle}{versteckt} data-tafel>
      {paket_oben}<div class="fenster-rahmen">
        <div class="fenster-leiste"><span class="fenster-url">{e(x["url_anzeige"])}</span><span class="fenster-live">live</span></div>
        <div class="fenster-bild" data-fenster-bild>
          <iframe title="{e(x["name"])}, {e(x["marke"])}, live" data-src="{e(x["src"])}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
          <button class="fenster-tippen" type="button" data-tippen>{tr("Zum Ausprobieren klicken oder tippen", "Click or tap to try it out")}</button>
          <noscript><p class="fenster-ohne">{textlink(tr("Seite öffnen", "Open page"), x["src"])}</p></noscript>
        </div>
      </div>
      <div class="fenster-info">
        <p class="fenster-text">{e(x["text"])}</p>
        <p class="fenster-links">{neu}{case}{paket_link}</p>
      </div>
    </div>'''
    return f'<div class="fenster{" fenster-reiter" if mehrere else ""}" data-fenster>{reiter}{tafeln}</div>'


def formular(paket=""):
    """Kontaktformular. Ohne JavaScript und ohne Formspree-Adresse: mailto-Rückfall."""
    opts = [("", tr("noch offen", "not decided yet"))] + [(x["id"], x["name"]) for x in pakete()]
    o = "".join(f'<option value="{v}"{" selected" if v == paket else ""}>{e(t)}</option>' for v, t in opts)
    def auswahl(i, name, werte):
        return (f'<div class="feld"><label for="f-{i}">{name}</label><select id="f-{i}" name="{name}">'
                + "".join(f"<option>{e(w)}</option>" for w in werte) + '</select></div>')
    anlass = auswahl("anlass", tr("Anlass", "Occasion"), [tr("bitte wählen", "please choose"), tr("Neue Website", "New website"),
                     tr("Relaunch der bestehenden Seite", "Relaunch of the current site"), tr("Neues Angebot oder Produktlaunch", "New offer or product launch"),
                     tr("Landingpage oder Kampagne", "Landing page or campaign"), tr("Website-Check", "Website check"), tr("Etwas anderes", "Something else")])
    budget = auswahl("budget", tr("Budget", "Budget"), [tr("bitte wählen", "please choose"), tr("unter 1.500 €", "under €1,500"), "1.500–3.000\u00a0€" if LANG != "en" else "€1,500–3,000",
                     "3.000–4.000\u00a0€" if LANG != "en" else "€3,000–4,000", tr("über 4.000 €", "over €4,000"), tr("noch offen", "not decided yet")])
    zeit = auswahl("zeit", tr("Zeitraum", "Timeframe"), [tr("bitte wählen", "please choose"), tr("so bald wie möglich", "as soon as possible"),
                   tr("in 1–3 Monaten", "in 1–3 months"), tr("in 3–6 Monaten", "in 3–6 months"), tr("noch offen", "not decided yet")])
    if FORMSPREE:
        aktion = f'action="{e(FORMSPREE)}" method="post"'
        dat = f' data-endpoint="{e(FORMSPREE)}"'
    else:
        aktion = f'action="mailto:{MAIL}" method="post" enctype="text/plain"'
        dat = ""
    n_name, n_mail, n_firma, n_paket, n_text = (tr("Name", "Name"), tr("E-Mail", "Email"), tr("Betrieb oder Projekt", "Business or project"),
                                               tr("Leistung", "Service"), tr("Nachricht", "Message"))
    hinweis = (tr("Ihre Angaben gehen über den Formulardienst Formspree an mich. Mehr dazu im ",
                  "Your details reach me through the form service Formspree. More in the ") if FORMSPREE else
               tr("Das Formular öffnet Ihr E-Mail-Programm. Mehr dazu im ", "The form opens your email program. More in the "))
    return f'''<form class="formular" {aktion}{dat} data-formular novalidate>
      <div class="feld"><label for="f-name">{n_name}</label><input id="f-name" name="{n_name}" type="text" autocomplete="name" required></div>
      <div class="feld"><label for="f-mail">{n_mail}</label><input id="f-mail" name="{n_mail}" type="email" autocomplete="email" required></div>
      <div class="feld feld-breit"><label for="f-firma">{n_firma}</label><input id="f-firma" name="{n_firma}" type="text" autocomplete="organization"></div>
      <div class="feld"><label for="f-paket">{n_paket}</label><select id="f-paket" name="{n_paket}">{o}</select></div>
      {anlass}{budget}{zeit}
      <div class="feld feld-breit"><label for="f-text">{n_text}</label><textarea id="f-text" name="{n_text}" rows="5" required></textarea></div>
      <div class="feld falle" aria-hidden="true"><label for="f-web">{tr("Bitte leer lassen", "Please leave empty")}</label><input id="f-web" name="_gotcha" type="text" tabindex="-1" autocomplete="off"></div>
      <div class="formular-fuss">
        <button class="knopf" type="submit">{tr("Erstgespräch anfragen", "Book an intro call")}</button>
        <p class="klein">{hinweis}<a href="{P("/datenschutz/")}">{tr("Datenschutz", "privacy policy")}</a>.</p>
      </div>
      <p class="formular-meldung" role="status" aria-live="polite" data-meldung></p>
    </form>'''


def direkt_block():
    tel = (f'<li><span class="direkt-titel">{tr("Telefon", "Phone")}</span><a href="{telefon_href()}">{e(TELEFON)}</a></li>' if TELEFON else "")
    return f'''<ul class="direkt">
      <li><span class="direkt-titel">{tr("E-Mail", "Email")}</span><a href="mailto:{MAIL}">{MAIL}</a></li>{tel}
      <li><span class="direkt-titel">{tr("Antwort", "Reply")}</span>{tr("innerhalb von zwei Werktagen", "within two working days")}</li>
    </ul>'''


def kopfzeile(pfad):
    en = LANG == "en"
    def cur(p):
        return ' aria-current="page"' if pfad == p or (p != "/" and pfad.startswith(p)) else ""
    links = "".join(f'<a href="{P(p)}"{cur(P(p))}>{t.replace("&", "&amp;")}</a>' for p, t in (NAV_EN if en else NAV))
    gg = gegenstueck(pfad)
    sprache = sprache_menue = ""
    if gg and en:
        sprache = f'<a class="kopf-sprache" href="{gg[0]}" hreflang="de-AT" lang="de" aria-label="Deutsche Version">DE</a>'
        sprache_menue = f'<a class="menue-sprache" href="{gg[0]}" hreflang="de-AT" lang="de">Deutsch</a>'
    elif gg:
        sprache = f'<a class="kopf-sprache" href="{gg[1]}" hreflang="en" lang="en" aria-label="English version">EN</a>'
        sprache_menue = f'<a class="menue-sprache" href="{gg[1]}" hreflang="en" lang="en">English</a>'
    return f'''<header class="kopf" data-kopf>
  <a class="kopf-name" href="{P("/")}" aria-label="{tr("Simon Monu, zur Startseite", "Simon Monu, home")}">{_wortmarke()}</a>
  <nav class="kopf-nav" aria-label="{tr("Hauptmenü", "Main menu")}">{links}</nav>
  {sprache}<a class="knopf knopf-klein kopf-cta" href="{P("/kontakt/")}">{tr("Erstgespräch", "Intro call")}</a>
  <details class="menue" data-menue>
    <summary><span>{tr("Menü", "Menu")}</span><i aria-hidden="true"></i></summary>
    <div class="menue-blatt">
      <nav aria-label="{tr("Hauptmenü, mobil", "Main menu, mobile")}">{links}{sprache_menue}</nav>
    </div>
  </details>
</header>'''


def fusszeile():
    en = LANG == "en"
    seiten = "".join(f'<li><a href="{P(p)}">{t.replace("&", "&amp;")}</a></li>' for p, t in (FUSS_SEITEN_EN if en else FUSS_SEITEN))
    tel = f'<li><a href="{telefon_href()}">{e(TELEFON)}</a></li>' if TELEFON else ""
    soc = ""
    if INSTAGRAM: soc += f'<li><a href="{e(INSTAGRAM)}" target="_blank" rel="noopener noreferrer">Instagram</a></li>'
    if LINKEDIN: soc += f'<li><a href="{e(LINKEDIN)}" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>'
    return f'''<footer class="fuss">
  <div class="wrap raster fuss-oben">
    <div class="fuss-marke">
      <p class="fuss-name"><span class="nur-leser">Simon Monu</span>{_wortmarke()}</p>
      <p>{tr("B2B-Websites für Beratungs- und Technologieunternehmen in Wien und Salzburg. Strategie, Design, Motion und Code von einer Person.",
             "B2B websites for consulting and technology companies in Vienna and Salzburg. Strategy, design, motion and code from one person.")}</p>
    </div>
    <nav class="fuss-spalte fuss-seiten" aria-label="{tr("Seiten", "Pages")}"><h2 class="fuss-titel">{tr("Seiten", "Pages")}</h2><ul>{seiten}</ul></nav>
    <nav class="fuss-spalte fuss-recht" aria-label="{tr("Rechtliches", "Legal")}"><h2 class="fuss-titel">{tr("Rechtliches", "Legal")}</h2><ul><li><a href="{P("/impressum/")}">{tr("Impressum", "Legal notice")}</a></li><li><a href="{P("/datenschutz/")}">{tr("Datenschutz", "Privacy")}</a></li></ul></nav>
    <div class="fuss-spalte fuss-kontakt"><h2 class="fuss-titel">{tr("Kontakt", "Contact")}</h2><ul><li><a href="mailto:{MAIL}">{MAIL}</a></li>{tel}{soc}</ul></div>
  </div>
  <div class="wrap fuss-unten">
    <button class="thema" type="button" data-thema aria-label="{tr("Darstellung wechseln: System, hell, dunkel", "Switch appearance: system, light, dark")}"><span data-thema-text>{tr("Darstellung: System", "Appearance: System")}</span></button>
    <p class="fuss-c">© 2026 Simon Monu</p>
  </div>
</footer>'''


def json_ld(daten):
    return '<script type="application/ld+json">' + json.dumps(daten, ensure_ascii=False, separators=(",", ":")) + "</script>"


def krumel(pfad, titel):
    en = LANG == "en"
    teile = [(tr("Start", "Home"), DOMAIN + P("/"))]
    segs = [s for s in pfad.strip("/").split("/") if s]
    if en and segs and segs[0] == "en":
        segs = segs[1:]
    if segs:
        namen = {"arbeiten": "Arbeiten", "leistungen": "Leistungen und Preise", "handwerk": "Für Handwerksbetriebe",
                 "ueber-mich": "Über mich", "kontakt": "Kontakt", "nickmonu": "nickmonu.com", "hallwirth": "Tischlerei Hallwirth",
                 "lindtner": "Vera Lindtner Coaching", "impressum": "Impressum", "datenschutz": "Datenschutz"}
        namen_en = {"work": "Work", "services": "Services and pricing", "trades": "For trades businesses", "about": "About",
                    "contact": "Contact", "nickmonu": "nickmonu.com", "hallwirth": "Tischlerei Hallwirth",
                    "lindtner": "Vera Lindtner Coaching", "legal-notice": "Legal notice", "privacy": "Privacy"}
        acc = "/en" if en else ""
        for s in segs:
            acc += "/" + s
            teile.append(((namen_en if en else namen).get(s, titel), DOMAIN + acc + "/"))
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": u} for i, (n, u) in enumerate(teile, 1)]}


# Startansicht: liegt im HTML, damit sie mit dem ersten Bild steht. Sichtbar nur mit html.intro (frueh.js).
def stueckliste():
    return ('<div class="stueckliste" aria-hidden="true" data-stueckliste>'
            f'<p class="st-kopf"><span>Simon Monu</span><span>{tr("Diese Seite wird geladen", "This page is loading")}</span></p>'
            f'<p class="st-name">Simon Monu<span>{tr("Webdesign", "Web design")}</span></p>'
            '<div class="st-unten"><ul class="st-liste" data-st-liste></ul>'
            '<div class="st-balken"><span data-st-balken></span></div>'
            f'<p class="st-fuss"><span>{tr("Jede Datei dieser Seite, so wie sie bei Ihnen ankommt", "Every file of this page, as it arrives on your device")}</span><span data-st-summe></span></p></div>'
            '</div>\n')


def seite(pfad, titel, beschreibung, inhalt, start=False, og="start", robots="index, follow", jsonld=None, klasse="", fruehe_bilder=(), fonts=(), weiter=""):
    """Vollständige HTML-Seite. Platzhalter @@N@@ und @@KB@@ füllt bau.py."""
    url = DOMAIN + (pfad if pfad.endswith("/") or pfad.endswith(".html") else pfad + "/")
    if pfad == "/":
        url = DOMAIN + "/"
    if weiter:
        url = DOMAIN + weiter
    volltitel = titel if titel.startswith("Simon Monu") else f"{titel} · Simon Monu"
    ld = jsonld or []
    if pfad not in ("/", "/en/") and not pfad.endswith(".html"):
        ld = ld + [krumel(pfad, titel)]
    ldh = "\n".join(json_ld(x) for x in ld)
    pre = "".join(f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n' for f in fonts)
    ds = " data-start" if start else ""
    kl = f' class="{klasse}"' if klasse else ""
    gg = gegenstueck(pfad)
    alt = ""
    if gg:
        alt = (f'<link rel="alternate" hreflang="de-AT" href="{DOMAIN}{gg[0]}">\n'
               f'<link rel="alternate" hreflang="en" href="{DOMAIN}{gg[1]}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{gg[0]}">\n')
    return f'''<!DOCTYPE html>
<html lang="{tr("de-AT", "en")}"{ds}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp(meta=True)}">
<title>{e(volltitel)}</title>
<meta name="description" content="{e(beschreibung)}">
<meta name="robots" content="{robots}">{f'<meta http-equiv="refresh" content="0; url={weiter}">' if weiter else ""}
<link rel="canonical" href="{url}">
{alt}<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#F4F4F1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B1426" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:locale" content="{tr("de_AT", "en_GB")}">
<meta property="og:site_name" content="Simon Monu">
<meta property="og:title" content="{e(volltitel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/og/og-{og}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{pre}<link rel="stylesheet" href="/css/stil.css?v={VERSION}">
<script src="/js/frueh.js?v={VERSION}"></script>
{ldh}
</head>
<body{kl}>
{stueckliste() if start else ""}<a class="sprung" href="#inhalt">{tr("Zum Inhalt springen", "Skip to content")}</a>
{kopfzeile(pfad)}
<main id="inhalt" tabindex="-1">
{inhalt}
</main>
{fusszeile()}
<script src="/js/seite.js?v={VERSION}" defer></script>
</body>
</html>
'''
