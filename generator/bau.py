# -*- coding: utf-8 -*-
"""Baut simonmonu.at nach website/ (oder $SM_AUS). Aufruf: python3 generator/bau.py

1. Bilder aus _quelle/bilder/ nach AVIF/WebP/JPEG, schreibt generator/_bilder.json
2. Seiten erzeugen (zweimal: erst ohne, dann mit Dateizahl und Gewicht der Spur-Zeile)
3. sitemap, robots, _headers, .htaccess, Manifest, Icons
4. Demos kopieren (Pfade, CSP-Hashes)
5. Meldung, was vor dem Livegang noch fehlt
"""
import os, sys, json, re, shutil, hashlib, base64, gzip, glob
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # Windows-Konsole: Umlaute und § sauber ausgeben

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemeinsam as G
from gemeinsam import anschrift_fehlt
import seiten_de, seiten_arbeiten, seiten_en

AUS = G.AUS
QUELLE = os.path.join(G.WURZEL, "_quelle")
BILDER_Q = os.path.join(QUELLE, "bilder")
CACHE = os.path.join(QUELLE, "bild-cache")   # fertig umgerechnete Bilder, damit nicht jeder Bau alles neu rechnet

# Bildname -> (Quelldatei, Beschnitt (l,o,r,u) oder None, Ausgabebreiten, JPEG-Breite)
BILDER = {
    # Die drei Arbeiten als Aufnahmen des ersten Bildschirms: Desktop 1440 x 900 in doppelter Auflösung, Handy 390 x 844 doppelt,
    # für die Startseite auf 4:5 beschnitten. Neu aufnehmen mit tools/aufnahmen.py, wenn sich eine Arbeit sichtbar ändert.
    "werk-nickmonu-d": ("werk-nickmonu-d.png", None, [720, 1080, 1440, 2160, 2880], 1440),
    "werk-hallwirth-d": ("werk-hallwirth-d.png", None, [720, 1080, 1440, 2160, 2880], 1440),
    "werk-lindtner-d": ("werk-lindtner-d.png", None, [720, 1080, 1440, 2160, 2880], 1440),
    "werk-nickmonu-m": ("werk-nickmonu-m.png", (0, 0, 780, 975), [390, 780], 780),
    "werk-hallwirth-m": ("werk-hallwirth-m.png", (0, 0, 780, 975), [390, 780], 780),
    "werk-lindtner-m": ("werk-lindtner-m.png", (0, 0, 780, 975), [390, 780], 780),
    # Startseite, Schieber: die Tischlerei-Demo ohne CSS und Bilder (roh) und fertig, gleiche Fenstergröße.
    "vn-roh-d": ("vn-roh-d.png", None, [720, 1080, 1440, 2160, 2880], 1440),
    "vn-fertig-d": ("vn-fertig-d.png", None, [720, 1080, 1440, 2160, 2880], 1440),
    "vn-roh-m": ("vn-roh-m.png", (0, 0, 780, 975), [390, 780], 780),
    "vn-fertig-m": ("vn-fertig-m.png", (0, 0, 780, 975), [390, 780], 780),
    # Vorher/Nachher im Case nickmonu.com
    "nickmonu-25-m": ("nickmonu25-m-oben.png", None, [390, 780], 390),
    "nickmonu-26-m": ("nickmonu-index-m-oben.png", None, [390, 780], 390),
}


