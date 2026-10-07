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
MAIL = "office@simonmonu.at"

# Stand von CSS/JS. Bei jeder Änderung an css/ oder js/ hochzählen, sonst zeigen
# Browser bis zu einer Woche lang die alte Fassung (Cache-Regel in _headers).
VERSION = "17"

# --- Noch offen (bis zum Livegang eintragen) ----------------------------------
TELEFON = "+43 676 561 8098"            # z. B. "+43 660 1234567"; leer = Telefon wird nirgends angezeigt
FORMSPREE = "https://formspree.io/f/xwlpyyoq"          # z. B. "https://formspree.io/f/abcdwxyz"; leer = mailto-Formular
NAECHSTER_START = os.environ.get("SM_START", "")   # z. B. "November"; leer = Ring entfällt
ANSCHRIFT = {"strasse": "Eichetstrasse 51", "plz": "5071", "ort": "Wals-Siezenheim"}   # Pflicht nach § 5 ECG
UID = ""                # nur eintragen, wenn es eine gibt (z. B. "ATU12345678")
GEWERBE = {"wortlaut": "Werbeagentur", "behoerde": "Bezirkshauptmannschaft Salzburg-Umgebung", "fachgruppe": "Fachgruppe Werbung und Marktkommunikation"}   # genau laut GISA-Auszug
INSTAGRAM = ""          # optional, volle Adresse
LINKEDIN = ""           # optional, volle Adresse

EINFUEHRUNG = True      # Einführungsangebot ein/aus (eine Zeile)
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


# --- Pakete (Preise und Umfang wortgleich aus Webdesign_Pakete_Preise_Kunden_6.pdf) ----

PAKETE = [
    {"id": "onepager", "name": "Onepager", "ab": 950, "einf": 650,
     "fuer": "Personal Brands, Coaches, Events, kleine lokale Betriebe",
     "seiten": "1 Seite mit mehreren Bereichen", "dauer": "ca. 1–2 Wochen",
     "nutzen": "Eine einzige Seite, die sagt, was Sie tun, was es kostet und wie man Sie erreicht. Schnell gebaut, schnell online.",
     "umfang": ["1 Seite mit mehreren Bereichen", "responsives Design", "Basis-SEO (Title und Meta)", "2 Korrekturrunden",
                "Lieferzeit ca. 1–2 Wochen"],
     "optional": "Copywriting, zweite Sprache, Wartung",
     "betreuung": "Optional zubuchbar.",
     "zahlung": "50 % bei Auftragserteilung, 50 % bei Fertigstellung"},
    {"id": "business", "name": "Business-Website", "ab": 2400, "einf": 1500,
     "fuer": "Selbstständige und KMU mit mehreren Angeboten",
     "seiten": "4–7 Unterseiten", "dauer": "ca. 3–5 Wochen", "betreuung_ab": 60,
     "nutzen": "Eine Seite mit 4–7 Unterseiten, die Ihre Angebote einzeln zeigt und am Handy zuerst gebaut ist. Sie sehen das Konzept, bevor ich baue.",
     "umfang": ["4–7 Unterseiten", "Konzept zur Freigabe vor dem Bau", "responsives Design",
                "Pflege-Oberfläche für wiederkehrende Inhalte (auf Wunsch)", "Kontaktformular", "3 Korrekturrunden",
                "Betreuung ab 60 €/Monat gehört dazu (Hosting, kleine Änderungen)", "Lieferzeit ca. 3–5 Wochen"],
     "optional": "zweite Sprache, Copywriting",
     "betreuung": "Mindestlaufzeit 3 Monate, danach monatlich kündbar.",
     "zahlung": "50 % bei Auftragserteilung, 50 % bei Fertigstellung"},
    {"id": "premium", "name": "Premium", "ab": 4800, "einf": None,
     "fuer": "Marken mit hohem Anspruch an Craft, Bewegung, Individualität. So wie diese Seite und nickmonu.com",
     "seiten": "wie Business-Website, mehrsprachig", "dauer": "ca. 5–8 Wochen", "betreuung_ab": 80,
     "nutzen": "Alles aus der Business-Website, dazu Bewegung und Bausteine, die es nur für Ihre Marke gibt. Die Lieferzeit hängt vom Animationsumfang ab.",
     "umfang": ["alles aus Business-Website", "individuelle Animationen (Seitenübergänge, Cursor-Effekte, Lade-Momente)",
                "maßgeschneiderte Komponenten statt Standardbausteinen", "mehrsprachig als Standard", "4 Korrekturrunden",
                "Betreuung ab 80 €/Monat gehört dazu", "Lieferzeit ca. 5–8 Wochen, abhängig vom Animationsumfang"],
     "optional": "Bildproduktion/Fotografie, Copywriting",
     "betreuung": "Mindestlaufzeit 3 Monate, danach monatlich kündbar.",
     "zahlung": "40 % bei Start, 30 % nach Konzept-Freigabe, 30 % bei Fertigstellung"},
    {"id": "shop", "name": "Shop", "ab": 3800, "einf": None,
     "fuer": "Kleine Produktpalette, Markenshop",
     "seiten": "Produktkatalog bis ca. 20 Produkte", "dauer": None, "betreuung_ab": 80,
     "nutzen": "Ein einfacher Markenshop mit überschaubarer Produktzahl. Bei mehr Produkten oder Varianten sage ich Ihnen vorher, welche technische Basis passt.",
     "umfang": ["Produktkatalog bis ca. 20 Produkte", "Checkout", "eine Zahlungsanbindung", "responsives Design", "3 Korrekturrunden",
                "Betreuung ab 80 €/Monat gehört dazu"],
     "optional": None,
     "hinweis": "Bei höherer Komplexität (viele Varianten, internationaler Versand, Lagerhaltung) berate ich ehrlich, welche technische Basis wirklich passt, gegebenenfalls mit einem Individualangebot außerhalb des Fixpakets.",
     "betreuung": "Mindestlaufzeit 3 Monate, danach monatlich kündbar.",
     "zahlung": "40 % bei Start, 30 % nach Konzept-Freigabe, 30 % bei Fertigstellung"},
]

