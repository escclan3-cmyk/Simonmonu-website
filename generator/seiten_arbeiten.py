# -*- coding: utf-8 -*-
"""Arbeiten: Übersicht und drei Cases. Kontrastwerte werden hier gerechnet, nicht behauptet."""
from gemeinsam import *
from seiten_de import ARBEITEN, arbeit_zeile, schaufenster_eintraege, werke_liste, MESSWERTE, LIVE_SEIT, FASSUNG


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def kontrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return f"{(la + 0.05) / (lb + 0.05):.1f}".replace(".", ",") + " : 1"


def farbreihe(farben):
    """farben: [(name, hex, text_hex_oder_None, zweck)]. Kontrast gegen den zweiten Wert."""
    z = ""
    for name, hx, geg, zweck in farben:
        kt = f'<span class="mono">{kontrast(hx, geg)} gegen {geg.upper()}</span>' if geg else ""
        z += (f'<li class="farbe"><span class="farbe-feld f-{hx[1:].upper()}"></span>'
              f'<span class="farbe-text"><strong>{e(name)}</strong> <span class="mono">{hx.upper()}</span> {kt}<br>{e(zweck)}</span></li>')
    return f'<ul class="farbreihe">{z}</ul>'


def spez_tabelle(zeilen):
    z = "".join(f"<tr><th scope=\"row\">{e(a)}</th><td>{b}</td></tr>" for a, b in zeilen)
    return f'<div class="tab-wrap"><table class="tabelle tabelle-spez"><tbody>{z}</tbody></table></div>'


def case_kopf(titel, marke, sub, id, links):
    """Kopf einer Case-Seite. Darunter läuft die Arbeit live, sofern sie sich einbetten lässt."""
    ein = schaufenster_eintraege([id])
    for x in ein:
        x["case"] = None   # auf der Case-Seite selbst kein Link auf sich selbst
    live = (f'<section class="sek sek-case-bild" aria-label="Live-Ansicht"><div class="wrap">{fenster(ein)}</div></section>' if ein else "")
    return f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <p class="kicker"><span class="marke{" marke-demo" if "Demo" in marke else ""}">{marke}</span></p>
  <h1 id="h1" class="t-xl">{titel}</h1>
  <p class="lead">{sub}</p>
  <p class="knoepfe">{links}</p>
</div></section>
{live}'''


def abschnitt(nr, titel, inhalt, hid):
    return f'''<section class="sek sek-abschnitt" aria-labelledby="{hid}"><div class="wrap raster">
  <h2 id="{hid}" class="t-m spalte-titel">{titel}</h2>
  <div class="text-spalte">{inhalt}</div>
</div></section>'''


def case_ende(weiter_titel, weiter_href):
    return f'''<section class="sek sek-schluss" aria-labelledby="h-schluss"><div class="wrap">
  <h2 id="h-schluss" class="t-l">Passt so ein Ansatz zu Ihrem Vorhaben?</h2>
  <p class="knoepfe">{knopf("Erstgespräch anfragen", "/kontakt/")} {textlink(weiter_titel, weiter_href)}</p>
