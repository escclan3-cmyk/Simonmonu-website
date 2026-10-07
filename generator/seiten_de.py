# -*- coding: utf-8 -*-
"""Seiten von simonmonu.at (Deutsch). Jede Funktion gibt (pfad, titel, beschreibung, inhalt, optionen) zurück."""
from gemeinsam import *
import zeichnung as Z

# Zahlen für die Zeichnung: Platzhalter, bau.py setzt die gemessenen Dateigrößen ein
ZAHLEN = {"html": "@@ZH@@", "css": "@@ZC@@", "fonts": "@@ZF@@", "js": "@@ZJ@@"}

# Messwerte von nickmonu.com. Quelle und Stand stehen auf der Seite, ändern hier an einer Stelle.
MESSWERTE = {"lcp_d": "0,56 s", "lcp_m": "2,4 s", "cls": "≈ 0", "tbt": "0 ms",
             "quelle": "Google PageSpeed Insights", "stand": "September 2026"}
LIVE_SEIT = "September 2026"
FASSUNG = "26"


def sek(klasse, innen, id=None, label=None):
    i = f' id="{id}"' if id else ""
    a = f' aria-labelledby="{label}"' if label else ""
    return f'<section class="sek {klasse}"{i}{a}>\n{innen}\n</section>'


# ------------------------------------------------------------------------------
# Bausteine, die auf mehreren Seiten vorkommen
# ------------------------------------------------------------------------------

def beleg_leiste():
    m = MESSWERTE
    return f'''<div class="wrap">
  <div class="beleg" data-beleg>
    <div class="beleg-text">
      <h2 class="beleg-kopf">nickmonu.com: echtes Projekt, live gemessen</h2>
      <p>Schauspieler, Regisseur und Acting Coach in Salzburg und Wien. 14 Seiten, Deutsch und Englisch, live seit {LIVE_SEIT}.</p>
      <p class="beleg-links">{textlink("Wie ich sie gebaut habe", "/arbeiten/nickmonu/")} {textlink("nickmonu.com öffnen ↗", "https://nickmonu.com", extern=True, etikett="Öffnet neu ↗")}</p>
    </div>
    <dl class="werte">
      <div><dt>Hauptinhalt sichtbar</dt><dd class="mono">{m["lcp_d"]}</dd><dd class="klein">am Desktop, bis das Wichtigste zu sehen ist</dd></div>
      <div><dt>Verrutschen</dt><dd class="mono">{m["cls"]}</dd><dd class="klein">Die Seite springt nicht, wenn Bilder laden.</dd></div>
      <div><dt>Cookies</dt><dd class="mono">keine</dd><dd class="klein">kein Tracking</dd></div>
    </dl>
    <p class="beleg-quelle klein">Gemessen mit {m["quelle"]}, {m["stand"]}</p>
  </div>
</div>'''


def arbeit_zeile(k, ebene=3):
    """Eine Arbeit als Textzeile (ohne Screenshot): Name, Art, ein Satz, zwei Wege."""
    marke = "Echtes Projekt" if k["echt"] else "Konzept-Demo"
    return f'''<article class="arbeit-zeile">
      <p class="arbeit-meta"><span class="marke{" marke-demo" if not k["echt"] else ""}">{marke}</span> {e(k["art"])}</p>
      <h{ebene} class="arbeit-titel">{e(k["titel"])}</h{ebene}>
      <p class="arbeit-text">{e(k["text"])}</p>
      <p class="arbeit-wege">{textlink("Wie ich sie gebaut habe", k["href"])} {textlink(k["oeffnen"], k["oeffnen_url"], extern=True, etikett="Öffnet neu ↗")}</p>
    </article>'''


def paket_von(k):
    return next(p for p in PAKETE if p["id"] == k["paket"])


def schaufenster_eintraege(nur=None):
    """Einträge für das Schaufenster, mit dem Paket, dem die Seite entspricht."""
    aus = []
    for k in ARBEITEN:
        if nur and k["id"] not in nur:
            continue
        p = paket_von(k)
        aus.append({"id": k["id"], "name": k["titel"], "marke": "Echtes Projekt" if k["echt"] else "Konzept-Demo",
                    "src": k["src"], "url_anzeige": k["url_anzeige"], "text": k["fenster_text"], "case": k["href"],
                    "oeffnen": k["oeffnen"], "oeffnen_url": k["oeffnen_url"],
                    "paket": p["name"], "paket_id": p["id"], "paket_ab": eur(p["ab"])})
    return aus


ARBEITEN = [
    {"id": "nickmonu", "titel": "nickmonu.com", "echt": True, "art": "14 Seiten, Deutsch und Englisch", "href": "/arbeiten/nickmonu/",
     "paket": "premium", "src": "/demos/nickmonu/", "url_anzeige": "simonmonu.at/demos/nickmonu", "oeffnen": "nickmonu.com öffnen ↗", "oeffnen_url": "https://nickmonu.com",
     "fenster_text": "Die Website von Nicholas Monu als Kopie, Deutsch und Englisch. Klicken Sie sich durch alle 14 Seiten, nur das Formular sendet hier nichts.",
     "bild": "case-nickmonu", "clip": "nickmonu",
     "alt": "nickmonu.com am Desktop: dunkler Grund, Porträt von Nicholas Monu rechts, links sein Name in großer Serifenschrift.",
     "text": "Nach dem Livegang kam von mehreren Leuten dieselbe Rückmeldung: Optik stark, aber die wichtigen Infos stehen nicht dort, wo man sie sucht. Also habe ich die Startseite umgebaut."},
    {"id": "hallwirth", "titel": "Tischlerei Hallwirth", "echt": False, "art": "Business-Website für eine erfundene Tischlerei in Wien-Liesing", "href": "/arbeiten/hallwirth/",
     "paket": "business", "src": "/demos/hallwirth/", "url_anzeige": "simonmonu.at/demos/hallwirth", "oeffnen": "Demo öffnen ↗", "oeffnen_url": "/demos/hallwirth/",
     "fenster_text": "Eine erfundene Tischlerei in Wien-Liesing. Die Seite vermisst beim Start Ihr Fenster und passt das Foto ein. Richtpreise stehen bei jeder Leistung.",
     "bild": "case-hallwirth", "clip": "hallwirth",
     "alt": "Konzept-Demo Tischlerei Hallwirth: helle Werkzeichnung, groß die Überschrift, rechts ein Foto vom Anreißen.",
     "text": "Die Startseite vermisst Ihr Browserfenster, bevor sie das Foto einpasst. Richtpreise stehen bei jeder Leistung."},
    {"id": "lindtner", "titel": "Vera Lindtner Coaching", "echt": False, "art": "Onepager für eine erfundene Coaching-Praxis in Wien-Neubau", "href": "/arbeiten/lindtner/",
     "paket": "onepager", "src": "/demos/lindtner/", "url_anzeige": "simonmonu.at/demos/lindtner", "oeffnen": "Demo öffnen ↗", "oeffnen_url": "/demos/lindtner/",
     "fenster_text": "Eine erfundene Coaching-Praxis in Wien-Neubau. Ein Onepager mit drei Angeboten, Preisen inklusive USt und einem einzigen Knopf.",
     "bild": "case-lindtner", "clip": "lindtner",
     "alt": "Konzept-Demo Vera Lindtner Coaching: heller Grund, tiefgrüne Fläche, große Serifenüberschrift.",
     "text": "Drei Angebote mit Preisen inklusive USt und ein einziger Knopf zum Kennenlernen."},
]


