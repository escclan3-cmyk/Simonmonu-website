# -*- coding: utf-8 -*-
"""Explosionszeichnung einer Website: sechs Schichten, isometrisch, nur Linien.
Reines Inline-SVG, keine Bilder. Die Zahlen an den Hilfslinien kommen aus dem Bau (gemessene Dateigrößen);
nur die Summe unten ist live (data-live-kb) und deshalb magenta.

zeichnung(lang, z, etiketten) -> SVG-String
  lang: "de" | "en"
  z: dict mit den Zahlen {"html","css","fonts","js"} in KB (Strings)
  etiketten: False = schmale Fassung fürs Handy (ohne Beschriftung an den Hilfslinien)
"""
import math

C = math.cos(math.radians(30))
S = 0.5
W, D = 150, 110          # Plattengröße in Plattenkoordinaten
ABSTAND = 104            # senkrechter Abstand der Schichten (auseinandergezogen)
OX = 150                 # x der oberen Ecke der Platten im Bild


def proj(x, y):
    """Plattenkoordinate -> Bildkoordinate relativ zur oberen Ecke."""
    return ((x - y) * C, (x + y) * S)


def p(x, y, dx=0, dy=0):
    a, b = proj(x, y)
    return f"{a + dx:.1f} {b + dy:.1f}"


def platte_rahmen():
    o, r, u, l = proj(0, 0), proj(W, 0), proj(W, D), proj(0, D)
    dick = 5
    flaeche = f"M{o[0]:.1f} {o[1]:.1f}L{r[0]:.1f} {r[1]:.1f}L{u[0]:.1f} {u[1]:.1f}L{l[0]:.1f} {l[1]:.1f}Z"
    kante = (f"M{l[0]:.1f} {l[1]:.1f}v{dick}L{u[0]:.1f} {u[1] + dick:.1f}L{r[0]:.1f} {r[1] + dick:.1f}v-{dick}"
             f"M{u[0]:.1f} {u[1]:.1f}v{dick}")
    return flaeche, kante, r


# Inhalt jeder Schicht, gezeichnet in Plattenkoordinaten (flach), die Gruppe wird isometrisch gekippt
def inhalt_text():
    z = '<path d="M14 16h64" class="d"/>'
    for i, b in enumerate((112, 96, 118, 84, 104)):
        z += f'<path d="M14 {32 + i * 11}h{b}"/>'
    return z


def inhalt_layout():
    z = ""
    for i in range(4):
        z += f'<rect x="{12 + i * 34}" y="12" width="26" height="86" class="g"/>'
    z += '<rect x="12" y="12" width="60" height="30"/><rect x="80" y="12" width="58" height="12"/><rect x="80" y="56" width="58" height="42"/>'
    return z


def inhalt_schrift():
    return ('<text x="14" y="72" class="aa">Aa</text>'
            '<path d="M14 84h122M14 28h122" class="g"/><path d="M104 28v56M104 28h-4M104 84h-4"/>')


def inhalt_bilder():
    return ('<rect x="14" y="14" width="122" height="82"/><path d="M14 96L136 14M14 14L136 96" class="g"/>'
            '<circle cx="46" cy="38" r="8"/><path d="M30 84l30-28 20 18 14-12 28 22"/>')


def inhalt_bewegung():
    return ('<path d="M20 14v82h112" class="g"/><path d="M20 96C48 96 58 20 132 18"/>'
            '<circle cx="132" cy="18" r="3.5" class="f"/><path d="M20 96L132 18" class="g"/>')


def inhalt_formular():
    return ('<rect x="14" y="16" width="122" height="18"/><rect x="14" y="42" width="122" height="18"/>'
            '<rect x="14" y="70" width="52" height="22" class="f"/>')


SCHICHTEN = [  # von unten nach oben
    ("inhalt", inhalt_text),
    ("layout", inhalt_layout),
    ("schrift", inhalt_schrift),
    ("bilder", inhalt_bilder),
    ("bewegung", inhalt_bewegung),
    ("formular", inhalt_formular),
]

NAMEN = {
    "de": {"inhalt": "Inhalt", "layout": "Raster", "schrift": "Schrift", "bilder": "Bilder", "bewegung": "Bewegung", "formular": "Formular"},
    "en": {"inhalt": "Content", "layout": "Grid", "schrift": "Type", "bilder": "Images", "bewegung": "Motion", "formular": "Form"},
}