ZUSATZ = [
    ("SEO-Basis-Setup (Meta-Tags, Struktur, Sitemap, Google-Unternehmensprofil)", "250–400 €"),
    ("Copywriting je Unterseite", "60–90 € je Seite"),
    ("Zusätzliche Sprache", "+15–20 % auf den Paketpreis"),
    ("Wartung „Aktiv“: mehr Änderungsvolumen, priorisierte Bearbeitung (Upgrade zur inkludierten Betreuung)", "150 €/Monat"),
    ("Express-Zuschlag (Lieferzeit halbiert)", "+20–30 % auf den Paketpreis"),
]

BETREUUNG_UMFANG = [
    ("Hosting", "Die Seite liegt auf meinem Hosting. Sie kümmern sich um keinen Server und keine Verlängerung."),
    ("Updates und Sicherung", "Was sich ändert, halte ich aktuell. Es gibt jederzeit eine Kopie."),
    ("Erreichbarkeits-Prüfung", "Ein automatischer Check meldet mir, wenn die Seite nicht erreichbar ist."),
    ("Kleine Änderungen", "Ein Preis, ein Foto, ein Text. Der Umfang pro Monat wird im Vertrag festgelegt."),
    ("Quartalscheck", "Ladezeit, kaputte Links, veraltete Inhalte."),
]

ABLAUF = [
    ("Erstgespräch", "30 Minuten, kostenlos. Sie erzählen, was Ihr Betrieb macht und was die Seite leisten soll."),
    ("Konzept zur Freigabe", "Sie sehen Aufbau, Texte und Gestaltung, bevor ich baue. Ohne Ihr Okay geht es nicht weiter."),
    ("Umsetzung", "Ich baue, Sie sehen Zwischenstände. 2 bis 4 Korrekturrunden sind im Preis, je nach Paket."),
    ("Übergabe", "Die Seite geht online. Sie bekommen alle Zugänge und eine kurze Anleitung."),
]