# ------------------------------------------------------------------------------
# START
# ------------------------------------------------------------------------------

# Texte der Arbeiten auf der Startseite: was es ist, und bei nickmonu.com der gemessene Wert
WERK_TEXT = {
    "nickmonu": {"art": "Website für Nicholas Monu, Schauspieler, Regisseur und Acting Coach. 14 Seiten, Deutsch und Englisch, live seit September 2026.",
                 "beleg": f"Am Desktop in {MESSWERTE['lcp_d']} geladen. Google wertet bis 2,5 s als gut.",
                 "alt": "nickmonu.com, erster Bildschirm: dunkler Grund, rechts ein Porträt von Nicholas Monu, links sein Name in großer Serifenschrift."},
    "hallwirth": {"art": "Business-Website für eine erfundene Tischlerei in Wien-Liesing. Telefon und Richtpreise stehen dort, wo man sie zuerst sucht.",
                  "alt": "Konzept-Demo Tischlerei Hallwirth, erster Bildschirm: heller Grund, links die Überschrift „Passt auf den Millimeter.“, rechts ein Foto vom Anreißen auf Holz."},
    "lindtner": {"art": "Onepager für eine erfundene Coaching-Praxis in Wien-Neubau. Drei Angebote mit Preisen und ein einziger Knopf.",
                 "alt": "Konzept-Demo Vera Lindtner Coaching, erster Bildschirm: tiefgrüne Fläche mit der Überschrift „Wechseln, führen, gründen.“, rechts eine Frau am Fenster."},
}


def werke_liste():
    aus = []
    for k in ARBEITEN:
        w = WERK_TEXT[k["id"]]
        oeffnen = "Live ansehen ↗" if k["echt"] else "Demo öffnen ↗"
        aus.append({"id": k["id"], "titel": k["titel"], "echt": k["echt"], "art": w["art"], "beleg": w.get("beleg"), "alt": w["alt"],
                    "href": k["href"], "oeffnen": oeffnen, "oeffnen_url": k["oeffnen_url"], "paket": paket_von(k)})
    return aus