def zahlen_zeile(lang, k, z):
    de = lang == "de"
    return {
        "inhalt": f"index.html {z['html']} KB",
        "layout": f"stil.css {z['css']} KB",
        "schrift": ("2 Schriften " if de else "2 typefaces ") + f"{z['fonts']} KB",
        "bilder": "AVIF, WebP" if de else "AVIF, WebP",
        "bewegung": f"seite.js {z['js']} KB",
        "formular": "0 Cookies" if de else "0 cookies",
    }[k]


def zeichnung(lang="de", z=None, etiketten=True, abstand=None):
    z = z or {"html": "9", "css": "9", "fonts": "72", "js": "7"}
    flaeche, kante, r = platte_rahmen()
    n = len(SCHICHTEN)
    ABSTAND = abstand or (104 if etiketten else 80)
    hoehe = (D + W) * S + 5 + (n - 1) * ABSTAND + 40
    breite = 590 if etiketten else 330
    ox = OX + D * C - 0 if etiketten else 20 + D * C   # obere Ecke so setzen, dass die linke Ecke bei x=ox-D*C liegt
    teile = []
    for i, (k, f) in enumerate(SCHICHTEN):
        # i = 0 ist unten; y der oberen Ecke
        y0 = 8 + (n - 1 - i) * ABSTAND
        kipp = f"matrix({C:.4f} {S} {-C:.4f} {S} 0 0)"
        etikett = ""
        if etiketten:
            ex = ox + r[0] + 26
            ey = y0 + r[1]
            etikett = (f'<path d="M{ox + r[0] + 6:.1f} {ey:.1f}H{ex - 4:.1f}" class="h"/><circle cx="{ox + r[0] + 4:.1f}" cy="{ey:.1f}" r="2" class="pt"/>'
                       f'<text x="{ex:.1f}" y="{ey - 5:.1f}" class="nm">{i + 1:02d} {NAMEN[lang][k]}</text>'
                       f'<text x="{ex:.1f}" y="{ey + 13:.1f}" class="zl">{zahlen_zeile(lang, k, z)}</text>')
        teile.append(
            f'<g class="s s{i}"><g transform="translate({ox:.1f} {y0:.1f})">'
            f'<path d="{flaeche}" class="pl"/><path d="{kante}" class="kt"/>'
            f'<g transform="{kipp}" class="in">{f()}</g></g>{etikett}</g>')
    # Maßlinie links über alle Schichten, Summe live (magenta)
    mx = ox - D * C - 22 if etiketten else 8
    yo, yu = 8 + proj(0, 0)[1], 8 + (n - 1) * ABSTAND + (D + W) * S + 5
    sum_txt = "Σ" if True else ""
    mass = (f'<g class="mass"><path d="M{mx:.1f} {yo:.1f}V{yu:.1f}M{mx - 5:.1f} {yo:.1f}h10M{mx - 5:.1f} {yu:.1f}h10" class="ml"/>'
            f'<g class="mtg"><text x="{mx - 8:.1f}" y="{(yo + yu) / 2:.1f}" class="live" transform="rotate(-90 {mx - 8:.1f} {(yo + yu) / 2:.1f})" text-anchor="middle">'
            f'Σ <tspan data-live-kb>@@KB@@</tspan> KB</text></g></g>')
    titel = ("Explosionszeichnung dieser Website in sechs Schichten: Inhalt, Raster, Schrift, Bilder, Bewegung, Formular"
             if lang == "de" else
             "Exploded view of this website in six layers: content, grid, type, images, motion, form")
    return (f'<svg class="zeichnung {"z-voll" if etiketten else "z-schmal"}" viewBox="0 0 {breite} {hoehe:.0f}" role="img" aria-label="{titel}" '
            f'focusable="false" preserveAspectRatio="xMidYMid meet">{mass}{"".join(teile)}</svg>')