</div></section>'''


# ------------------------------------------------------------------------------

def arbeiten():
    n, h, l = ARBEITEN
    ist = {"lindtner": "lindtner"}
    hand = [
        ("nickmonu.com", "#0B0A09", "Libre Caslon Display, Instrument Sans", "Messing #BBA883 auf Schwarz", "Bühne, Ruhe, ein Porträt"),
        ("Tischlerei Hallwirth", "#F5F1F1", "Barlow Condensed, Barlow", "Eisenrot #943A2C auf Papier", "Werkzeichnung, Maße, Handwerk"),
        ("Vera Lindtner Coaching", "#F5F4F0", "Spectral, Hanken Grotesk", "Tiefgrün #1A2E26, Orange #E8914A", "Warm, ruhig, ein Knopf"),
        ("simonmonu.at", "#F4F4F1", "Schibsted Grotesk", "Nachtblau #0C1A33 als Bühne, Kobalt #2D55E8", "Papier, Bühne, Bemaßung"),
    ]
    zeilen = "".join(f'<tr><th scope="row">{e(a)}</th><td><span class="farbe-feld farbe-klein f-{b[1:].upper()}"></span><span class="mono">{b}</span></td><td>{e(c)}</td><td>{e(d)}</td><td>{e(f)}</td></tr>'
                     for a, b, c, d, f in hand)
    live = f'''<div class="werke-live">
    <h2 id="h-live" class="t-l">Live ausprobieren</h2>
    <p class="lead">Alle drei Seiten laufen hier im Fenster und lassen sich bedienen. Wählen Sie eine aus und klicken Sie hinein.</p>
    {fenster(schaufenster_eintraege(), "h-live")}
  </div>'''
    arb = werke(werke_liste(), "h-liste",
                '''<h2 id="h-liste" class="t-l">Drei Arbeiten, drei Handschriften.</h2>
    <p class="lead">nickmonu.com ist ein echtes Projekt. Die Tischlerei und die Coaching-Praxis sind Konzept-Demos mit erfundenen Betrieben, und das steht auch auf den Seiten.</p>''', live)
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Webdesign-Referenzen</span>Websites, die niemand für ein Template hält.</h1>
  <p class="lead">Ein echtes Projekt und zwei Konzept-Demos. Jede Seite hat ihre eigene Schrift, Farbe und Bewegung, weil jeder Auftritt eine andere Aufgabe hat.</p>
</div></section>
<section class="sek sek-werke" aria-labelledby="h-liste">{arb}</section>
<section class="sek sek-hand" aria-labelledby="h-hand"><div class="wrap">
  <h2 id="h-hand" class="t-l">Vier Handschriften</h2>
  <p class="lead">Vier Seiten, vier Aufgaben, vier Auftritte. Der Beleg dafür, dass ich nicht aus einer Vorlage baue.</p>
  <div class="tab-wrap"><table class="tabelle"><caption>Grundfarbe, Schriften und Charakter der vier Seiten</caption>
  <thead><tr><th scope="col">Seite</th><th scope="col">Grund</th><th scope="col">Schriften</th><th scope="col">Farbe</th><th scope="col">Ton</th></tr></thead>
  <tbody>{zeilen}</tbody></table></div>
</div></section>
{case_ende("Leistungen und Preise", "/leistungen/")}'''
    return ("/arbeiten/", "Webdesign-Referenzen und Arbeiten",
            "Webdesign-Referenzen: ein echtes Projekt (nickmonu.com) und zwei Konzept-Demos für Handwerk und Coaching, jeweils mit Ausgangslage und Entscheidungen.",
            inhalt, {"og": "arbeiten"})


# ------------------------------------------------------------------------------