def startseite():
    p = PAKETE
    einf = ""
    if EINFUEHRUNG:
        einf = (f'<p class="einfuehrung">Für die ersten Projekte gilt ein Einführungspreis: Onepager ab {eur(p[0]["einf"])}, Business-Website ab {eur(p[1]["einf"])}. '
                'Gleiche Arbeit, gleicher Umfang. Dafür darf ich Ihre fertige Seite als Referenz zeigen.</p>')
    hero = f'''<div class="wrap hero-innen">
  <h1 id="h1" class="hero-titel"><span class="h1-dach">Webdesign in Wien und Salzburg</span>Jede Website<br> ein Einzelstück.</h1>
  <div class="hero-text">
    <p class="lead">Ich entwerfe und programmiere Websites für Betriebe, Selbstständige und Marken in Wien und Salzburg. Ohne Baukasten, ohne Vorlage, jede Zeile selbst geschrieben.</p>
    <p class="knoepfe">{knopf("Arbeiten ansehen", "#arbeiten")} {textlink("Preise ab " + eur(p[0]["ab"]), "/leistungen/")}</p>
  </div>
</div>'''

    arb = werke(werke_liste(), "h-arbeiten",
                '''<h2 id="h-arbeiten" class="t-l">Drei Arbeiten, drei Handschriften.</h2>
    <p class="lead">nickmonu.com ist ein echtes Projekt. Die Tischlerei und die Coaching-Praxis sind Konzept-Demos mit erfundenen Betrieben, und das steht auch auf den Seiten.</p>''',
                f'<p class="werke-mehr">Alle drei lassen sich auch hier auf der Seite bedienen. {textlink("Arbeiten live ausprobieren", "/arbeiten/")}</p>')

    schritte = [("Inhalt", "Zuerst die Texte, so wie links. Was ohne Gestaltung nicht verständlich ist, rettet später kein Design."),
                ("Raster", "Dann bekommt jeder Inhalt seinen Platz, zuerst am Handy, danach am großen Bildschirm."),
                ("Schrift", "Die Schrift bestimmt den Ton. Ich wähle sie für Ihren Betrieb aus, statt eine Standardschrift zu nehmen."),
                ("Farbe und Bewegung", "Zuletzt Farbe, Bilder und Bewegung. Sparsam, damit die Seite schnell bleibt.")]
    sl = "".join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in schritte)
    folge = f'''<div class="wrap">
  <header class="schieber-kopf">
    <h2 id="h-folge" class="t-l">Derselbe Text,<br> eine andere Firma.</h2>
    <p class="lead">Links die Startseite der Tischlerei-Demo, wie der Browser sie ohne Gestaltung und ohne Bilder zeigt. Rechts dieselbe Seite fertig, Wort für Wort gleich. Ziehen Sie die Linie.</p>
  </header>
  {schieber("Die Tischlerei-Startseite ohne Gestaltung: schwarze Standardschrift auf Weiß, blaue unterstrichene Links, alles untereinander.",
            "Dieselbe Startseite fertig: Logo und Navigation oben, große Überschrift „Passt auf den Millimeter.“, rechts ein Foto vom Anreißen auf Holz.",
            "Ohne Gestaltung", "Fertig", "Grenze zwischen Rohfassung und fertiger Seite")}
  <ul class="schieber-schritte">{sl}</ul>
</div>'''

    pakete = f'''<div class="wrap">
  <header class="sek-kopf">
    <h2 id="h-pakete" class="t-l">Was eine Website kostet.</h2>
    <p class="lead">Vier Pakete mit festen Preisen. Sie sehen das Konzept, bevor ich baue, und die Korrekturrunden sind im Preis.</p>
  </header>
  {datenblatt(p)}
  <div class="pakete-fuss">
    {einf}
    <p class="klein preis-hinweis">{PREIS_HINWEIS}</p>
    <p class="alle">{textlink("Leistungen und Preise im Detail", "/leistungen/")} {textlink("Für Handwerksbetriebe", "/handwerk/")}</p>
  </div>
</div>'''

    ueber = f'''<div class="wrap ueber-raster">
  <h2 id="h-ueber" class="statement">Ihr Webdesigner für Wien und Salzburg, vom ersten Gespräch bis zur Übergabe.</h2>
  <div class="ueber-text">
    <p>Ich bin Simon Monu und arbeite allein, seit Herbst 2026 mit eigenem Gewerbe. Mein erstes Projekt ist nickmonu.com, die Website meines Vaters. Sie ist bis Fassung {FASSUNG} gewachsen, weil ich nach jeder Rückmeldung nachgebessert habe.</p>
    <p>Jede Seite baue ich selbst in Code, und auf Ihre Nachricht antworte ich selbst.</p>
    <p class="ueber-link">{textlink("Mehr über mich", "/ueber-mich/")}</p>
  </div>
</div>'''

    tel = f'<a class="kontakt-tel" href="{telefon_href()}">{e(TELEFON)}</a>' if TELEFON else ""
    kontakt = f'''<div class="wrap kontakt-raster">
  <div class="kontakt-links">
    <h2 id="h-kontakt" class="t-xl">Erzählen Sie mir von Ihrem Vorhaben.</h2>
    <p class="lead">Ein Erstgespräch dauert 30 Minuten und kostet nichts. Ich antworte innerhalb von zwei Werktagen.</p>
    <p class="kontakt-direkt"><a class="kontakt-mail" href="mailto:{MAIL}">{MAIL}</a>{tel}</p>
  </div>
  <div class="kontakt-rechts">
    {formular()}
  </div>
</div>'''

    inhalt = "\n".join([
        sek("sek-hero", hero, label="h1"),
        sek("sek-werke", arb, id="arbeiten", label="h-arbeiten"),
        sek("sek-folge", folge, id="entstehung", label="h-folge"),
        sek("sek-pakete", pakete, id="pakete", label="h-pakete"),
        sek("sek-ueber", ueber, id="ueber", label="h-ueber"),
        sek("sek-kontakt", kontakt, id="kontakt", label="h-kontakt"),
    ])
    ld = [
        {"@context": "https://schema.org", "@type": "Person", "name": NAME, "url": DOMAIN + "/", "jobTitle": "Webdesigner",
         "email": MAIL, "address": {"@type": "PostalAddress", "addressLocality": "Wals-Siezenheim", "addressCountry": "AT"}},
        {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Simon Monu, Webdesign", "url": DOMAIN + "/",
         "email": MAIL, "description": "Webdesign und Website-Erstellung in Wien und Salzburg: Onepager, Business-Websites und Shops, entworfen und programmiert ohne Baukasten.", "areaServed": [{"@type": "City", "name": "Wien"}, {"@type": "City", "name": "Salzburg"}], "address": {"@type": "PostalAddress", "addressLocality": "Wals-Siezenheim", "addressCountry": "AT"}},
    ]
    return ("/", "Webdesign Wien & Salzburg: Websites ohne Baukasten",
            "Website erstellen lassen in Wien und Salzburg: Ich entwerfe und programmiere jede Website selbst, ohne Baukasten und ohne Vorlage. Onepager ab 950 €.",
            inhalt, {"start": True, "og": "start", "jsonld": ld})


# ------------------------------------------------------------------------------
# LEISTUNGEN
# ------------------------------------------------------------------------------