ZAHLUNG_TEXT = ("Zahlung bei Onepager und Business-Website: 50 % bei Auftragserteilung, 50 % bei Fertigstellung. "
                "Bei Premium und Shop gestaffelt: 40 % bei Start, 30 % nach Konzept-Freigabe, 30 % bei Fertigstellung.")
PREIS_HINWEIS = ("Alle Preise sind Endpreise. Als Kleinunternehmer (§ 6 Abs. 1 Z 27 UStG) verrechne ich keine Umsatzsteuer.")

# Seiten, die in Navigation und Fuß vorkommen: (Pfad, Text)
NAV = [("/arbeiten/", "Arbeiten"), ("/leistungen/", "Leistungen & Preise"), ("/ueber-mich/", "Über mich"), ("/kontakt/", "Kontakt")]
FUSS_SEITEN = [("/arbeiten/", "Arbeiten"), ("/leistungen/", "Leistungen & Preise"), ("/handwerk/", "Für Handwerksbetriebe"),
               ("/ueber-mich/", "Über mich"), ("/kontakt/", "Kontakt")]

# --- Englische Fassung der Pakete und Texte (Preise, Umfang und Bedingungen wie oben) ------------
_EN = {
    "onepager": {
        "name": "One-pager", "fuer": "Personal brands, coaches, events, small local businesses",
        "seiten": "1 page with several sections", "dauer": "approx. 1–2 weeks",
        "nutzen": "A single page that says what you do, what it costs and how to reach you. Quick to build, quick to launch.",
        "umfang": ["1 page with several sections", "responsive design", "Basic SEO (title and meta description)", "2 rounds of revisions",
                   "Delivery in approx. 1–2 weeks"],
        "optional": "copywriting, second language, maintenance",
        "betreuung": "Optional add-on.",
        "zahlung": "50 % on order, 50 % on completion"},
    "business": {
        "name": "Business website", "fuer": "Freelancers and small businesses with several services",
        "seiten": "4–7 subpages", "dauer": "approx. 3–5 weeks",
        "nutzen": "A site with 4–7 subpages that presents your services one by one and is designed mobile-first. You see the concept before I build.",
        "umfang": ["4–7 subpages", "Concept for your approval before the build", "responsive design",
                   "Editing interface for recurring content (on request)", "Contact form", "3 rounds of revisions",
                   "Ongoing care from €60/month is included (hosting, small changes)", "Delivery in approx. 3–5 weeks"],
        "optional": "second language, copywriting",
        "betreuung": "Minimum term 3 months, then cancellable monthly.",
        "zahlung": "50 % on order, 50 % on completion"},
    "premium": {
        "name": "Premium",
        "fuer": "Brands with high standards for craft, motion and individuality. Like this site and nickmonu.com",
        "seiten": "as Business website, multilingual", "dauer": "approx. 5–8 weeks",
        "nutzen": "Everything in the Business website, plus motion and building blocks that exist only for your brand. Delivery time depends on the amount of animation.",
        "umfang": ["everything in the Business website", "custom animations (page transitions, cursor effects, loading moments)",
                   "tailor-made components instead of standard blocks", "multilingual as standard", "4 rounds of revisions",
                   "Ongoing care from €80/month is included", "Delivery in approx. 5–8 weeks, depending on the amount of animation"],
        "optional": "image production/photography, copywriting",
        "betreuung": "Minimum term 3 months, then cancellable monthly.",
        "zahlung": "40 % at start, 30 % after concept approval, 30 % on completion"},
    "shop": {
        "name": "Shop", "fuer": "Small product range, brand shop",
        "seiten": "Product catalogue of up to approx. 20 products",
        "nutzen": "A simple brand shop with a manageable number of products. If you have more products or variants, I will tell you beforehand which technical basis fits.",
        "umfang": ["Product catalogue of up to approx. 20 products", "Checkout", "one payment integration", "responsive design",
                   "3 rounds of revisions", "Ongoing care from €80/month is included"],
        "hinweis": "For higher complexity (many variants, international shipping, stock management) I will advise you candidly which technical basis really fits, if necessary with a custom quote outside the fixed package.",
        "betreuung": "Minimum term 3 months, then cancellable monthly.",
        "zahlung": "40 % at start, 30 % after concept approval, 30 % on completion"},
}
PAKETE_EN = [dict(p, **_EN[p["id"]]) for p in PAKETE]