def case_nickmonu():
    m = MESSWERTE
    kopf = case_kopf("nickmonu.com", "Echtes Projekt",
                     "Website von Schauspieler, Regisseur und Acting Coach Nicholas Monu, Salzburg und Wien. 14 Seiten, Deutsch und Englisch, live seit " + LIVE_SEIT + ".",
                     "nickmonu",
                     knopf("nickmonu.com öffnen", "https://nickmonu.com", "knopf-2", extern=True) )
    a = abschnitt(1, "Ausgangslage", "<p>Nicholas Monu arbeitet als Schauspieler, Regisseur und Acting Coach. Seine Website soll drei Dinge leisten: zeigen, wer er ist, zeigen, was er anbietet, und Anfragen möglich machen. Zwei Sprachen, weil seine Kundschaft in Salzburg und Wien gemischt ist.</p>", "h-a")
    b = abschnitt(2, "Entscheidung", "<p>Ein dunkler Grund mit Messing als einziger Akzentfarbe, Serifenschrift für den Auftritt, Grotesk für alles, was gelesen und angeklickt wird. Der Grund dafür: Die Seite soll nach Bühne aussehen und trotzdem schnell und ruhig bleiben.</p>", "h-b")
    fr = farbreihe([("Grund", "#0B0A09", "#EFE9DF", "Seitengrund, Text hell darauf"), ("Messing", "#BBA883", "#0B0A09", "Akzent für Linien und Hervorhebungen")])
    c = abschnitt(3, "Umsetzung", f'''<p>Die Farben stammen aus dem Material der Seite und sind auf Kontrast geprüft:</p>{fr}
{spez_tabelle([("Schriften", "Libre Caslon Display und Libre Caslon Text, Instrument Sans. Alle selbst gehostet."), ("Sprachen", "Deutsch und Englisch, jede Seite in beiden Fassungen."), ("Aufbau", "14 Seiten, statisch erzeugt, ohne Baukasten."), ("Datenschutz", "Keine Cookies, kein Tracking.")])}''', "h-c")
    d = abschnitt(4, f"Umbau: Fassung 25 → {FASSUNG}", f'''<p>Nach dem Livegang kam von mehreren Leuten dieselbe Rückmeldung: Die Optik überzeugt, aber die wichtigen Informationen stehen nicht dort, wo man sie sucht, besonders am Handy. Also habe ich die Startseite umgebaut.</p>
<div class="vorher-nachher"><figure>{bild("nickmonu-25-m", "nickmonu.com Fassung 25 am Handy, oberer Bereich.", "(min-width: 1024px) 280px, 45vw")}<figcaption>Fassung 25</figcaption></figure><figure>{bild("nickmonu-26-m", f"nickmonu.com Fassung {FASSUNG} am Handy, oberer Bereich.", "(min-width: 1024px) 280px, 45vw")}<figcaption>Fassung {FASSUNG}</figcaption></figure></div>''', "h-d")
    f = abschnitt(5, "Ergebnis", f'''<dl class="werte werte-breit"><div><dt>Hauptinhalt sichtbar, Desktop</dt><dd>{m["lcp_d"]}</dd></div><div><dt>Verrutschen (CLS)</dt><dd>{m["cls"]}</dd></div><div><dt>Blockierzeit (TBT)</dt><dd>{m["tbt"]}</dd></div></dl>
<p class="klein">Gemessen mit {m["quelle"]}, {m["stand"]}. Die Seite ist live und kann jederzeit selbst gemessen werden.</p>''', "h-f")
    g = abschnitt(6, "Grenzen", "<p>Es ist mein erstes Projekt, und es gehört meiner Familie. Sie sehen hier also keine Kundenarbeit unter Marktbedingungen, sondern das, was ich ohne Auftraggeber-Druck erreichen kann, und wie ich mit Rückmeldung umgehe. Eine Kundenstimme von außen habe ich noch nicht, und ich erfinde keine.</p>", "h-g")
    ld = [{"@context": "https://schema.org", "@type": "CreativeWork", "name": "nickmonu.com", "creator": {"@type": "Person", "name": NAME},
           "url": "https://nickmonu.com"}]
    return ("/arbeiten/nickmonu/", "nickmonu.com: Case", "Wie nickmonu.com entstanden ist: Ausgangslage, Entscheidungen, Umbau von Fassung 25 auf 26 und gemessene Ergebnisse.",
            "\n".join([kopf, a, b, c, d, f, g, case_ende("Zu den Konzept-Demos", "/arbeiten/hallwirth/")]), {"og": "arbeiten", "jsonld": ld})