def leistungen():
    p = PAKETE
    einf = ""
    if EINFUEHRUNG:
        einf = f'''<section class="sek sek-einf" aria-labelledby="h-einf"><div class="wrap raster">
  <div class="einf-text">
    <h2 id="h-einf" class="t-l">Einführungsangebot für die ersten Projekte.</h2>
    <p class="lead">Onepager ab {eur(p[0]["einf"])} statt ab {eur(p[0]["ab"])}. Business-Website ab {eur(p[1]["einf"])} statt ab {eur(p[1]["ab"])}. Gleiche Arbeit, gleicher Umfang.</p>
    <p>Dafür darf ich Ihre fertige Seite als Referenz zeigen. Wie lange das Angebot gilt, frage ich Sie gern im Erstgespräch: Es ist zeitlich begrenzt und gilt für die ersten Projekte.</p>
  </div>
</div></section>'''
    zus = "".join(f"<tr><td>{e(t)}</td><td class=\"preis-spalte\">{pr}</td></tr>" for t, pr in ZUSATZ)
    bet = "".join(f"<li><strong>{e(t)}</strong> {e(x)}</li>" for t, x in BETREUUNG_UMFANG)
    faq = [
        ("Warum kein WordPress?",
         "Ich baue in Code. Das hat einen praktischen Grund: Es gibt keine Datenbank und keine Plug-ins, die veralten und angegriffen werden können. Deshalb bleibt die Betreuung klein. Wenn Sie ausdrücklich WordPress brauchen, etwa für einen bestehenden Shop, sage ich Ihnen das offen."),
        ("Gehört mir die Domain?",
         "Ja. Die Domain läuft immer auf Ihren Namen, nie auf meinen. Sie bekommen alle Zugänge."),
        ("Was, wenn ich später selbst Texte ändern will?",
         "Ab der Business-Website gibt es auf Wunsch eine Pflege-Oberfläche für wiederkehrende Inhalte, zum Beispiel Referenzen, Aktuelles oder Team. Alles andere ändere ich für Sie im Rahmen der Betreuung."),
        ("Warum kostet das mehr als ein Baukasten?",
         "Beim Baukasten bauen Sie selbst, und die Seite lebt beim Anbieter. Bei mir ist der Preis einmalig, ich entwerfe und verantworte jede Zeile für Ihren Betrieb, und die Seite gehört Ihnen samt allen Zugängen."),
        ("Wie lange dauert es?",
         "Onepager ca. 1–2 Wochen, Business-Website ca. 3–5 Wochen, Premium ca. 5–8 Wochen, je nach Animationsumfang. Mit dem Express-Zuschlag halbiert sich die Lieferzeit."),
    ]
    faqh = "".join(f'<details class="faq"><summary><span>{e(f)}</span></summary><p>{e(a)}</p></details>' for f, a in faq)
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Website erstellen lassen: Preise und Pakete</span>Was es kostet, was drin ist, wie es läuft.</h1>
  <p class="lead">Jedes Paket hat einen festen Preis. Sie sehen ein Konzept, bevor ich baue, und die Korrekturrunden sind im Preis.</p>
</div></section>
<section class="sek sek-pakete" aria-labelledby="h-pakete"><div class="wrap">
  <h2 id="h-pakete" class="t-l">Vier Pakete</h2>
  <div class="karten karten-detail" data-stagger>{"".join(paket_karte(x, detail=True) for x in p)}</div>
  <p class="klein preis-hinweis">{PREIS_HINWEIS}</p>
</div></section>
{einf}
<section class="sek sek-zusatz" aria-labelledby="h-zusatz"><div class="wrap">
  <h2 id="h-zusatz" class="t-l">Zusatzleistungen</h2>
  <div class="tab-wrap"><table class="tabelle"><caption>Preise als Endpreise, ohne Umsatzsteuerausweis</caption><thead><tr><th scope="col">Leistung</th><th scope="col">Preis</th></tr></thead><tbody>{zus}</tbody></table></div>
  <p class="klein">Ab der Business-Website aufwärts gehört die laufende Betreuung fix zum Paket. Nur beim Onepager ist sie optional zubuchbar.</p>
</div></section>
<section class="sek sek-betreuung" aria-labelledby="h-betreuung"><div class="wrap raster">
  <div class="betreuung-text">
    <h2 id="h-betreuung" class="t-l">Was in der Betreuung steckt.</h2>
    <p class="lead">Business-Website ab 60 €/Monat, Premium und Shop ab 80 €/Monat. Mindestlaufzeit 3 Monate, danach monatlich kündbar.</p>
  </div>
  <ul class="betreuung-liste">{bet}</ul>
</div></section>
<section class="sek sek-ablauf" id="ablauf" aria-labelledby="h-ablauf"><div class="wrap">
  <h2 id="h-ablauf" class="t-l">Ablauf und Zahlung</h2>
  {ablauf_schiene()}
  <p class="zahlung">{ZAHLUNG_TEXT} Korrekturrunden sind im Paketpreis inkludiert, es gibt keine Stundenabrechnung.</p>
</div></section>
<section class="sek sek-empfehlung" aria-labelledby="h-empf"><div class="wrap raster">
  <div class="empf-text">
    <h2 id="h-empf" class="t-l">Empfehlungsprämie</h2>
    <p class="lead">Für jede erfolgreich vermittelte Neukundin oder jeden Neukunden erhalten Sie 10 % des einmaligen Projektpreises zurück, den Sie selbst bezahlt haben.</p>
    <p>Gezählt ab Vertragsabschluss und erster bezahlter Rechnung, nicht auf laufende Betreuungsgebühren. Gedeckelt auf die ersten 3 vermittelten Kundinnen und Kunden. Die Auszahlung erfolgt, sobald die erste Rechnung der neuen Kundin oder des neuen Kunden beglichen ist.</p>
  </div>
</div></section>
<section class="sek sek-faq" aria-labelledby="h-faq"><div class="wrap raster">
  <h2 id="h-faq" class="t-l faq-titel">Häufige Fragen</h2>
  <div class="faq-liste">{faqh}</div>
</div></section>
<section class="sek sek-schluss" aria-labelledby="h-schluss"><div class="wrap">
  <h2 id="h-schluss" class="t-l">Passt das für Ihr Vorhaben?</h2>
  <p class="lead">Ein Erstgespräch kostet Sie 30 Minuten. Kostenlos und unverbindlich.</p>
  <p class="knoepfe">{knopf("Erstgespräch anfragen", "/kontakt/")}</p>