def handy(lang="de"):
    """Linienzeichnung: Betriebs-Website am Handy, Nummer oben, Richtpreise. Gleiche Zeichensprache wie die Explosionszeichnung."""
    de = lang == "de"
    t = {
        "titel": "Zeichnung einer Handwerker-Website am Handy mit Telefonnummer oben und Richtpreisen" if de else
                 "Drawing of a trades website on a phone with the phone number at the top and guide prices",
        "a": "Nummer oben, ein Tipp" if de else "Number on top, one tap",
        "b": "Foto echter Arbeit" if de else "Photo of real work",
        "c": "Richtpreis je Leistung" if de else "Guide price per service",
        "btn": "Anrufen" if de else "Call",
    }
    zeilen = "".join(f'<path d="M36 {214 + i * 38}h74M150 {214 + i * 38}h24"/><path d="M36 {228 + i * 38}h138" class="g"/>' for i in range(3))
    return (f'<svg class="zeichnung z-handy" viewBox="0 0 400 372" role="img" aria-label="{t["titel"]}" focusable="false">'
            '<rect x="20" y="8" width="170" height="356" rx="24" class="pl"/><path d="M80 20h50" />'
            '<path d="M36 44h70"  class="d"/><path d="M148 44h26M148 52h26"/>'
            f'<rect x="36" y="68" width="138" height="38" rx="6" class="f"/><text x="105" y="92" text-anchor="middle" class="inv">{t["btn"]}</text>'
            '<rect x="36" y="122" width="138" height="72"/><path d="M36 194L174 122M36 122L174 194" class="g"/>'
            f'{zeilen}'
            '<path d="M190 87h40M190 158h40M190 233h40" class="h"/><circle cx="190" cy="87" r="2" class="pt"/><circle cx="190" cy="158" r="2" class="pt"/><circle cx="190" cy="233" r="2" class="pt"/>'
            f'<text x="238" y="91" class="zl">{t["a"]}</text><text x="238" y="162" class="zl">{t["b"]}</text><text x="238" y="237" class="zl">{t["c"]}</text>'
            '</svg>')


# --- Schichten: dieselbe Seite in vier Ausbaustufen -----------------------------------------------------------------
# Vier Platten aus echtem HTML, gestaltet durch jeweils mehr CSS (stil.css, Block 'Platten'). Keine Bilder, nichts
# muss neu aufgenommen werden, wenn sich Text oder Farbe ändern.
SCHICHT_BILDER = ["inhalt", "raster", "schrift", "fertig"]
SCHICHT_NAMEN = {
    "de": {"inhalt": "Inhalt", "raster": "Raster", "schrift": "Schrift", "fertig": "Farbe und Bewegung"},
    "en": {"inhalt": "Content", "raster": "Grid", "schrift": "Type", "fertig": "Colour and motion"},
}


def schichten(lang="de", z=None):
    z = z or {"html": "9", "css": "9", "fonts": "72", "js": "7"}
    de = lang == "de"
    zeile = {
        "inhalt": f"index.html {z['html']} KB",
        "raster": f"stil.css {z['css']} KB",
        "schrift": ("2 Schriften " if de else "2 typefaces ") + f"{z['fonts']} KB",
        "fertig": f"seite.js {z['js']} KB",
    }
    titel = ("Diese Startseite in vier Schichten: nur Inhalt, dazu das Raster, dazu die Schrift, am Ende fertig mit Farbe und Bewegung"
             if de else "This home page in four layers: content only, plus grid, plus type, finally finished with colour and motion")
    T = {
        "de": {"marke": "Simon Monu", "nav": ["Arbeiten", "Leistungen", "Kontakt"], "h": ["Ich baue", "Ihre Website.", "Und messe nach."],
               "lead": "Ich entwerfe und verantworte jede Zeile, ohne Baukasten und ohne Vorlage. Für Betriebe, Selbstständige und Marken in Wien und Salzburg.",
               "k1": "Arbeiten ansehen", "k2": "Preise ansehen"},
        "en": {"marke": "Simon Monu", "nav": ["Work", "Services", "Contact"], "h": ["I build", "your website.", "And measure it."],
               "lead": "I design it and take responsibility for every line, with no site builder and no template. For businesses, freelancers and brands in Vienna and Salzburg.",
               "k1": "See my work", "k2": "See prices"},
    }[lang]
    tafel = [("index.html", f"{z['html']} KB"), ("stil.css", f"{z['css']} KB"),
             (("2 Schriften" if de else "2 typefaces"), f"{z['fonts']} KB"), ("seite.js", f"{z['js']} KB")]
    zeilen = "".join(f'<span class="pl-z"><span>{a}</span><span>{b}</span></span>' for a, b in tafel)
    nav = "".join(f"<span>{n}</span>" for n in T["nav"])
    h = "<br>".join(T["h"])
    # Dieselbe Seite, viermal mit weniger Stylesheet: echtes HTML und CSS, also auf jedem Bildschirm scharf.
    platten = "".join(
        f'<div class="platte p{i} pk-{k}"><div class="pl">'
        f'<div class="pl-nav"><b>{T["marke"]}</b>{nav}</div>'
        f'<div class="pl-haupt"><div class="pl-h">{h}</div><div class="pl-lead">{T["lead"]}</div>'
        f'<div class="pl-knoepfe"><span class="pl-k1">{T["k1"]}</span><span class="pl-k2">{T["k2"]}</span></div></div>'
        f'<div class="pl-tafel">{zeilen}</div></div></div>'
        for i, k in enumerate(SCHICHT_BILDER))
    liste = "".join(
        f'<li><span class="sl-name">{SCHICHT_NAMEN[lang][k]}</span><span class="sl-wert">{zeile[k]}</span></li>'
        for i, k in reversed(list(enumerate(SCHICHT_BILDER))))
    spur = ('<p class="spur mono" data-spur>Diese Seite: @@N@@ Dateien, @@KB@@ KB</p>' if de else
            '<p class="spur mono" data-spur>This page: @@N@@ files, @@KB@@ KB</p>')
    return (f'<figure class="schichten" data-schichten role="group" aria-label="{titel}">'
            f'<div class="stapel" aria-hidden="true">{platten}</div>'
            f'<ol class="schicht-liste">{liste}</ol>{spur}</figure>')