def pakete():
    return PAKETE_EN if LANG == "en" else PAKETE


ZUSATZ_EN = [
    ("Basic SEO setup (meta tags, structure, sitemap, Google Business Profile)", "€250–400"),
    ("Copywriting per subpage", "€60–90 per page"),
    ("Additional language", "+15–20 % on the package price"),
    ("“Active” maintenance: more changes per month, prioritised handling (upgrade to the included care)", "€150/month"),
    ("Express surcharge (delivery time halved)", "+20–30 % on the package price"),
]

BETREUUNG_UMFANG_EN = [
    ("Hosting", "The site lives on my hosting. You don't have to deal with a server or renewals."),
    ("Updates and backups", "I keep everything up to date. There is always a copy."),
    ("Uptime monitoring", "An automatic check tells me if the site is not reachable."),
    ("Small changes", "A price, a photo, a text. The volume per month is set in the contract."),
    ("Quarterly check", "Load time, broken links, outdated content."),
]

ABLAUF_EN = [
    ("Intro call", "30 minutes, free. You tell me what your business does and what the site should achieve."),
    ("Concept for approval", "You see structure, copy and design before I build. Nothing moves on without your OK."),
    ("Build", "I build, you see work in progress. 2 to 4 rounds of revisions are included, depending on the package."),
    ("Handover", "The site goes live. You get all access details and a short guide."),
]

ZAHLUNG_TEXT_EN = ("Payment for One-pager and Business website: 50 % on order, 50 % on completion. "
                   "For Premium and Shop in instalments: 40 % at start, 30 % after concept approval, 30 % on completion.")
PREIS_HINWEIS_EN = ("All prices are final prices. As a small business under § 6 (1) no. 27 of the Austrian VAT Act (UStG) I do not charge VAT.")