</div></section>'''
    angebote = []
    for x in p:
        angebote.append({"@type": "Offer", "name": x["name"], "priceCurrency": "EUR", "url": DOMAIN + "/leistungen/#" + x["id"],
                         "priceSpecification": {"@type": "PriceSpecification", "minPrice": x["ab"], "priceCurrency": "EUR"}})
    ld = [{"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Simon Monu, Webdesign", "url": DOMAIN + "/",
           "description": "Webdesign und Website-Erstellung in Wien und Salzburg: Onepager, Business-Websites und Shops, entworfen und programmiert ohne Baukasten.", "areaServed": [{"@type": "City", "name": "Wien"}, {"@type": "City", "name": "Salzburg"}], "makesOffer": angebote}]
    return ("/leistungen/", "Website erstellen lassen: Preise und Pakete",
            "Was kostet eine Website? Webdesign zu festen Preisen in Wien und Salzburg: Onepager ab 950 €, Business-Website ab 2.400 €, Shop ab 3.800 €, Premium ab 4.800 €.",
            inhalt, {"og": "leistungen", "jsonld": ld})


# ------------------------------------------------------------------------------
# HANDWERK
# ------------------------------------------------------------------------------

def handwerk():
    p = PAKETE
    tel = ""
    if TELEFON:
        tel = f'<p class="tel-gross"><a href="{telefon_href()}">{e(TELEFON)}</a></p>'
    drin = [
        ("Ihre Nummer steht oben.", "Auf jeder Seite, am Handy antippbar. Wer anrufen will, muss nicht suchen."),
        ("Ihre Leistungen mit Richtpreis.", "Damit niemand anrufen muss, um zu erfahren, ob es überhaupt passt."),
        ("Fotos Ihrer Arbeit.", "Von echten Aufträgen. Sie liefern die Fotos, ich mache sie schnell und scharf."),
        ("Am Handy zuerst gebaut.", "Dort schaut die Kundschaft zuerst hin, also fängt der Entwurf dort an."),
        ("Google-Unternehmensprofil.", "Über das SEO-Basis-Setup (250–400 €) richte ich Ihren Eintrag ein, damit man Sie auch in der Karte findet."),
    ]
    dh = "".join(f"<li><strong>{e(t)}</strong> {e(x)}</li>" for t, x in drin)
    einf1 = f'Einführung ab {eur(p[0]["einf"])}' if EINFUEHRUNG else ""
    einf2 = f'Einführung ab {eur(p[1]["einf"])}' if EINFUEHRUNG else ""
    faq = [
        ("Was muss ich liefern?", "Fotos Ihrer Arbeit, Stichworte zu Ihren Leistungen und zwei Freigaben: eine für das Konzept, eine für die fertige Seite. Den Rest übernehme ich."),
        ("Wer schreibt die Texte?", "Wenn Sie keine Zeit zum Schreiben haben, schreibe ich sie für 60–90 € je Unterseite. Sie geben sie frei."),
        ("Was kostet es im Monat?", "Beim Onepager nichts, die Betreuung ist dort optional. Bei der Business-Website gehört die Betreuung ab 60 €/Monat dazu, mindestens 3 Monate, danach monatlich kündbar."),
        ("Gehört mir die Domain?", "Ja. Die Domain läuft immer auf Ihren Namen, nie auf meinen. Sie bekommen alle Zugänge."),
    ]
    fq = "".join(f'<details class="faq"><summary><span>{e(f)}</span></summary><p>{e(a)}</p></details>' for f, a in faq)
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Website für Handwerker in Wien und Salzburg</span>Eine neue Website, ohne dass Sie Zeit dafür haben müssen.</h1>
  <p class="lead">Für Handwerksbetriebe in Wien und Salzburg. Ihr Aufwand: ein Gespräch von 30 Minuten, Fotos Ihrer Arbeit, zwei Freigaben.</p>
  <p class="knoepfe">{knopf("Erstgespräch anfragen", "#anfrage")}</p>
</div></section>
<section class="sek sek-problem" aria-labelledby="h-problem"><div class="wrap raster">
  <div class="problem-text">
    <h2 id="h-problem" class="t-l">Wer Sie am Handy findet, will vor allem eines: Sie anrufen.</h2>
    <p>Dafür muss Ihre Nummer oben stehen, Ihre Arbeit zu sehen sein und die Seite laden, bevor der nächste Betrieb auf der Liste dran ist.</p>
    <p>Eine neue Website klingt nach Wochen Arbeit neben dem Betrieb. Die sollen Sie nicht haben. So läuft es bei mir: ein Gespräch, 30 Minuten. Dann schreibe ich ein Konzept, Sie geben es frei, und ich baue.</p>
  </div>
</div></section>
<section class="sek sek-demo" aria-labelledby="h-demo"><div class="wrap">
  <h2 id="h-demo" class="t-l">So sähe es für eine Tischlerei aus.</h2>
  <p class="lead">Die Konzept-Demo „Tischlerei Hallwirth“: Betrieb, Team und Aufträge sind erfunden, und das steht auch drauf.</p>
  <div class="demo-groß">{fenster(schaufenster_eintraege(["hallwirth"]))}</div>
</div></section>
<section class="sek sek-drin" aria-labelledby="h-drin"><div class="wrap raster">
  <h2 id="h-drin" class="t-l drin-titel">Was drin ist.</h2>
  <ul class="drin-liste" data-stagger>{dh}</ul>
</div></section>
<section class="sek sek-preise" aria-labelledby="h-preise"><div class="wrap">
  <h2 id="h-preise" class="t-l">Zwei Pakete für Betriebe.</h2>
  <div class="karten karten-zwei" data-stagger>
    {paket_karte(p[0])}
    {paket_karte(p[1])}
  </div>
  <p class="klein preis-hinweis">{PREIS_HINWEIS} {textlink("Alle Pakete und Zusatzleistungen", "/leistungen/")}</p>
</div></section>
<section class="sek sek-faq" aria-labelledby="h-faq"><div class="wrap raster">
  <h2 id="h-faq" class="t-l faq-titel">Häufige Fragen</h2>
  <div class="faq-liste">{fq}</div>
</div></section>
<section class="sek sek-anfrage" id="anfrage" aria-labelledby="h-anfrage"><div class="wrap kontakt-raster">
  <div class="kontakt-links">
    <h2 id="h-anfrage" class="t-l">{"Rufen Sie an oder schreiben Sie kurz." if TELEFON else "Schreiben Sie kurz, worum es geht."}</h2>
    {tel}
    <p class="lead">Ein Erstgespräch dauert 30 Minuten, ist kostenlos und unverbindlich. Ich antworte innerhalb von zwei Werktagen.</p>
    {formular("business")}
  </div>
  <div class="kontakt-rechts">
    <h3 class="t-m">Direkt</h3>
    {direkt_block()}
    {ring_svg(NAECHSTER_START)}
  </div>
</div></section>'''
    return ("/handwerk/", "Website für Handwerker in Wien und Salzburg",
            "Homepage für Ihren Handwerksbetrieb in Wien und Salzburg: ein Gespräch von 30 Minuten, Fotos Ihrer Arbeit, zwei Freigaben. Onepager ab 950 €.",
            inhalt, {"og": "handwerk"})