def case_hallwirth():
    kopf = case_kopf("Tischlerei Hallwirth", "Konzept-Demo",
                     "Eine erfundene Tischlerei in Wien-Liesing, gebaut als Business-Website. Zeigt, wie ich für einen Handwerksbetrieb denke. Betrieb, Team und Aufträge sind nicht echt.",
                     "hallwirth",
                     knopf("Demo öffnen", "/demos/hallwirth/", "knopf-2", extern=True))
    a = abschnitt(1, "Ausgangslage", "<p>Wer einen Tischler sucht, sucht am Handy und will wissen: Macht der das, was ich brauche, was kostet es ungefähr, und wie erreiche ich ihn? Die meisten Handwerkerseiten beantworten das erst nach mehreren Klicks.</p>", "h-a")
    b = abschnitt(2, "Entscheidung", "<p>Die Seite nimmt ihr Vokabular aus der Werkstatt: Werkzeichnung, Maße, Graphit auf hellem Papier, ein einziges Eisenrot. Telefon und Richtpreise stehen dort, wo man sie zuerst sucht.</p>", "h-b")
    fr = farbreihe([("Papier", "#F5F1F1", "#272120", "Grund, Text in Graphit"), ("Eisenrot", "#943A2C", "#F5F1F1", "Akzent für Hervorhebungen")])
    c = abschnitt(3, "Umsetzung", f'''{fr}{spez_tabelle([("Schriften", "Barlow Condensed und Barlow, selbst gehostet."), ("Besonderheit", "Die Startseite misst das Browserfenster und passt das Foto darin ein."), ("Preise", "Richtpreise stehen bei jeder Leistung."), ("Kennzeichnung", "Oben auf jeder Seite der Demo steht, dass es den Betrieb nicht gibt.")])}''', "h-c")
    g = abschnitt(4, "Grenzen", "<p>Es ist eine Demo. Es gibt keinen Betrieb, keine echten Fotos und keine echten Preise. Bei einem echten Auftrag käme das Material vom Betrieb: Fotos der Werkstatt und der Arbeiten, die tatsächlichen Leistungen und Preise, ein Telefon, das jemand abhebt.</p>", "h-g")
    return ("/arbeiten/hallwirth/", "Tischlerei Hallwirth: Konzept-Demo", "Konzept-Demo für einen Handwerksbetrieb: Werkzeichnung, Telefon und Richtpreise sofort sichtbar. Betrieb erfunden.",
            "\n".join([kopf, a, b, c, g, case_ende("Vera Lindtner Coaching", "/arbeiten/lindtner/")]), {"og": "arbeiten"})


def case_lindtner():
    kopf = case_kopf("Vera Lindtner Coaching", "Konzept-Demo",
                     "Eine erfundene Coaching-Praxis in Wien-Neubau, gebaut als Onepager. Zeigt, wie ich für Selbstständige denke. Person und Angebote sind nicht echt.",
                     "lindtner",
                     knopf("Demo öffnen", "/demos/lindtner/", "knopf-2", extern=True))
    a = abschnitt(1, "Ausgangslage", "<p>Ein Coaching lebt davon, dass man der Person vertraut, bevor man sie kennt. Die Seite muss ruhig sein, sagen was es kostet und einen einzigen nächsten Schritt anbieten.</p>", "h-a")
    b = abschnitt(2, "Entscheidung", "<p>Ein warmer heller Grund, tiefes Grün für Ernst und ein Orange als einzige Wärme. Drei Angebote mit Preisen inklusive USt, ein Knopf zum Kennenlernen.</p>", "h-b")
    fr = farbreihe([("Grund", "#F5F4F0", "#1A2E26", "Seitengrund, Text in tiefem Grün"), ("Tiefgrün", "#1A2E26", "#F5F4F0", "Flächen und Text"), ("Orange", "#E8914A", "#1A2E26", "Akzent, nur für den Knopf und Hervorhebungen")])
    c = abschnitt(3, "Umsetzung", f'''{fr}{spez_tabelle([("Schriften", "Spectral und Hanken Grotesk, selbst gehostet."), ("Aufbau", "Ein Onepager mit mehreren Bereichen."), ("Kennzeichnung", "Im Fuß der Demo und bei den Kundenstimmen steht, dass Person und Zitate erfunden sind.")])}''', "h-c")
    g = abschnitt(4, "Grenzen", "<p>Es ist eine Demo. Person, Angebote und Preise sind erfunden. Bei einem echten Auftrag wären es Ihre Stimme, Ihre Fotos und Ihre Preise, und ich würde Sie nach echten Kundenstimmen fragen, statt welche zu erfinden.</p>", "h-g")
    return ("/arbeiten/lindtner/", "Vera Lindtner Coaching: Konzept-Demo", "Konzept-Demo für eine Coaching-Praxis: ruhiger Onepager mit drei Angeboten und einem Knopf. Person erfunden.",
            "\n".join([kopf, a, b, c, g, case_ende("Alle Arbeiten", "/arbeiten/")]), {"og": "arbeiten"})


def alle():
    return [arbeiten(), case_nickmonu(), case_hallwirth(), case_lindtner()]