# --- Wie eine Seite entsteht: dieselbe Startseite in vier Stufen ------------------------------------------------
# Vier Platten aus echtem HTML, gestaltet durch jeweils mehr CSS (stil.css, Block „Folge“). Sie liegen im selben Rahmen
# übereinander; beim Scrollen durch die vier Schritte schiebt sich die jeweils nächste Stufe über die vorige.
FOLGE_TEXT = {
    "de": {"nav": ["Arbeiten", "Leistungen", "Kontakt"], "h": ["Jede Website", "ein Einzelstück."],
           "lead": "Ich entwerfe und programmiere Websites für Betriebe, Selbstständige und Marken in Wien und Salzburg.",
           "k1": "Arbeiten ansehen", "k2": "Preise ab 950 €",
           "werke": ["nickmonu.com", "Tischlerei Hallwirth", "Vera Lindtner Coaching"],
           "titel": "Diese Startseite in vier Stufen: nur Inhalt, dazu das Raster, dazu die Schrift, am Ende mit Farbe"},
    "en": {"nav": ["Work", "Services", "Contact"], "h": ["Every website", "a one-off."],
           "lead": "I design and code websites for businesses, freelancers and brands in Vienna and Salzburg.",
           "k1": "See my work", "k2": "Prices from €950",
           "werke": ["nickmonu.com", "Tischlerei Hallwirth", "Vera Lindtner Coaching"],
           "titel": "This home page in four stages: content only, plus grid, plus type, finally with colour"},
}


def folge(lang="de"):
    T = FOLGE_TEXT[lang]
    nav = "".join(f"<span>{n}</span>" for n in T["nav"])
    werke = "".join(f'<span class="pl-w pl-w{i + 1}">{w}</span>' for i, w in enumerate(T["werke"]))
    platten = "".join(
        f'<div class="platte p{i} pk-{k}"><div class="pl">'
        f'<div class="pl-nav"><b>Simon Monu</b>{nav}</div>'
        f'<div class="pl-h">{"<br> ".join(T["h"])}</div>'
        f'<div class="pl-lead">{T["lead"]}</div>'
        f'<div class="pl-knoepfe"><span class="pl-k1">{T["k1"]}</span><span class="pl-k2">{T["k2"]}</span></div>'
        f'<div class="pl-werke">{werke}</div>'
        f'</div></div>'
        for i, k in enumerate(SCHICHT_BILDER))
    return (f'<figure class="folge" data-folge role="img" aria-label="{T["titel"]}">'
            f'<div class="folge-rahmen" aria-hidden="true">{platten}</div></figure>')