# ------------------------------------------------------------------------------
# ÜBER MICH
# ------------------------------------------------------------------------------

def ueber_mich():
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Simon Monu, Webdesigner in Wien und Salzburg</span>Sie sprechen mit dem, der baut.</h1>
  <p class="lead">Ich bin Simon Monu, Webdesigner aus Salzburg, und arbeite allein: Konzept, Gestaltung, Code und Betreuung kommen von mir.</p>
</div></section>
<section class="sek" aria-labelledby="h-wer"><div class="wrap raster">
  <h2 id="h-wer" class="t-m spalte-titel">Wer das ist</h2>
  <div class="text-spalte">
    <p>Ich bin Simon Monu, Webdesigner für Wien, seit Herbst 2026 mit eigenem Gewerbe. Mein erstes Projekt ist nickmonu.com, die Website meines Vaters. Sie ist bis Fassung {FASSUNG} gewachsen, weil ich nach jeder Rückmeldung nachgebessert habe.</p>
    <p>Ich mache das seit knapp einem Jahr. Deshalb zeige ich Ihnen nur, was ich belegen kann: eine echte Seite mit gemessenen Werten und zwei Konzept-Demos, die als solche gekennzeichnet sind.</p>
  </div>
</div></section>
<section class="sek" aria-labelledby="h-wie"><div class="wrap raster">
  <h2 id="h-wie" class="t-m spalte-titel">Wie ich arbeite</h2>
  <div class="text-spalte">
    <ol class="prinzipien">
      <li><strong>Konzept vor dem Bau.</strong> Sie sehen Aufbau, Texte und Gestaltung, bevor ich eine Zeile schreibe. Ohne Ihr Okay baue ich nichts.</li>
      <li><strong>Ich messe nach.</strong> Ladezeit, Gewicht und Verschiebungen beim Laden messe ich an der fertigen Seite und nenne die Zahlen.</li>
      <li><strong>Nach dem Livegang weiterarbeiten.</strong> Wie Besucher eine Seite wirklich nutzen, sieht man erst, wenn sie online ist. Bei nickmonu.com haben mehrere Leute dasselbe an der Startseite angemerkt, und ich habe sie daraufhin umgebaut.</li>
      <li><strong>Preis nach Paket, nicht nach Stunden.</strong> Sie wissen vorher, was es kostet. Korrekturrunden sind im Preis.</li>
    </ol>
  </div>
</div></section>
<section class="sek" aria-labelledby="h-code"><div class="wrap raster">
  <h2 id="h-code" class="t-m spalte-titel">Warum in Code</h2>
  <div class="text-spalte">
    <p>Ich baue ohne Baukasten und ohne Vorlage. Das hat Folgen für Sie: Die Seite lädt schnell, weil nichts drauf ist, was sie nicht braucht: Diese hier besteht beim ersten Aufruf aus <span data-live-n>@@N@@</span> Dateien mit zusammen <span data-live-kb>@@KB@@</span> KB. Sie setzt keine Cookies. Und sie gehört Ihnen, samt Domain und Zugängen.</p>
    <p>Wie das aussieht, zeigt ein Ausschnitt aus meinem eigenen Generator. Diese Warnung gibt er aus, wenn im Impressum die Anschrift fehlt:</p>
    <figure class="code"><pre><code>def anschrift_fehlt():
    return not (ANSCHRIFT["strasse"] and ANSCHRIFT["plz"])

# in bau.py
if anschrift_fehlt():
    print("WARNUNG: Impressum ohne Anschrift. Pflicht nach § 5 ECG.")</code></pre><figcaption>Aus generator/gemeinsam.py und bau.py von simonmonu.at</figcaption></figure>
    <p>Ein Detail, das zeigt, wie ich arbeite: Der Fehler fällt beim Bauen auf, nicht erst, wenn ein Kunde ihn findet.</p>
  </div>
</div></section>
<section class="sek sek-schluss" aria-labelledby="h-schluss"><div class="wrap">
  <h2 id="h-schluss" class="t-l">Reden wir 30 Minuten.</h2>
  <p class="lead">Kostenlos und unverbindlich.</p>
  <p class="knoepfe">{knopf("Erstgespräch anfragen", "/kontakt/")} {textlink("Meine Arbeiten ansehen", "/arbeiten/")}</p>
</div></section>'''
    return ("/ueber-mich/", "Über mich: Webdesigner in Wien und Salzburg",
            "Simon Monu, Webdesigner für Wien und Salzburg, seit Herbst 2026 mit eigenem Gewerbe. Erstes Projekt: nickmonu.com. Echte Messwerte statt Versprechen.",
            inhalt, {"og": "ueber-mich"})


# ------------------------------------------------------------------------------
# KONTAKT, DANKE
# ------------------------------------------------------------------------------

def kontakt():
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Website anfragen</span>Ein Erstgespräch kostet Sie 30 Minuten.</h1>
  <p class="lead">Kostenlos und unverbindlich. Schreiben Sie mir kurz, worum es geht. Ich antworte innerhalb von zwei Werktagen.</p>
</div></section>
<section class="sek sek-kontakt" aria-labelledby="h-anfrage"><div class="wrap kontakt-raster">
  <div class="kontakt-links">
    <h2 id="h-anfrage" class="t-m">Anfrage</h2>
    {formular()}
    <h3 class="t-m hilft">Was mir bei Ihrer Anfrage hilft</h3>
    <ul class="hilft-liste">
      <li>Welche Branche, was bieten Sie an?</li>
      <li>Wie groß soll die Seite werden: eine Seite oder mehrere?</li>
      <li>Gibt es einen Wunschtermin?</li>
      <li>Haben Sie schon eine Domain und eine bestehende Seite?</li>
    </ul>
  </div>
  <div class="kontakt-rechts">
    <h3 class="t-m">Direkt</h3>
    {direkt_block()}
    {ring_svg(NAECHSTER_START)}
  </div>
</div></section>'''
    return ("/kontakt/", "Website anfragen: kostenloses Erstgespräch",
            "Website anfragen in Wien oder Salzburg: Das Erstgespräch dauert 30 Minuten, ist kostenlos und unverbindlich. Antwort innerhalb von zwei Werktagen.",
            inhalt, {"og": "kontakt"})