NAV_EN = [("/arbeiten/", "Work"), ("/leistungen/", "Services & pricing"), ("/ueber-mich/", "About"), ("/kontakt/", "Contact")]
FUSS_SEITEN_EN = [("/arbeiten/", "Work"), ("/leistungen/", "Services & pricing"), ("/handwerk/", "For trades businesses"),
                  ("/ueber-mich/", "About"), ("/kontakt/", "Contact")]

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
        p = k["paket"]
        marke = tr("Echtes Projekt", "Real project") if k["echt"] else tr("Konzept-Demo", "Concept demo")
        beleg = f'<p class="werk-beleg">{k["beleg"]}</p>' if k.get("beleg") else ""
        teile += f'''<article class="werk werk-{i + 1}" aria-labelledby="werk-{k["id"]}">
    <a class="werk-bild" href="{P(k["href"])}" tabindex="-1" aria-hidden="true">{bild_werk("werk-" + k["id"], k["alt"], groessen[min(i, 2)])}</a>
    <div class="werk-info">
      <h3 class="werk-name" id="werk-{k["id"]}"><a href="{P(k["href"])}">{e(k["titel"])}</a></h3>
      <p class="werk-art">{e(k["art"])}</p>
      {beleg}
      <dl class="werk-daten"><div><dt>{tr("Art", "Type")}</dt><dd>{marke}</dd></div><div><dt>{tr("Paket", "Package")}</dt><dd><a href="{P("/leistungen/#" + p["id"])}">{e(p["name"])}, {ab}\u00a0{eur(p["ab"])}</a></dd></div></dl>
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


def preis_zeile(p):
    ab = tr("ab", "from")
    if EINFUEHRUNG and p.get("einf"):
        return (f'<span class="preis-alt">{ab} {eur(p["ab"])}</span> '
                f'<span class="preis-einf">{tr("Einführung ab", "Launch offer from")} {eur(p["einf"])}</span>')
    return f'{ab} {eur(p["ab"])}'


def paket_karte(p, detail=False):
    """Karte mit Ab-Preis. Mit detail=True klappt „Dafür bekommen Sie“ auf (details, geht ohne JavaScript)."""
    ab = tr("ab", "from")
    dauer = f'<li>{e(p["dauer"])}</li>' if p.get("dauer") else ""
    bet = (f'<li>{tr("Betreuung ab", "Care from")} {eur(p["betreuung_ab"])}{tr("/Monat", "/month")}</li>'
           if p.get("betreuung_ab") else "")
    einf = ""
    if EINFUEHRUNG and p.get("einf"):
        einf = f'<p class="karte-einf">{tr("Einführungsangebot:", "Launch offer:")} {tr("ab", "from")} {eur(p["einf"])}</p>'
    kopf = f'''<h3 class="karte-name">{e(p["name"])}</h3>
      <p class="karte-preis">{ab} {eur(p["ab"])}</p>{einf}
      <p class="karte-fuer">{e(p["fuer"])}</p>
      <ul class="karte-liste"><li>{e(p["seiten"])}</li>{dauer}{bet}</ul>'''
    if detail:
        umf = "".join(f"<li>{e(x)}</li>" for x in p["umfang"])
        opt = (f'<p class="klein">{tr("Optional dazu buchbar", "Optional extras")}: {e(p["optional"])}.</p>' if p.get("optional") else "")
        hin = f'<p class="klein">{e(p["hinweis"])}</p>' if p.get("hinweis") else ""
        return f'''<article class="karte" id="{p["id"]}">
      {kopf}
      <details class="karte-auf"><summary><span>{tr("Dafür bekommen Sie", "What you get")}</span></summary>
        <div class="karte-auf-inhalt">
          <p>{e(p["nutzen"])}</p>
          <h4>{tr("Enthalten", "Included")}</h4>
          <ul>{umf}</ul>{opt}{hin}
          <p class="klein">{e(p["betreuung"])} {tr("Zahlung", "Payment")}: {e(p["zahlung"])}.</p>
        </div>
      </details>
      {knopf(tr("Erstgespräch anfragen", "Book an intro call"), "/kontakt/?paket=" + p["id"], "knopf-2")}
    </article>'''
    return f'''<article class="karte" id="{p["id"]}">
      {kopf}
    </article>'''


def datenblatt(pk):
    """Pakete als Datenblatt: eine Zeile je Paket, Spalten zum Vergleichen. Am Handy wird jede Zeile ein Block mit Beschriftungen."""
    de = LANG != "en"
    L = {"p": "Paket" if de else "Package", "u": "Umfang" if de else "Scope", "d": "Dauer" if de else "Duration",
         "b": "Betreuung" if de else "Care", "pr": "Preis" if de else "Price"}
    zeilen = ""
    for p in pk:
        if p.get("betreuung_ab"):
            bet = f'{tr("ab", "from")}\u00a0{eur(p["betreuung_ab"])}{tr("/Monat", "/month")}'
        else:
            bet = tr("optional", "optional")
        dauer = p.get("dauer") or tr("nach Absprache", "by arrangement")
        einf = ""
        if EINFUEHRUNG and p.get("einf"):
            einf = f'<span class="db-einf">{tr("Befristet:", "Limited offer:")} {tr("ab", "from")}\u00a0{eur(p["einf"])}</span>'
        zeilen += (f'<tr id="{p["id"]}-zeile"><th scope="row"><a class="db-name" href="{P("/leistungen/#" + p["id"])}">{e(p["name"])}</a>'
                   f'<span class="db-fuer">{e(p["fuer"])}</span></th>'
                   f'<td data-l="{L["u"]}">{e(p["seiten"])}</td><td data-l="{L["d"]}">{e(dauer)}</td><td data-l="{L["b"]}">{bet}</td>'
                   f'<td class="db-preis" data-l="{L["pr"]}"><span>{tr("ab", "from")}\u00a0{eur(p["ab"])}</span>{einf}</td></tr>')
    cap = tr("Die vier Pakete im Vergleich", "The four packages compared")
    return (f'<div class="tab-wrap"><table class="datenblatt"><caption class="nur-leser">{cap}</caption><thead><tr>'
            f'<th scope="col">{L["p"]}</th><th scope="col">{L["u"]}</th><th scope="col">{L["d"]}</th><th scope="col">{L["b"]}</th>'
            f'<th scope="col">{L["pr"]}</th></tr></thead><tbody>{zeilen}</tbody></table></div>')


def ablauf_schiene():
    """Waagrechte Schiene mit vier Schritten (am Handy senkrecht)."""
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
            f'<span class="reiter-name">{e(x["name"])}</span><span class="reiter-paket">{e(x["paket"])}, {ab} {x["paket_ab"]}</span>'
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
    opts = [("", tr("noch offen", "not decided yet")), ("onepager", tr("Onepager", "One-pager")),
            ("business", tr("Business-Website", "Business website")), ("premium", "Premium"), ("shop", "Shop")]
    o = "".join(f'<option value="{v}"{" selected" if v == paket else ""}>{t}</option>' for v, t in opts)
    if FORMSPREE:
        aktion = f'action="{e(FORMSPREE)}" method="post"'
        dat = f' data-endpoint="{e(FORMSPREE)}"'
    else:
        aktion = f'action="mailto:{MAIL}" method="post" enctype="text/plain"'
        dat = ""
    n_name, n_mail, n_firma, n_paket, n_text = (tr("Name", "Name"), tr("E-Mail", "Email"), tr("Betrieb oder Projekt", "Business or project"),
                                               tr("Paket", "Package"), tr("Nachricht", "Message"))
    hinweis = (tr("Ihre Angaben gehen über den Formulardienst Formspree an mich. Mehr dazu im ",
                  "Your details reach me through the form service Formspree. More in the ") if FORMSPREE else
               tr("Das Formular öffnet Ihr E-Mail-Programm. Mehr dazu im ", "The form opens your email program. More in the "))
    return f'''<form class="formular" {aktion}{dat} data-formular novalidate>
      <div class="feld"><label for="f-name">{n_name}</label><input id="f-name" name="{n_name}" type="text" autocomplete="name" required></div>
      <div class="feld"><label for="f-mail">{n_mail}</label><input id="f-mail" name="{n_mail}" type="email" autocomplete="email" required></div>
      <div class="feld"><label for="f-firma">{n_firma}</label><input id="f-firma" name="{n_firma}" type="text" autocomplete="organization"></div>
      <div class="feld"><label for="f-paket">{n_paket}</label><select id="f-paket" name="{n_paket}">{o}</select></div>
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
  <a class="kopf-name" href="{P("/")}" aria-label="{tr("Simon Monu, zur Startseite", "Simon Monu, home")}">Simon Monu</a>
  <nav class="kopf-nav" aria-label="{tr("Hauptmenü", "Main menu")}">{links}</nav>
  {sprache}<a class="knopf knopf-klein kopf-cta" href="{P("/kontakt/")}">{tr("Erstgespräch", "Intro call")}</a>
  <details class="menue" data-menue>
    <summary><span>{tr("Menü", "Menu")}</span><i aria-hidden="true"></i></summary>
    <div class="menue-blatt">
      <nav aria-label="{tr("Hauptmenü, mobil", "Main menu, mobile")}">{links}<a href="{P("/handwerk/")}"{cur(P("/handwerk/"))}>{tr("Für Handwerksbetriebe", "For trades businesses")}</a>{sprache_menue}</nav>
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
      <p class="fuss-name">Simon Monu</p>
      <p>{tr("Websites für Betriebe, Selbstständige und Marken in Wien und Salzburg. Entworfen und gebaut von einer Person.",
             "Websites for businesses, freelancers and brands in Vienna and Salzburg. Designed and built by one person.")}</p>
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


def seite(pfad, titel, beschreibung, inhalt, start=False, og="start", robots="index, follow", jsonld=None, klasse="", fruehe_bilder=(), fonts=()):
    """Vollständige HTML-Seite. Platzhalter @@N@@ und @@KB@@ füllt bau.py."""
    url = DOMAIN + (pfad if pfad.endswith("/") or pfad.endswith(".html") else pfad + "/")
    if pfad == "/":
        url = DOMAIN + "/"
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
<meta name="robots" content="{robots}">
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