def quelle(name):
    for d in (BILDER_Q,):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def bilder():
    """Bilder aus _quelle/bilder in drei Formaten. Schon gerechnete Dateien (bild-cache) werden wiederverwendet,
    solange die Quelle nicht neuer ist. Fehlt AVIF in Pillow, genügt der Cache; sonst gibt es eine klare Meldung."""
    from PIL import features
    avif = features.check("avif")
    zielp = os.path.join(AUS, "assets", "img")
    os.makedirs(zielp, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    man = {}
    for name, (q, crop, breiten, jpgb) in BILDER.items():
        pfad = quelle(q)
        if not pfad:
            print(f"WARNUNG: Bildquelle fehlt: {q}")
            continue
        im = Image.open(pfad).convert("RGB")
        if crop:
            im = im.crop(crop)
        w0, h0 = im.size
        ok = []
        for b in breiten:
            if b > w0:
                continue
            h = round(h0 * b / w0)
            r = None
            for ext, opt in (("jpg", dict(quality=82, optimize=True, progressive=True)), ("webp", dict(quality=80, method=6)),
                             ("avif", dict(quality=55, speed=6))):
                c = os.path.join(CACHE, f"{name}-{b}.{ext}")
                if not (os.path.exists(c) and os.path.getmtime(c) >= os.path.getmtime(pfad)):
                    if ext == "avif" and not avif:
                        sys.exit(f"FEHLER: {c} fehlt und Pillow kann kein AVIF. Abhilfe: pip install -U pillow")
                    r = r or im.resize((b, h), Image.LANCZOS)
                    r.save(c, **opt)
                shutil.copy2(c, os.path.join(zielp, os.path.basename(c)))
            ok.append(b)
        man[name] = {"breiten": ok, "jpg": min(jpgb, ok[-1]) if jpgb in ok else ok[0], "w": w0, "h": h0}
    json.dump(man, open(os.path.join(G.BASIS, "_bilder.json"), "w", encoding="utf-8"), indent=1)
    G._MANIFEST = man
    return man


def schreibe(rel, text, binaer=False):
    p = os.path.join(AUS, rel.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb" if binaer else "w", **({} if binaer else {"encoding": "utf-8"})).write(text)


def groesse(rel, gz=False):
    p = os.path.join(AUS, rel.lstrip("/"))
    if not os.path.exists(p):
        return 0
    d = open(p, "rb").read()
    return len(gzip.compress(d, 6)) if gz else len(d)


ZEICHEN = re.compile("[\u00d7\u2190-\u2199\u2248\u2264\u2265]")


def zeichen_bedarf(html):
    """Braucht die Seite die Zusatzdateien mit Pfeilen und Zeichen (siehe unicode-range in stil.css)?
    Getrennt nach Grotesk und Mono; Mono gilt für Text in Elementen mit der Klasse „mono“."""
    from html.parser import HTMLParser
    leer = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "circle"}

    class P(HTMLParser):
        def __init__(s):
            super().__init__(); s.st = []; s.sans = s.mono = False; s.skip = 0
        def handle_starttag(s, tag, a):
            if tag in leer: return
            k = (dict(a).get("class") or "").split()
            s.st.append((tag, "mono" in k))
        def handle_endtag(s, tag):
            if tag in leer: return
            while s.st and s.st[-1][0] != tag: s.st.pop()
            if s.st: s.st.pop()
        def handle_data(s, d):
            if not ZEICHEN.search(d) or any(x[0] in ("script", "style", "title") for x in s.st): return
            if any(x[1] for x in s.st): s.mono = True
            else: s.sans = True
    p = P(); p.feed(html[html.find("<body"):])
    return p.sans, p.mono


def dateien_der_seite(html, pfad):
    """Was ein Erstbesuch lädt: HTML, CSS, zwei Skripte, vorgeladene Schriften, Bilder ohne lazy (kleinste Quelle)."""
    n, b = 1, len(gzip.compress(html.encode("utf-8"), 6))
    for u in re.findall(r'(?:href|src)="(/(?:css|js)/[^"?]+)', html):
        n += 1
        b += groesse(u, gz=True)
    for u in re.findall(r'<link rel="preload" href="(/assets/fonts/[^"]+)"', html):
        n += 1
        b += groesse(u)
    sans, mono = zeichen_bedarf(html)
    for f, noetig in (("schibsted-grotesk-zeichen.woff2", sans), ("fragment-mono-zeichen.woff2", mono)):
        if noetig and groesse("/assets/fonts/" + f):
            n += 1
            b += groesse("/assets/fonts/" + f)
    for m in re.finditer(r'<picture[^>]*>(.*?)</picture>', html, re.S):
        if 'loading="lazy"' in m.group(1):
            continue
        av = re.search(r'type="image/avif" srcset="([^"]+)"', m.group(1))
        if av:
            erst = av.group(1).split(",")[-1].strip().split(" ")[0]
            n += 1
            b += groesse(erst)
    return n, b


EINHEIT = re.compile(r"(\d|§) (€|%|KB|MB|s|ms|px|Minuten|Wochen|Werktagen|Werktage|Monate|Monat|Seiten|Unterseiten|Dateien|"
                     r"Korrekturrunden|Produkte|Stunden|Jahre|Sprachen|Freigaben|\d|days|weeks|months|month|pages|subpages|files|minutes|hours|years|languages|rounds|products|approvals)")


def satz(html):
    """Geschützte Leerzeichen zwischen Zahl und Einheit (und nach §), nur im sichtbaren Text, nicht in <pre>."""
    kopf, _, rumpf = html.partition("<body")
    teile = re.split(r"(<pre\b.*?</pre>|<script\b.*?</script>)", rumpf, flags=re.S)
    for i in range(0, len(teile), 2):
        teile[i] = re.sub(r">([^<]+)<", lambda m: ">" + EINHEIT.sub(lambda n: n.group(1) + "\u00a0" + n.group(2), m.group(1)) + "<", teile[i])
    return kopf + "<body" + "".join(teile)


def relativ(html, pfad):
    """Pfade ab der Domain-Wurzel (/css/..., /arbeiten/) in relative Pfade umrechnen. Damit läuft dieselbe Datei
    auf dem Server und per Doppelklick im Ordner. Ausnahme 404.html: Die liefert der Server unter jeder Adresse aus,
    dort müssen die Pfade absolut bleiben."""
    if pfad.endswith(".html"):
        return html
    tiefe = len([s for s in pfad.strip("/").split("/") if s])
    vor = "../" * tiefe
    def ziel(p):
        return (vor + p) if (vor + p) else "./"
    html = re.sub(r'(\s(?:href|src|action))="/(?!/)([^"]*)"', lambda m: f'{m.group(1)}="{ziel(m.group(2))}"', html)
    html = re.sub(r'(\ssrcset)="([^"]*)"', lambda m: m.group(1) + '="' + re.sub(r'(^|,\s*)/(?!/)', lambda n: n.group(1) + vor, m.group(2)) + '"', html)
    return html


def seiten():
    fonts = [f for f in ("schibsted-grotesk.woff2",) if os.path.exists(os.path.join(AUS, "assets", "fonts", f))]
    G.LANG = "de"
    alle = seiten_de.alle() + seiten_arbeiten.alle()
    G.LANG = "en"
    alle_en = seiten_en.alle()
    G.LANG = "de"
    fertig = {}
    for pfad, titel, beschr, inhalt, opt in alle + alle_en:
        k = dict(opt)
        G.LANG = "en" if pfad.startswith("/en/") else "de"
        h = satz(G.seite(pfad, titel, beschr, inhalt, fonts=fonts, **k))
        fertig[pfad] = (h, k)
    G.LANG = "de"
    # zweiter Durchgang: Zahlen einsetzen
    for pfad, (h, k) in fertig.items():
        n, b = dateien_der_seite(h, pfad)
        kb = f"{b / 1000:.0f}".replace(".", ",")
        h = h.replace("@@N@@", str(n)).replace("@@KB@@", kb)
        h = (h.replace("@@ZH@@", f"{len(gzip.compress(h.encode('utf-8'), 6)) / 1000:.0f}")
              .replace("@@ZC@@", f"{groesse('/css/stil.css', gz=True) / 1000:.0f}")
              .replace("@@ZF@@", f"{(groesse('/assets/fonts/schibsted-grotesk.woff2') + groesse('/assets/fonts/fragment-mono.woff2')) / 1000:.0f}")
              .replace("@@ZJ@@", f"{(groesse('/js/seite.js', gz=True) + groesse('/js/frueh.js', gz=True)) / 1000:.0f}"))
        rel = "404.html" if pfad.endswith(".html") else pfad.strip("/") + "/index.html" if pfad != "/" else "index.html"
        schreibe(rel, relativ(h, pfad))
        fertig[pfad] = (h, k)
    return fertig


def sitemap(fertig):
    z = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pfad, (h, k) in sorted(fertig.items()):
        if "noindex" in k.get("robots", "") or pfad.endswith(".html"):
            continue
        z.append(f"  <url><loc>{G.DOMAIN}{pfad}</loc></url>")
    z.append("</urlset>")
    schreibe("sitemap.xml", "\n".join(z) + "\n")
    # /demos/ bewusst NICHT per Disallow sperren: Sonst sieht Google das noindex der Demos nie und kann die Adressen trotzdem listen.
    schreibe("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {G.DOMAIN}/sitemap.xml\n")
    schreibe(".well-known/security.txt", f"Contact: mailto:{G.MAIL}\nExpires: 2027-09-30T00:00:00.000Z\nPreferred-Languages: de, en\n"
             f"Canonical: {G.DOMAIN}/.well-known/security.txt\n")


def csp_haupt():
    return G.csp()


def demo_csp(verz):
    """CSP je Demo: eigene Skripte per Hash, Stile wie die Demo sie braucht."""
    hs = []
    for f in glob.glob(os.path.join(verz, "**", "*.html"), recursive=True):
        t = open(f, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", t, re.S):
            if m.group(1).strip() and "ld+json" not in m.group(0)[:80]:
                hs.append("'sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode("utf-8")).digest()).decode() + "'")
    sk = " ".join(sorted(set(hs)))
    return ("default-src 'none'; script-src 'self' " + sk + "; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; "
            "connect-src 'self'; media-src 'self'; form-action 'none'; base-uri 'self'; frame-ancestors 'self'; object-src 'none'; upgrade-insecure-requests").replace("  ", " ")


# nickmonu.com läuft als Kopie unter /demos/nickmonu/. Das Formular darin ist echt (Formspree, landet bei Nick).
# In der Kopie sendet es nicht, sondern sagt, wo das Original ist: Wer die Demos ausprobiert, schickt Nick keine Testanfragen.
NICKMONU_FORM = """      // simonmonu.at: In der Kopie wird nichts gesendet.
      var hin = sprache === "en"
        ? ["Just a copy.", "This page is a copy of nickmonu.com on simonmonu.at, so your enquiry was not sent. To reach Nick, please use the original site: "]
        : ["Nur eine Kopie.", "Diese Seite ist eine Kopie von nickmonu.com auf simonmonu.at, Ihre Anfrage wurde nicht gesendet. Nick erreichen Sie \\u00fcber die Originalseite: "];
      var kopie = el("div", { class: "danke", role: "status", "aria-live": "polite" }, [
        el("p", { text: hin[0] }),
        el("p", null, [document.createTextNode(hin[1]), el("a", { href: "https://nickmonu.com/", target: "_blank", rel: "noopener", text: "nickmonu.com" })])
      ]);
      form.parentNode.replaceChild(kopie, form);
      kopie.scrollIntoView({ behavior: "smooth", block: "center" });
      return;

"""


def nickmonu_kopie(z):
    """Formular der nickmonu-Kopie stilllegen. Bricht den Bau ab, wenn sich formular.js so geändert hat, dass der Eingriff nicht mehr greift."""
    f = os.path.join(z, "js", "formular.js")
    t = open(f, encoding="utf-8").read()
    t2 = re.sub(r'var ENDPOINT = "[^"]*";', 'var ENDPOINT = "";', t, count=1)
    anker = "      var data = new FormData(form);"
    if t2 == t or t2.count(anker) != 1:
        raise SystemExit("FEHLER: nickmonu formular.js hat sich geändert, die Kopie würde echte Anfragen senden. Eingriff in bau.py anpassen.")
    open(f, "w", encoding="utf-8").write(t2.replace(anker, NICKMONU_FORM + anker))


def demos():
    """Kopiert die Demos nach /demos/<name>/ und liefert {pfad: csp}."""
    quellen = {n: os.path.join(QUELLE, "demos", n) for n in ("nickmonu", "hallwirth", "lindtner")}
    csps = {}
    for name, q in quellen.items():
        if not os.path.isdir(q):
            print(f"WARNUNG: Demo-Quelle fehlt: {q}")
            continue
        z = os.path.join(AUS, "demos", name)
        if os.path.exists(z):
            shutil.rmtree(z)
        shutil.copytree(q, z, ignore=shutil.ignore_patterns("*.py", "__pycache__", "generator", "*.md", "_*", ".htaccess", "sitemap.xml", "robots.txt"))
        if name == "nickmonu":
            nickmonu_kopie(z)
        # absolute Pfade auf die Unterordner umbiegen
        for f in glob.glob(os.path.join(z, "**", "*.html"), recursive=True):
            t = open(f, encoding="utf-8").read()
            if os.path.basename(f) == "404.html":
                t2 = re.sub(r'(href|src|action)="/(?!/|demos/)', rf'\1="/demos/{name}/', t)
            else:
                tiefe = 0 if os.path.dirname(f) == z else os.path.relpath(os.path.dirname(f), z).count(os.sep) + 1
                vor = "../" * tiefe
                t2 = re.sub(r'(\s(?:href|src|action))="/(?!/)([^"]*)"', lambda m: f'{m.group(1)}="{(vor + m.group(2)) or "index.html"}"', t)
            # erfundene Domains der Demos auf den echten Ort umbiegen, keine strukturierten Daten für erfundene Betriebe
            t2 = t2.replace("https://tischlerei-hallwirth.at", f"{G.DOMAIN}/demos/hallwirth").replace("https://vera-lindtner.example", f"{G.DOMAIN}/demos/lindtner")
            t2 = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', t2, flags=re.S)
            if 'name="robots"' not in t2:
                t2 = t2.replace("<head>", '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
            if t2 != t:
                open(f, "w", encoding="utf-8").write(t2)
        csps[name] = demo_csp(z)
    return csps


def header_dateien(fertig, demo_csps):
    """_headers für Cloudflare Pages. Cloudflare führt gleiche Kopfzeilen mehrerer Regeln zusammen: Deshalb steht die CSP
    nie in /*, sondern je Seite, damit die Demo-CSP nicht mit der strengen CSP der Hauptseite verbunden wird."""
    sicher = ("  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
              "  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()\n"
              "  Cross-Origin-Opener-Policy: same-origin\n  Strict-Transport-Security: max-age=31536000; includeSubDomains\n")
    csp = csp_haupt()
    z = ["# Erzeugt von generator/bau.py, nicht von Hand ändern.\n", f"/*\n{sicher}"]
    for pfad in sorted(fertig):
        p = "/404.html" if pfad.endswith(".html") else pfad
        z.append(f"{p}\n  Content-Security-Policy: {csp}\n")
    for name, c in demo_csps.items():
        z.append(f"/demos/{name}/*\n  Content-Security-Policy: {c}\n  X-Robots-Tag: noindex, nofollow\n")
    z.append("/css/*\n  Cache-Control: public, max-age=604800\n")
    z.append("/js/*\n  Cache-Control: public, max-age=604800\n")
    z.append("/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n")
    z.append("/assets/img/*\n  Cache-Control: public, max-age=2592000\n")
    schreibe("_headers", "\n".join(z))
    # Apache-Variante (falls die Seite einmal nicht auf Cloudflare Pages liegt)
    ht = ["# Apache-Variante von _headers (erzeugt von generator/bau.py)", "<IfModule mod_headers.c>",
          f'  Header always set Content-Security-Policy "{csp}"',
          '  Header always set X-Content-Type-Options "nosniff"', '  Header always set Referrer-Policy "strict-origin-when-cross-origin"',
          '  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"',
          '  Header always set Cross-Origin-Opener-Policy "same-origin"',
          '  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"',
          '  <FilesMatch "\\.(woff2)$">', '    Header set Cache-Control "public, max-age=31536000, immutable"', "  </FilesMatch>",
          "</IfModule>", "ErrorDocument 404 /404.html", "DirectoryIndex index.html", ""]
    schreibe(".htaccess", "\n".join(ht) + "\n")
    for name, c in demo_csps.items():   # <Directory> ist in .htaccess nicht erlaubt: eigene Datei im Demo-Ordner
        schreibe(f"demos/{name}/.htaccess", "\n".join(["<IfModule mod_headers.c>", f'  Header always set Content-Security-Policy "{c}"',
                                                       '  Header always set X-Robots-Tag "noindex, nofollow"', "</IfModule>",
                                                       f"ErrorDocument 404 /demos/{name}/404.html", ""]))


def manifest_icons():
    schreibe("site.webmanifest", json.dumps({"name": "Simon Monu, Webdesign", "short_name": "Simon Monu", "lang": "de-AT", "start_url": "/",
                                               "display": "browser", "background_color": "#F4F4F1", "theme_color": "#0C1A33",
                                               "icons": [{"src": "/assets/icons/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]},
                                              ensure_ascii=False, indent=1))
    # Zeichen "S.": fertige Dateien aus generator/marke/ (Schrift dort schon in Pfade umgewandelt)
    marke = os.path.join(G.BASIS, "marke")
    schreibe("assets/icons/icon.svg", open(os.path.join(marke, "favicon.svg"), encoding="utf-8").read())
    os.makedirs(os.path.join(AUS, "assets", "icons"), exist_ok=True)
    shutil.copyfile(os.path.join(marke, "apple-touch-icon.png"), os.path.join(AUS, "assets", "icons", "apple-touch-icon.png"))
    shutil.copyfile(os.path.join(marke, "favicon.ico"), os.path.join(AUS, "favicon.ico"))


def statisch():
    """Alles aus _quelle/statisch/ (css, js, schriften, og, clips) unverändert übernehmen."""
    s = os.path.join(QUELLE, "statisch")
    if os.path.isdir(s):
        shutil.copytree(s, AUS, dirs_exist_ok=True)
    else:
        print("WARNUNG: _quelle/statisch/ fehlt (css, js, fonts)")


def main():
    if os.path.isdir(AUS):
        # immer sauber neu bauen, damit keine alten Dateien liegen bleiben. Sicherung: nur einen Ordner leeren,
        # den bau.py selbst erzeugt hat (erkennbar an _headers) oder der leer ist.
        if os.listdir(AUS) and not os.path.exists(os.path.join(AUS, "_headers")):
            sys.exit(f"FEHLER: {AUS} sieht nicht nach einem Bau-Ordner aus (kein _headers). Nichts gelöscht.")
        shutil.rmtree(AUS)
    os.makedirs(AUS)
    statisch()
    bilder()
    manifest_icons()
    fertig = seiten()
    sitemap(fertig)
    dc = demos()
    header_dateien(fertig, dc)
    print(f"{len(fertig)} Seiten nach {AUS}")
    if anschrift_fehlt():
        print("WARNUNG: Impressum ohne Anschrift. Pflicht nach § 5 ECG.")
    o = G.offen()
    if o:
        print("\nNOCH OFFEN VOR DEM LIVEGANG:")
        for x in o:
            print("  -", x)
    for f in ("assets/fonts/schibsted-grotesk.woff2",):
        if not os.path.exists(os.path.join(AUS, f)):
            print("WARNUNG: Schrift fehlt:", f)
    for f in ("assets/og/og-start.jpg",):
        if not os.path.exists(os.path.join(AUS, f)):
            print("WARNUNG: OG-Bild fehlt:", f)


if __name__ == "__main__":
    main()