def danke():
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl">Danke, Ihre Nachricht ist angekommen.</h1>
  <p class="lead" data-danke>Ich melde mich innerhalb von zwei Werktagen bei Ihnen.</p>
  <p class="knoepfe">{knopf("Zur Startseite", "/", "knopf-2")} {textlink("Meine Arbeiten ansehen", "/arbeiten/")}</p>
</div></section>'''
    return ("/danke/", "Danke", "Ihre Nachricht ist angekommen.", inhalt, {"og": "start", "robots": "noindex, follow"})


# ------------------------------------------------------------------------------
# RECHT
# ------------------------------------------------------------------------------

def _anschrift_html():
    a = ANSCHRIFT
    if a["strasse"] and a["plz"]:
        return f'{e(a["strasse"])}<br>\n    {e(a["plz"])} {e(a["ort"])}<br>\n    Österreich'
    return ('<!-- VOR DEM LIVEGANG: Straße, Hausnummer und PLZ in generator/gemeinsam.py bei ANSCHRIFT eintragen (Pflicht nach § 5 ECG) -->\n'
            f'    {e(a["ort"])}, Österreich')


def _anschrift_zeile():
    a = ANSCHRIFT
    if a["strasse"] and a["plz"]:
        return f'{e(a["strasse"])}, {e(a["plz"])} {e(a["ort"])}, Österreich'
    return f'{e(a["ort"])}, Österreich'


def impressum():
    g = GEWERBE
    if gewerbe_fehlt():
        gew = ('<!-- VOR DEM LIVEGANG: Gewerbewortlaut, Gewerbebehörde und Fachgruppe genau laut GISA-Auszug in generator/gemeinsam.py bei GEWERBE eintragen -->\n'
               '    <p>Gewerbe: Webdesign</p>')
    else:
        gew = (f'<p>Gewerbe: {e(g["wortlaut"])}<br>\n    Gewerbebehörde: {e(g["behoerde"])}<br>\n'
               f'    Mitglied der {e(g["fachgruppe"])}, Wirtschaftskammer Salzburg<br>\n'
               '    Anwendbare Vorschriften: Gewerbeordnung, einsehbar unter <a href="https://www.ris.bka.gv.at" rel="noopener" target="_blank">ris.bka.gv.at</a></p>')
    uid = f'\n    <h2>Umsatzsteuer-Identifikationsnummer</h2>\n    <p>{e(UID)}</p>\n' if UID else ""
    tel = f'<br>\n    Telefon: <a href="{telefon_href()}">{e(TELEFON)}</a>' if TELEFON else ""
    inhalt = f'''<section class="sek rechtstext" aria-labelledby="h1"><div class="wrap raster">
  <div class="rechtstext-innen">
    <h1 id="h1" class="t-xl">Impressum</h1>
    <p class="lead">Informationen nach § 5 E-Commerce-Gesetz (ECG) und Offenlegung nach § 25 Mediengesetz (MedienG).</p>

    <h2>Medieninhaber und Diensteanbieter</h2>
    <p>Simon Monu<br>
    {_anschrift_html()}</p>

    <h2>Kontakt</h2>
    <p>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a>{tel}<br>
    Anfrageformular auf der Seite <a href="/kontakt/">Kontakt</a></p>

    <h2>Unternehmensgegenstand</h2>
    <p>Webdesign: Konzeption, Gestaltung und Programmierung von Websites.</p>
    {gew}{uid}
    <h2>Kleinunternehmer</h2>
    <p>Alle Preise sind Endpreise. Als Kleinunternehmer nach § 6 Abs. 1 Z 27 UStG verrechne ich keine Umsatzsteuer.</p>

    <h2>Grundlegende Richtung</h2>
    <p>Information über die Leistungen und Arbeiten von Simon Monu als Webdesigner.</p>

    <h2>Urheberrecht</h2>
    <p>Texte, Gestaltung und Programmierung dieser Website sind urheberrechtlich geschützt. Die gezeigten Arbeiten (nickmonu.com und die beiden Konzept-Demos) gehören ihren jeweiligen Inhabern beziehungsweise sind ausdrücklich als erfundene Demos gekennzeichnet.</p>

    <h2>Schriften</h2>
    <p>Schibsted Grotesk unter der SIL Open Font License 1.1. Die Schrift liegt auf diesem Server.</p>

    <h2>Haftung für Links</h2>
    <p>Für die Inhalte verlinkter Websites sind ausschließlich deren Betreiber verantwortlich. Zum Zeitpunkt der Verlinkung waren keine rechtswidrigen Inhalte erkennbar. Werden solche bekannt, entferne ich den Link umgehend.</p>

    <p class="stand klein">Stand: Oktober 2026</p>
  </div>
</div></section>'''
    return ("/impressum/", "Impressum", "Impressum und Offenlegung von simonmonu.at.", inhalt, {"og": "start", "robots": "noindex, follow"})


def datenschutz():
    if FORMSPREE:
        form = ('<p>Für die Zustellung nutze ich den Dienst Formspree (Formspree, Inc., USA). Formspree nimmt die Formulardaten entgegen und leitet sie per E-Mail an mich weiter. '
                'Die Übermittlung in die USA erfolgt auf Grundlage der EU-Standardvertragsklauseln (Art. 46 Abs. 2 lit. c DSGVO). Wenn Sie das nicht möchten, schreiben Sie mir einfach direkt eine E-Mail.</p>\n'
                '    <p>Steht die Zustellung über Formspree nicht zur Verfügung, öffnet das Formular stattdessen Ihr E-Mail-Programm mit einer vorbereiteten Nachricht. Dann gehen die Daten über Ihren eigenen E-Mail-Anbieter direkt an mich.</p>')
    else:
        form = '<p>Das Formular öffnet Ihr E-Mail-Programm mit einer vorbereiteten Nachricht. Die Daten gehen dann über Ihren eigenen E-Mail-Anbieter direkt an mich. Es gibt keinen zwischengeschalteten Formulardienst.</p>'
    inhalt = f'''<section class="sek rechtstext" aria-labelledby="h1"><div class="wrap raster">
  <div class="rechtstext-innen">
    <h1 id="h1" class="t-xl">Datenschutz</h1>
    <p class="lead">Kurz gesagt: Diese Website setzt keine Cookies, zählt keine Besucher und bindet nichts von Dritten ein.</p>

    <h2>Verantwortlich</h2>
    <p>Simon Monu, {_anschrift_zeile()}. Für alle Fragen zum Datenschutz genügt eine E-Mail an <a href="mailto:{MAIL}">{MAIL}</a>.</p>

    <h2>Beim Aufruf der Website</h2>
    <p>Die Website wird über Cloudflare ausgeliefert (Cloudflare, Inc., USA, mit Servern auch in der EU), das in meinem Auftrag als Hoster und Auslieferungsnetzwerk arbeitet (Auftragsverarbeitung nach Art. 28 DSGVO). Dabei verarbeitet der Server technisch notwendige Zugriffsdaten: IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browser und Betriebssystem. Das ist nötig, um die Seite auszuliefern und Angriffe abzuwehren. Rechtsgrundlage ist mein berechtigtes Interesse an einem sicheren Betrieb (Art. 6 Abs. 1 lit. f DSGVO).</p>

    <h2>Keine Cookies, keine Statistik</h2>
    <p>Es gibt keine Cookies, keine Besucherzählung, keine Werbe- oder Analysedienste.</p>
    <p>Diese Website legt bis zu zwei Angaben in Ihrem Browser ab, die Ihr Gerät nie verlassen und nicht ausgewertet werden:</p>
    <ul>
      <li>Im Sitzungsspeicher (sessionStorage) einen Merker „sm-intro“, damit die kurze Startansicht nur einmal pro Besuch läuft.</li>
      <li>Im lokalen Speicher (localStorage) einen Eintrag „sm-theme“, falls Sie die Darstellung auf hell oder dunkel umstellen.</li>
    </ul>
    <p>Die eingebetteten Arbeiten liegen auf demselben Server. Zwei davon merken sich ebenso im Sitzungsspeicher, dass ihre Startansicht schon gelaufen ist: die Kopie von nickmonu.com („nm-eintritt“) und die Demo Vera Lindtner („vl-intro“). Das Formular in der nickmonu-Kopie sendet nichts.</p>
    <p>Sie dienen nur dazu, die von Ihnen aufgerufene Website wie von Ihnen gewünscht anzuzeigen. Deshalb sind sie nach § 165 Abs. 3 Telekommunikationsgesetz 2021 ohne Einwilligung zulässig. Die Sitzungsmerker verschwinden, wenn Sie den Tab schließen.</p>
    <p>Die Startansicht liest aus Ihrem Browser aus, welche Dateien dieser Seite wie groß sind, und zeigt sie an. Das passiert nur auf Ihrem Gerät. Es wird nichts an mich oder Dritte gesendet.</p>

    <h2>Schriften</h2>
    <p>Die Schriften liegen auf demselben Server wie die Website. Es besteht keine Verbindung zu Google Fonts oder einem anderen Schriftdienst.</p>

    <h2>Anfrageformular</h2>
    <p>Wenn Sie das Formular absenden, werden Ihre Angaben verarbeitet: Name, E-Mail-Adresse, auf Wunsch Betrieb oder Projekt, Paketwunsch und Ihre Nachricht. Ich nutze sie ausschließlich, um Ihre Anfrage zu beantworten. Rechtsgrundlage ist die Anbahnung eines Vertrags (Art. 6 Abs. 1 lit. b DSGVO). Ich lösche die Daten, sobald die Anfrage erledigt ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
    {form}

    <h2>E-Mail</h2>
    <p>Wenn Sie mir schreiben, verarbeite ich Ihre Nachricht und Ihre Adresse, um zu antworten (Art. 6 Abs. 1 lit. b oder f DSGVO), und lösche sie, wenn die Sache erledigt ist und keine Aufbewahrungspflichten bestehen.</p>

    <h2>Links zu anderen Websites</h2>
    <p>Links zu nickmonu.com und anderen Seiten sind gewöhnliche Links. Erst wenn Sie einen anklicken, verlassen Sie diese Website; dort gilt die Datenschutzerklärung des jeweiligen Anbieters.</p>

    <h2>Ihre Rechte</h2>
    <p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Eine erteilte Einwilligung können Sie jederzeit widerrufen. Eine E-Mail an <a href="mailto:{MAIL}">{MAIL}</a> genügt.</p>
    <p>Außerdem können Sie sich bei der Österreichischen Datenschutzbehörde beschweren: Barichgasse 40–42, 1030 Wien, <a href="https://www.dsb.gv.at" rel="noopener" target="_blank">dsb.gv.at</a>.</p>

    <p class="stand klein">Stand: September 2026</p>
  </div>
</div></section>'''
    return ("/datenschutz/", "Datenschutz", "Datenschutzerklärung von simonmonu.at: keine Cookies, keine Statistik, keine Dienste von Dritten.", inhalt,
            {"og": "start", "robots": "noindex, follow"})


def fehler():
    """404: ein leerer Rahmen für eine Seite, die es nicht gibt."""
    links = "".join(f'<li><a href="{p}">{t.replace("&", "&amp;")}</a></li>' for p, t in FUSS_SEITEN[:4])
    inhalt = f'''<section class="sek fehler" aria-labelledby="h1"><div class="wrap raster">
  <div class="fehler-text">
    <h1 id="h1" class="t-xl">Hier wurde nie etwas gebaut. Oder es ist umgezogen.</h1>
    <ul class="fehler-links">{links}</ul>
  </div>
  <div class="fehler-plan" aria-hidden="true"><div class="fehler-rahmen"><span class="mono">Diese Seite: 0 Dateien, 0 KB</span></div></div>
</div></section>'''
    return ("/404.html", "Seite nicht gefunden", "Diese Seite gibt es nicht.", inhalt, {"og": "start", "robots": "noindex, follow", "klasse": "seite-404"})


def alle():
    return [startseite(), leistungen(), handwerk(), ueber_mich(), kontakt(), danke(), impressum(), datenschutz(), fehler()]
