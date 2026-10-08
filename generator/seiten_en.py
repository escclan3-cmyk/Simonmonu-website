# -*- coding: utf-8 -*-
"""Seiten von simonmonu.at (Englisch, unter /en/). Jede Funktion gibt (pfad, titel, beschreibung, inhalt, optionen) zurück.
bau.py setzt gemeinsam.LANG = "en", bevor alle() läuft. Adressen in Links stehen deutsch und werden von P() übersetzt."""
from gemeinsam import *
import zeichnung as Z
from seiten_de import ZAHLEN
from seiten_de import sek, FASSUNG
from seiten_arbeiten import abschnitt, spez_tabelle

MESSWERTE = {"lcp_d": "0.56 s", "lcp_m": "2.4 s", "cls": "≈ 0", "tbt": "0 ms",
             "quelle": "Google PageSpeed Insights", "stand": "September 2026"}
LIVE_SEIT = "September 2026"

COURTESY = ('<p class="klein">This English text is a courtesy translation. The German version, '
            '<a href="{de}">{name}</a>, is the legally binding one.</p>')


# ------------------------------------------------------------------------------
# Bausteine
# ------------------------------------------------------------------------------

def beleg_leiste():
    m = MESSWERTE
    return f'''<div class="wrap">
  <div class="beleg" data-beleg>
    <div class="beleg-text">
      <h2 class="beleg-kopf">nickmonu.com: a real project, measured live</h2>
      <p>Actor, director and acting coach in Salzburg and Vienna. 14 pages, German and English, live since {LIVE_SEIT}.</p>
      <p class="beleg-links">{textlink("How I built it", "/arbeiten/nickmonu/")} {textlink("Open nickmonu.com ↗", "https://nickmonu.com", extern=True, etikett="Opens in a new tab ↗")}</p>
    </div>
    <dl class="werte">
      <div><dt>Main content visible</dt><dd>{m["lcp_d"]}</dd><dd class="klein">on desktop, until the essentials are visible</dd></div>
      <div><dt>Layout shift</dt><dd>{m["cls"]}</dd><dd class="klein">The page does not jump when images load.</dd></div>
      <div><dt>Cookies</dt><dd>none</dd><dd class="klein">no tracking</dd></div>
    </dl>
    <p class="beleg-quelle klein">Measured with {m["quelle"]}, {m["stand"]}</p>
  </div>
</div>'''


def arbeit_zeile(k, ebene=3):
    """Eine Arbeit als Textzeile (ohne Screenshot): Name, Art, ein Satz, zwei Wege."""
    marke = "Real project" if k["echt"] else "Concept demo"
    return f'''<article class="arbeit-zeile">
      <p class="arbeit-meta"><span class="marke{" marke-demo" if not k["echt"] else ""}">{marke}</span> {e(k["art"])}</p>
      <h{ebene} class="arbeit-titel">{e(k["titel"])}</h{ebene}>
      <p class="arbeit-text">{e(k["text"])}</p>
      <p class="arbeit-wege">{textlink("How I built it", k["href"])} {textlink(k["oeffnen"], k["oeffnen_url"], extern=True, etikett="Opens in a new tab ↗")}</p>
    </article>'''


ARBEITEN = [
    {"id": "nickmonu", "titel": "nickmonu.com", "echt": True, "art": "14 pages, German and English", "href": "/arbeiten/nickmonu/",
     "paket": "premium", "src": "/demos/nickmonu/en/", "url_anzeige": "simonmonu.at/demos/nickmonu", "oeffnen": "Open nickmonu.com ↗", "oeffnen_url": "https://nickmonu.com",
     "fenster_text": "The website of Nicholas Monu as a copy, German and English. Click through all 14 pages; only the form sends nothing here.",
     "text": "After launch, several people gave the same feedback: the look is strong, but the important information isn't where you would look for it. So I rebuilt the home page."},
    {"id": "hallwirth", "titel": "Tischlerei Hallwirth", "echt": False, "art": "Business website for an invented joinery in Vienna-Liesing", "href": "/arbeiten/hallwirth/",
     "paket": "business", "src": "/demos/hallwirth/", "url_anzeige": "simonmonu.at/demos/hallwirth", "oeffnen": "Open demo ↗", "oeffnen_url": "/demos/hallwirth/",
     "fenster_text": "An invented joinery in Vienna-Liesing (the demo is in German). At the start the page measures your window and fits the photo. Guide prices are shown for every service.",
     "text": "The home page measures your browser window before it fits the photo. Guide prices are shown for every service. The demo is in German."},
    {"id": "lindtner", "titel": "Vera Lindtner Coaching", "echt": False, "art": "One-pager for an invented coaching practice in Vienna-Neubau", "href": "/arbeiten/lindtner/",
     "paket": "onepager", "src": "/demos/lindtner/", "url_anzeige": "simonmonu.at/demos/lindtner", "oeffnen": "Open demo ↗", "oeffnen_url": "/demos/lindtner/",
     "fenster_text": "An invented coaching practice in Vienna-Neubau (the demo is in German). A one-pager with three offers, prices including VAT and a single button.",
     "text": "Three offers with prices including VAT and a single button to get to know each other. The demo is in German."},
]


def schaufenster_eintraege(nur=None):
    aus = []
    for k in ARBEITEN:
        if nur and k["id"] not in nur:
            continue
        p = next(x for x in pakete() if x["id"] == k["paket"])
        aus.append({"id": k["id"], "name": k["titel"], "marke": "Real project" if k["echt"] else "Concept demo",
                    "src": k["src"], "url_anzeige": k["url_anzeige"], "text": k["fenster_text"], "case": k["href"],
                    "oeffnen": k["oeffnen"], "oeffnen_url": k["oeffnen_url"],
                    "paket": p["name"], "paket_id": p["id"], "paket_ab": eur(p["ab"])})
    return aus


# ------------------------------------------------------------------------------
# START
# ------------------------------------------------------------------------------

WERK_TEXT = {
    "nickmonu": {"art": "Website for Nicholas Monu, actor, director and acting coach. 14 pages, German and English, live since September 2026.",
                 "beleg": f"Loads in {MESSWERTE['lcp_d']} on desktop. Google rates anything up to 2.5 s as good.",
                 "alt": "nickmonu.com, first screen: dark ground, a portrait of Nicholas Monu on the right, his name in a large serif on the left."},
    "hallwirth": {"art": "Business website for an invented joinery in Vienna-Liesing. Phone number and guide prices sit where people look first. The demo is in German.",
                  "alt": "Concept demo Tischlerei Hallwirth, first screen: light ground, the headline „Passt auf den Millimeter.“ on the left, a photo of marking out wood on the right."},
    "lindtner": {"art": "One-pager for an invented coaching practice in Vienna-Neubau. Three offers with prices and a single button. The demo is in German.",
                 "alt": "Concept demo Vera Lindtner Coaching, first screen: deep green area with the headline „Wechseln, führen, gründen.“, a woman at a window on the right."},
}


def werke_liste():
    aus = []
    for k in ARBEITEN:
        w = WERK_TEXT[k["id"]]
        p = next(x for x in pakete() if x["id"] == k["paket"])
        aus.append({"id": k["id"], "titel": k["titel"], "echt": k["echt"], "art": w["art"], "beleg": w.get("beleg"), "alt": w["alt"],
                    "href": k["href"], "oeffnen": "View live ↗" if k["echt"] else "Open demo ↗", "oeffnen_url": k["oeffnen_url"], "paket": p})
    return aus


def startseite():
    p = pakete()
    einf = ""
    if EINFUEHRUNG:
        einf = (f'<p class="einfuehrung">Launch offer {einf_bedingung()}: One-pager from {eur(p[0]["einf"])}, Business website from {eur(p[1]["einf"])}. '
                'Same work, same scope. In return, I may show your finished site as a reference.</p>')
    hero = f'''<div class="wrap hero-innen">
  <h1 id="h1" class="hero-titel"><span class="h1-dach">Web design in Vienna and Salzburg</span>Every website<br> a one-off.</h1>
  <div class="hero-text">
    <p class="lead">I design and code websites for businesses, freelancers and brands in Vienna and Salzburg. No site builder, no template: individually designed and developed.</p>
    <p class="knoepfe">{knopf("See my work", "#arbeiten")} {textlink("Prices from " + eur(p[0]["ab"]), "/leistungen/")}</p>
  </div>
</div>'''

    arb = werke(werke_liste(), "h-arbeiten",
                '''<h2 id="h-arbeiten" class="t-l">Three projects, three distinct styles.</h2>
    <p class="lead">nickmonu.com is a real project. The joinery and the coaching practice are concept demos with invented businesses, and the sites say so.</p>''',
                f'<p class="werke-mehr">All three can be used right here on this site. {textlink("Try the work live", "/arbeiten/")}</p>')

    schritte = [("Content", "First the copy, as on the left. If it is not clear without design, no design will rescue it later."),
                ("Grid", "Then every piece of content gets its place, on mobile first, then on the large screen."),
                ("Type", "The typeface sets the tone. I choose it for your business instead of using a default."),
                ("Colour and motion", "Colour, images and motion come last, and sparingly, so the site stays fast.")]
    sl = "".join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in schritte)
    folge = f'''<div class="wrap">
  <header class="schieber-kopf">
    <h2 id="h-folge" class="t-l">Same words,<br> a different company.</h2>
    <p class="lead">On the left, the home page of the joinery demo as a browser shows it without design or images. On the right, the same page finished, word for word. Drag the line.</p>
  </header>
  {schieber("The joinery home page without design: black default type on white, blue underlined links, everything stacked.",
            "The same page finished: logo and navigation at the top, a large headline, a photo of marking out on wood on the right.",
            "Without design", "Finished", "Divider between the raw and the finished page")}
  <ul class="schieber-schritte">{sl}</ul>
</div>'''

    pakete_html = f'''<div class="wrap">
  <header class="sek-kopf">
    <h2 id="h-pakete" class="t-l">What a website costs.</h2>
    <p class="lead">Four packages at fixed prices. You see the concept before I build, and the rounds of revisions are included.</p>
  </header>
  {datenblatt(p)}
  <div class="pakete-fuss">
    {einf}
    <p class="klein preis-hinweis">{PREIS_HINWEIS_EN}</p>
    <p class="alle">{textlink("Services and pricing in detail", "/leistungen/")} {textlink("For trades businesses", "/handwerk/")}</p>
  </div>
</div>'''

    ueber = f'''<div class="wrap ueber-raster">
  <h2 id="h-ueber" class="statement">Your web designer for Vienna and Salzburg, from the first call to the handover.</h2>
  <div class="ueber-text">
    <p>I am Simon Monu and I work on my own, with my own business since autumn 2026. My first project is nickmonu.com, my father's website. It has grown to version {FASSUNG} because I improved it after every piece of feedback.</p>
    <p>I develop every site individually in code, and I answer your message personally.</p>
    <p class="ueber-link">{textlink("More about me", "/ueber-mich/")}</p>
  </div>
</div>'''

    tel = f'<a class="kontakt-tel" href="{telefon_href()}">{e(TELEFON)}</a>' if TELEFON else ""
    kontakt = f'''<div class="wrap kontakt-raster">
  <div class="kontakt-links">
    <h2 id="h-kontakt" class="t-xl">Tell me about your project.</h2>
    <p class="lead">An intro call takes 30 minutes and costs nothing. I reply within two working days.</p>
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
        sek("sek-pakete", pakete_html, id="pakete", label="h-pakete"),
        sek("sek-ueber", ueber, id="ueber", label="h-ueber"),
        sek("sek-kontakt", kontakt, id="kontakt", label="h-kontakt"),
    ])
    ld = [
        {"@context": "https://schema.org", "@type": "Person", "name": NAME, "url": DOMAIN + "/en/", "jobTitle": "Web designer",
         "email": MAIL, "address": {"@type": "PostalAddress", "addressLocality": "Wals-Siezenheim", "addressCountry": "AT"}},
        {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Simon Monu, web design", "url": DOMAIN + "/en/",
         "email": MAIL, "description": "Web design and website building in Vienna and Salzburg: one-pagers, business websites and shops, designed and coded without site builders.", "areaServed": [{"@type": "City", "name": "Vienna"}, {"@type": "City", "name": "Salzburg"}], "address": {"@type": "PostalAddress", "addressLocality": "Wals-Siezenheim", "addressCountry": "AT"}},
    ]
    return ("/en/", "Web design Vienna & Salzburg: websites without templates",
            "Website design in Vienna and Salzburg: I design and code every website myself, with no site builder and no template. One-pager from €950.",
            inhalt, {"start": True, "og": "start", "jsonld": ld})


# ------------------------------------------------------------------------------
# LEISTUNGEN
# ------------------------------------------------------------------------------

def leistungen():
    p = pakete()
    einf = ""
    if EINFUEHRUNG:
        einf = f'''<section class="sek sek-einf" aria-labelledby="h-einf"><div class="wrap raster">
  <div class="einf-text">
    <h2 id="h-einf" class="t-l">Launch offer for my first {EINF_ANZAHL} projects.</h2>
    <p class="lead">One-pager from {eur(p[0]["einf"])} instead of from {eur(p[0]["ab"])}. Business website from {eur(p[1]["einf"])} instead of from {eur(p[1]["ab"])}. Same work, same scope.</p>
    <p>In return, I may show your finished site as a reference. The offer applies {einf_bedingung()}; care is not affected. Whether one of the {EINF_ANZAHL} places is still free, I will tell you in the intro call.</p>
  </div>
</div></section>'''
    zus = "".join(f"<tr><td>{e(t)}</td><td class=\"preis-spalte\">{pr}</td></tr>" for t, pr in ZUSATZ_EN)
    bet = "".join(f"<li><strong>{e(t)}</strong> {e(x)}</li>" for t, x in BETREUUNG_UMFANG_EN)
    faq = [
        ("Why no WordPress?",
         "I build in code. There is a practical reason: there is no database and no plug-ins that can go out of date and be attacked. That is why care stays small. If you explicitly need WordPress, for example for an existing shop, I will tell you openly."),
        ("Do I own the domain?",
         "Yes. The domain is always registered in your name, never mine. You get all access details."),
        ("What if I want to change texts myself later?",
         "From the Business website upwards there is, on request, an editing interface for recurring content, for example references, news or team. I make all other changes for you as part of the care plan."),
        ("Why does it cost more than a site builder?",
         "With a site builder you build it yourself, and the site lives with the provider. With me the price is one-off, I design and take responsibility for every line for your business, and the site belongs to you, including all access details."),
        ("How long does it take?",
         "One-pager approx. 1–2 weeks, Business website approx. 3–5 weeks, Premium approx. 5–8 weeks, depending on the amount of animation. With the express surcharge the delivery time is halved."),
    ]
    faqh = "".join(f'<details class="faq"><summary><span>{e(f)}</span></summary><p>{e(a)}</p></details>' for f, a in faq)
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Website design: prices and packages</span>What it costs, what is included, how it works.</h1>
  <p class="lead">Every package has a fixed price. You see a concept before I build, and the revision rounds are included in the price.</p>
</div></section>
<section class="sek sek-pakete" aria-labelledby="h-pakete"><div class="wrap">
  <h2 id="h-pakete" class="t-l">Four packages</h2>
  <div class="karten karten-detail" data-stagger>{"".join(paket_karte(x, detail=True) for x in p)}</div>
  <p class="klein preis-hinweis">{PREIS_HINWEIS_EN}</p>
</div></section>
{einf}
<section class="sek sek-zusatz" aria-labelledby="h-zusatz"><div class="wrap">
  <h2 id="h-zusatz" class="t-l">Extras</h2>
  <p class="klein">{ZUSATZ_HINWEIS_EN}</p>
  <div class="tab-wrap" tabindex="0" role="region" aria-label="Additional services and prices"><table class="tabelle"><caption>Prices are final prices, without VAT shown</caption><thead><tr><th scope="col">Service</th><th scope="col">Price</th></tr></thead><tbody>{zus}</tbody></table></div>
  <p class="klein">From the Business website upwards, care is added to the package price (plus €60 or €80/month, minimum 3 months) so that your site is looked after from the start. Only with the One-pager is it an optional add-on. Example, Business website: €2,400 one-off plus 3 × €60 makes at least €2,580 for the build and the first three months.</p>
</div></section>
<section class="sek sek-betreuung" aria-labelledby="h-betreuung"><div class="wrap raster">
  <div class="betreuung-text">
    <h2 id="h-betreuung" class="t-l">What care includes.</h2>
    <p class="lead">Business website €60/month, Premium and Shop €80/month, optional €60/month with the One-pager. Minimum term 3 months, then cancellable monthly. This amount is added to the package price.</p>
  </div>
  <ul class="betreuung-liste">{bet}</ul>
</div></section>
<section class="sek sek-ablauf" id="ablauf" aria-labelledby="h-ablauf"><div class="wrap">
  <h2 id="h-ablauf" class="t-l">Process and payment</h2>
  {ablauf_schiene()}
  <p class="zahlung">{ZAHLUNG_TEXT_EN} Revision rounds are included in the package price; there is no hourly billing.</p>
</div></section>
<section class="sek sek-empfehlung" aria-labelledby="h-empf"><div class="wrap raster">
  <div class="empf-text">
    <h2 id="h-empf" class="t-l">Referral bonus</h2>
    <p class="lead">For every new client you successfully refer, you receive 10 % of the one-off project price you paid yourself.</p>
    <p>Counted from contract signing and the first paid invoice, not on ongoing care fees. Capped at the first 3 referred clients. The payout happens as soon as the new client's first invoice has been paid.</p>
  </div>
</div></section>
<section class="sek sek-faq" aria-labelledby="h-faq"><div class="wrap raster">
  <h2 id="h-faq" class="t-l faq-titel">Frequently asked questions</h2>
  <div class="faq-liste">{faqh}</div>
</div></section>
<section class="sek sek-schluss" aria-labelledby="h-schluss"><div class="wrap">
  <h2 id="h-schluss" class="t-l">Is this right for your project?</h2>
  <p class="lead">An intro call costs you 30 minutes. Free and non-binding.</p>
  <p class="knoepfe">{knopf("Book an intro call", "/kontakt/")}</p>
</div></section>'''
    angebote = []
    for x in p:
        angebote.append({"@type": "Offer", "name": x["name"], "priceCurrency": "EUR", "url": DOMAIN + "/en/services/#" + x["id"],
                         "priceSpecification": {"@type": "PriceSpecification", "minPrice": x["ab"], "priceCurrency": "EUR"}})
    ld = [{"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Simon Monu, web design", "url": DOMAIN + "/en/",
           "description": "Web design and website building in Vienna and Salzburg: one-pagers, business websites and shops, designed and coded without site builders.", "areaServed": [{"@type": "City", "name": "Vienna"}, {"@type": "City", "name": "Salzburg"}], "makesOffer": angebote}]
    return ("/en/services/", "Website design: prices and packages",
            "What does a website cost? Web design at fixed prices in Vienna and Salzburg: one-pager from €950, business website from €2,400, shop from €3,800, premium from €4,800.",
            inhalt, {"og": "leistungen", "jsonld": ld})


# ------------------------------------------------------------------------------
# HANDWERK
# ------------------------------------------------------------------------------

def handwerk():
    p = pakete()
    tel = ""
    if TELEFON:
        tel = f'<p class="tel-gross"><a href="{telefon_href()}">{e(TELEFON)}</a></p>'
    drin = [
        ("Your number is at the top.", "On every page, tappable on mobile. Anyone who wants to call does not have to search."),
        ("Your services with a guide price.", "So nobody has to call just to find out whether it fits."),
        ("Photos of your work.", "From real jobs. You supply the photos, I make them quick and sharp."),
        ("Built mobile-first.", "That is where customers look first, so the design starts there."),
        ("Google Business Profile.", "With the SEO setup (€250–400) I set up your Google Business Profile listing so people can find you on the map, too."),
    ]
    dh = "".join(f"<li><strong>{e(t)}</strong> {e(x)}</li>" for t, x in drin)
    faq = [
        ("What do I have to provide?", "Photos of your work, keywords about your services and two approvals: one for the concept, one for the finished site. I take care of the rest."),
        ("Who writes the texts?", "If you have no time to write, I write them for €60–90 per subpage. You approve them."),
        ("What does it cost per month?", "Nothing with the One-pager, where care is optional (€60/month). With the Business website, €60/month for care is added to the package price, for at least 3 months, then cancellable monthly."),
        ("Do I own the domain?", "Yes. The domain is always registered in your name, never mine. You get all access details."),
    ]
    fq = "".join(f'<details class="faq"><summary><span>{e(f)}</span></summary><p>{e(a)}</p></details>' for f, a in faq)
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Websites for tradespeople in Vienna and Salzburg</span>A new website, without you having to find the time for it.</h1>
  <p class="lead">For trades businesses in Vienna and Salzburg. Your effort: one conversation of 30 minutes, photos of your work, two approvals.</p>
  <p class="knoepfe">{knopf("Book an intro call", "#anfrage")}</p>
</div></section>
<section class="sek sek-problem" aria-labelledby="h-problem"><div class="wrap raster">
  <div class="problem-text">
    <h2 id="h-problem" class="t-l">People who find you on their phone mostly want one thing: to call you.</h2>
    <p>For that, your number has to be at the top, your work has to be visible, and the page has to load before the next business on the list does.</p>
    <p>A new website sounds like weeks of work next to running your business. You should not have that. This is how it works with me: one conversation, 30 minutes. Then I write a concept, you approve it, and I build.</p>
  </div>
</div></section>
<section class="sek sek-demo" aria-labelledby="h-demo"><div class="wrap">
  <h2 id="h-demo" class="t-l">How it would look for a joinery.</h2>
  <p class="lead">The concept demo “Tischlerei Hallwirth”: business, team and jobs are invented, and it says so. The demo itself is in German.</p>
  <div class="demo-groß">{fenster(schaufenster_eintraege(["hallwirth"]))}</div>
</div></section>
<section class="sek sek-drin" aria-labelledby="h-drin"><div class="wrap raster">
  <h2 id="h-drin" class="t-l drin-titel">What is included.</h2>
  <ul class="drin-liste" data-stagger>{dh}</ul>
</div></section>
<section class="sek sek-preise" aria-labelledby="h-preise"><div class="wrap">
  <h2 id="h-preise" class="t-l">Two packages for trades businesses.</h2>
  <div class="karten karten-zwei" data-stagger>
    {paket_karte(p[0])}
    {paket_karte(p[1])}
  </div>
  <p class="klein preis-hinweis">{PREIS_HINWEIS_EN} {textlink("All packages and extras", "/leistungen/")}</p>
</div></section>
<section class="sek sek-faq" aria-labelledby="h-faq"><div class="wrap raster">
  <h2 id="h-faq" class="t-l faq-titel">Frequently asked questions</h2>
  <div class="faq-liste">{fq}</div>
</div></section>
<section class="sek sek-anfrage" id="anfrage" aria-labelledby="h-anfrage"><div class="wrap kontakt-raster">
  <div class="kontakt-links">
    <h2 id="h-anfrage" class="t-l">{"Call me or write a short message." if TELEFON else "Write briefly what it is about."}</h2>
    {tel}
    <p class="lead">An intro call takes 30 minutes, is free and non-binding. I reply within two working days.</p>
    {formular("business")}
  </div>
  <div class="kontakt-rechts">
    <h3 class="t-m">Direct</h3>
    {direkt_block()}
    {ring_svg(NAECHSTER_START)}
  </div>
</div></section>'''
    return ("/en/trades/", "Websites for tradespeople in Vienna and Salzburg",
            "A website for your trades business in Vienna and Salzburg: one 30-minute conversation, photos of your work, two approvals. One-pager from €950.",
            inhalt, {"og": "handwerk"})


# ------------------------------------------------------------------------------
# ÜBER MICH
# ------------------------------------------------------------------------------

def ueber_mich():
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Simon Monu, web designer in Vienna and Salzburg</span>You talk to the person who builds.</h1>
  <p class="lead">I am Simon Monu, a web designer from Salzburg, and I work on my own: concept, design, code and care all come from me.</p>
</div></section>
<section class="sek" aria-labelledby="h-wer"><div class="wrap raster">
  <h2 id="h-wer" class="t-m spalte-titel">Who I am</h2>
  <div class="text-spalte">
    <p>I am Simon Monu, a web designer for Vienna, with my own business since autumn 2026. My first project is nickmonu.com, my father's website. It has grown to version {FASSUNG} because I improved it after every piece of feedback.</p>
    <p>I have been doing this for just under a year. That is why I only show you what I can prove: a real site with measured results and two concept demos that are labelled as such.</p>
  </div>
</div></section>
<section class="sek" aria-labelledby="h-wie"><div class="wrap raster">
  <h2 id="h-wie" class="t-m spalte-titel">How I work</h2>
  <div class="text-spalte">
    <ol class="prinzipien">
      <li><strong>Concept before the build.</strong> You see structure, copy and design before I write a line. Without your OK I build nothing.</li>
      <li><strong>I measure.</strong> Load time, weight and layout shifts I measure on the finished site, and I give you the numbers.</li>
      <li><strong>Keep working after launch.</strong> How visitors really use a site only becomes clear once it is online. For nickmonu.com, several people pointed out the same thing about the home page, and I rebuilt it accordingly.</li>
      <li><strong>Price per package, not per hour.</strong> You know beforehand what it costs. Revision rounds are included in the price.</li>
    </ol>
  </div>
</div></section>
<section class="sek" aria-labelledby="h-code"><div class="wrap raster">
  <h2 id="h-code" class="t-m spalte-titel">Why in code</h2>
  <div class="text-spalte">
    <p>I build without a site builder and without a template. That has consequences for you: the page loads fast because nothing is on it that it does not need. This one consists, on a first visit, of <span data-live-n>@@N@@</span> files totalling <span data-live-kb>@@KB@@</span> KB. It sets no cookies. And it belongs to you, including domain and access details.</p>
    <p>What that looks like is shown by an excerpt from my own generator. It prints this warning when the address is missing from the legal notice:</p>
    <figure class="code"><pre tabindex="0" role="region" aria-label="Code excerpt"><code>def anschrift_fehlt():
    return not (ANSCHRIFT["strasse"] and ANSCHRIFT["plz"])

# in bau.py
if anschrift_fehlt():
    print("WARNUNG: Impressum ohne Anschrift. Pflicht nach § 5 ECG.")</code></pre><figcaption>From generator/gemeinsam.py and bau.py of simonmonu.at (the message is in German, like the generator)</figcaption></figure>
    <p>A detail that shows how I work: the error is caught at build time, not when a client finds it.</p>
  </div>
</div></section>
<section class="sek sek-schluss" aria-labelledby="h-schluss"><div class="wrap">
  <h2 id="h-schluss" class="t-l">Let's talk for 30 minutes.</h2>
  <p class="lead">Free and non-binding.</p>
  <p class="knoepfe">{knopf("Book an intro call", "/kontakt/")} {textlink("See my work", "/arbeiten/")}</p>
</div></section>'''
    return ("/en/about/", "About: web designer in Vienna and Salzburg",
            "Simon Monu, web designer for Vienna and Salzburg, with his own business since autumn 2026. First project: nickmonu.com. Real measurements instead of promises.",
            inhalt, {"og": "ueber-mich"})


# ------------------------------------------------------------------------------
# KONTAKT, DANKE
# ------------------------------------------------------------------------------

def kontakt():
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Request a website</span>An intro call costs you 30 minutes.</h1>
  <p class="lead">Free and non-binding. Tell me briefly what it is about. I reply within two working days.</p>
</div></section>
<section class="sek sek-kontakt" aria-labelledby="h-anfrage"><div class="wrap kontakt-raster">
  <div class="kontakt-links">
    <h2 id="h-anfrage" class="t-m">Enquiry</h2>
    {formular()}
    <h3 class="t-m hilft">What helps me with your enquiry</h3>
    <ul class="hilft-liste">
      <li>Which industry are you in, and what do you offer?</li>
      <li>How big should the site be: one page or several?</li>
      <li>Is there a preferred date?</li>
      <li>Do you already have a domain and an existing site?</li>
    </ul>
  </div>
  <div class="kontakt-rechts">
    <h3 class="t-m">Direct</h3>
    {direkt_block()}
    {ring_svg(NAECHSTER_START)}
  </div>
</div></section>'''
    return ("/en/contact/", "Request a website: free intro call",
            "Request a website in Vienna or Salzburg: the intro call takes 30 minutes and is free and non-binding. Reply within two working days.",
            inhalt, {"og": "kontakt"})


def danke():
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl">Thank you, your message has arrived.</h1>
  <p class="lead" data-danke>I will get back to you within two working days.</p>
  <p class="knoepfe">{knopf("To the home page", "/", "knopf-2")} {textlink("See my work", "/arbeiten/")}</p>
</div></section>'''
    return ("/en/thanks/", "Thank you", "Your message has arrived.", inhalt, {"og": "start", "robots": "noindex, follow"})


# ------------------------------------------------------------------------------
# RECHT (Höflichkeitsübersetzung, verbindlich ist die deutsche Fassung)
# ------------------------------------------------------------------------------

def _anschrift_html():
    a = ANSCHRIFT
    if a["strasse"] and a["plz"]:
        return f'{e(a["strasse"])}<br>\n    {e(a["plz"])} {e(a["ort"])}<br>\n    Austria'
    return ('<!-- BEFORE GOING LIVE: enter street, number and postcode in generator/gemeinsam.py under ANSCHRIFT (required by § 5 ECG) -->\n'
            f'    {e(a["ort"])}, Austria')


def _anschrift_zeile():
    a = ANSCHRIFT
    if a["strasse"] and a["plz"]:
        return f'{e(a["strasse"])}, {e(a["plz"])} {e(a["ort"])}, Austria'
    return f'{e(a["ort"])}, Austria'


def impressum():
    g = GEWERBE
    if gewerbe_fehlt():
        gew = ('<!-- BEFORE GOING LIVE: enter trade wording, trade authority and professional group exactly as in the GISA extract in generator/gemeinsam.py under GEWERBE -->\n'
               '    <p>Trade: web design</p>')
    else:
        gew = (f'<p>Trade: {e(g["wortlaut"])}<br>\n    Trade authority: {e(g["behoerde"])}<br>\n'
               f'    Member of the {e(g["fachgruppe"])} (advertising and market communication), Wirtschaftskammer Salzburg<br>\n'
               '    Applicable regulations: Trade Regulation Act (Gewerbeordnung), available at <a href="https://www.ris.bka.gv.at" rel="noopener" target="_blank">ris.bka.gv.at</a></p>')
    uid = f'\n    <h2>VAT identification number</h2>\n    <p>{e(UID)}</p>\n' if UID else ""
    tel = f'<br>\n    Phone: <a href="{telefon_href()}">{e(TELEFON)}</a>' if TELEFON else ""
    inhalt = f'''<section class="sek rechtstext" aria-labelledby="h1"><div class="wrap raster">
  <div class="rechtstext-innen">
    <h1 id="h1" class="t-xl">Legal notice</h1>
    <p class="lead">Information under § 5 of the Austrian E-Commerce Act (ECG) and disclosure under § 25 of the Austrian Media Act (MedienG).</p>
    {COURTESY.format(de=P("/impressum/").replace("/en/legal-notice/", "/impressum/"), name="Impressum")}

    <h2>Media owner and service provider</h2>
    <p>Simon Monu<br>
    {_anschrift_html()}</p>

    <h2>Contact</h2>
    <p>Email: <a href="mailto:{MAIL}">{MAIL}</a>{tel}<br>
    Enquiry form on the <a href="{P("/kontakt/")}">Contact</a> page</p>

    <h2>Business purpose</h2>
    <p>Web design: concept, design and programming of websites.</p>
    {gew}{uid}
    <h2>Small business</h2>
    <p>All prices are final prices. As a small business under § 6 (1) no. 27 of the Austrian VAT Act (UStG) I do not charge VAT.</p>

    <h2>Basic orientation</h2>
    <p>Information about the services and work of Simon Monu as a web designer.</p>

    <h2>Copyright</h2>
    <p>The texts, design and programming of this website are protected by copyright. The work shown (nickmonu.com and the two concept demos) belongs to its respective owners or is expressly labelled as an invented demo.</p>
    <p>Image credits: in the copy of nickmonu.com the photos are by Joachim Bergauer and S. Monu (each © with the creators). The stock photos in the two concept demos come from Unsplash and Pexels and are used under their licences. The creators are named next to the images in the demos. The portraits there do not show the invented people.</p>

    <h2>Fonts</h2>
    <p>Schibsted Grotesk and Fragment Mono under the SIL Open Font License 1.1. The typefaces are hosted on this server.</p>

    <h2>Liability for links</h2>
    <p>The operators of linked websites are solely responsible for their content. At the time of linking, no unlawful content was apparent. If such content becomes known, I will remove the link promptly.</p>

    <p class="stand klein">As of: October 2026</p>
  </div>
</div></section>'''
    return ("/en/legal-notice/", "Legal notice", "Legal notice and disclosure of simonmonu.at.", inhalt, {"og": "start", "robots": "noindex, follow"})


def _rechtsseite(h1, lead, courtesy, koerper, stand):
    return f'''<section class="sek rechtstext" aria-labelledby="h1"><div class="wrap raster">
  <div class="rechtstext-innen">
    <h1 id="h1" class="t-xl">{h1}</h1>
    <p class="lead">{lead}</p>
    {courtesy}
{koerper}
    <p class="stand klein">{stand}</p>
  </div>
</div></section>'''


def datenschutz():
    if FORMSPREE:
        form = f'''<p>When you submit the form, I process your name, your email address and your message and, if you give them, your business or project and package preference. Name, email address and message are required because otherwise I cannot reply. Everything else is optional. I also record that you agreed to the transmission.</p>
    <p>The purpose is to answer your enquiry and to make you an offer. The legal basis is the performance of pre-contractual measures at your request (Art. 6 (1) (b) GDPR).</p>
    <p>To deliver your message I use the service Formspree (Formspree, Inc., USA). Formspree receives the form data, stores it and forwards it to me by email. Formspree is based in the USA. According to its own information, Formspree bases transfers from the EU on the standard contractual clauses of the European Commission. In addition, I transmit your details only if you expressly agree in the form (Art. 49 (1) (a) GDPR). There is a risk that US authorities can access the data and that your rights are harder to enforce there than in the EU. You can withdraw your consent at any time with effect for the future; an email to <a href="mailto:{MAIL}">{MAIL}</a> is enough. If you do not want to agree, simply write to me directly by email.</p>
    <p>If delivery through Formspree is not available, the form opens your email program with a prepared message instead. The data then goes directly to me through your own email provider.</p>'''
    else:
        form = '<p>The form opens your email program with a prepared message. The data then goes directly to me through your own email provider. There is no form service in between.</p>'
    tel = f' Phone: <a href="{telefon_href()}">{e(TELEFON)}</a>.' if TELEFON else ""
    koerper = f'''
    <h2>Controller</h2>
    <p>Simon Monu, {_anschrift_zeile()}. Email: <a href="mailto:{MAIL}">{MAIL}</a>.{tel} For all questions about data protection, an email is enough.</p>

    <h2>When you visit the website (hosting)</h2>
    <p>This website is hosted on GitHub Pages (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). When you open a page, GitHub processes technically necessary access data, above all your IP address as well as date and time, the page requested, your browser and your operating system. According to GitHub, the IP address of visitors is stored for security reasons even if you have no GitHub account. For the delivery network, storage period and GitHub's responsibility, GitHub's <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener" target="_blank">privacy statement</a> applies. I do not evaluate this access data myself.</p>
    <p>The purpose is to deliver the page and to run it securely and stably. The legal basis is my legitimate interest in this (Art. 6 (1) (f) GDPR). GitHub is based in the USA. According to its privacy statement, GitHub bases transfers from the European Economic Area on the standard contractual clauses of the European Commission (Art. 46 (2) (c) GDPR).</p>

    <h2>No cookies, no statistics</h2>
    <p>There are no cookies, no visitor counting, no advertising and no analytics services. This website stores up to two items in your browser that never leave your device and are not evaluated: in session storage a marker “sm-intro”, so that the short start view runs only once per visit, and in local storage an entry “sm-theme”, if you switch the appearance to light or dark. The embedded pieces of work each set one further session marker. All items with purpose and duration are listed on the page <a href="{P("/cookies/")}">Cookies and storage</a>. That is why no cookie banner is needed (§ 165 (3) of the Austrian Telecommunications Act 2021).</p>
    <p>The start view reads from your browser which files of this page were loaded and how large they are, and shows them. This happens only on your device. Nothing is sent to me or to third parties.</p>

    <h2>Fonts</h2>
    <p>The fonts are hosted on the same server as the website. There is no connection to Google Fonts or any other font service.</p>

    <h2>Enquiry form</h2>
    {form}

    <h2>Email and phone</h2>
    <p>When you write to me or call me, I process your email address, your message and, if applicable, your phone number in order to reply (Art. 6 (1) (b) or (f) GDPR). My emails are held by my email provider.</p>

    <h2>How long I keep data</h2>
    <p>If no contract is concluded, I delete your enquiry no later than six months after the last message, including at Formspree. If a contract is concluded, I keep the documents for as long as the law requires (currently seven years, § 132 of the Austrian Federal Fiscal Code) and delete them afterwards.</p>

    <h2>Disclosure, automated decisions</h2>
    <p>I pass on your data only if that is necessary for your enquiry (Formspree, my email provider) or required by law. There is no automated decision-making and no profiling.</p>

    <h2>Embedded work and links</h2>
    <p>The pieces of work under “Work” run in the same window and are hosted on the same server. The forms of the work send nothing: the demos only show a demo message, and the form in the copy of nickmonu.com points to the original site. Links to nickmonu.com and other sites are ordinary links. You leave this website only when you click one; the privacy policy of the respective provider applies there.</p>

    <h2>Your rights</h2>
    <p>You have the right to access, rectification, erasure, restriction of processing, data portability and objection, in particular to processing based on legitimate interests (Art. 21 GDPR). You can withdraw any consent you have given at any time. An email to <a href="mailto:{MAIL}">{MAIL}</a> is enough.</p>
    <p>You can also lodge a complaint with the Austrian Data Protection Authority: Barichgasse 40–42, 1030 Vienna, <a href="https://www.dsb.gv.at" rel="noopener" target="_blank">dsb.gv.at</a>.</p>'''
    return ("/en/privacy/", "Privacy policy",
            "Privacy policy of simonmonu.at: no cookies, no statistics, hosting on GitHub Pages, form through Formspree.",
            _rechtsseite("Privacy policy", "In short: this website sets no cookies, counts no visitors and embeds nothing from third parties. The host, GitHub, stores your IP address for technical reasons when you open a page. If you use the form, your message goes through the service Formspree.",
                         COURTESY.format(de="/datenschutz/", name="Datenschutz"), koerper, "As of: October 2026"),
            {"og": "start", "robots": "noindex, follow"})


def cookies():
    tab = '''<div class="tab-wrap" tabindex="0" role="region" aria-label="Table of browser storage"><table class="tabelle tabelle-speicher"><caption>All items that this website and its embedded work store in the browser</caption>
      <thead><tr><th scope="col">Name</th><th scope="col">Type</th><th scope="col">Purpose</th><th scope="col">Duration</th></tr></thead>
      <tbody>
      <tr><th scope="row">sm-theme</th><td>localStorage</td><td>Remembers your choice of light, dark or system when you switch the appearance.</td><td>until you set it back to “system”</td></tr>
      <tr><th scope="row">sm-intro</th><td>sessionStorage</td><td>Makes sure the short start view runs only once per visit.</td><td>until you close the tab</td></tr>
      <tr><th scope="row">nm-eintritt</th><td>sessionStorage</td><td>Only in the copy of nickmonu.com under “Work”: start view once per visit.</td><td>until you close the tab</td></tr>
      <tr><th scope="row">vl-intro</th><td>sessionStorage</td><td>Only in the Vera Lindtner demo: start view once per visit.</td><td>until you close the tab</td></tr>
      </tbody></table></div>'''
    koerper = f'''
    <h2>Cookies</h2>
    <p>This website sets no cookies. There are also no third-party services that would set cookies: no statistics, no advertising, no maps, no embedded videos, no external fonts.</p>

    <h2>Browser storage</h2>
    <p>At most, the website stores the following items in the browser. They contain no personal data, are not evaluated and never leave your device.</p>
    {tab}

    <h2>Legal basis</h2>
    <p>The items serve only to display the website you requested as intended. They are technically necessary for the service you expressly asked for or result from your own choice. That is why, under § 165 (3) of the Austrian Telecommunications Act 2021, no consent is needed and there is no cookie banner.</p>

    <h2>What you can do</h2>
    <p>You can delete or block browser storage at any time in your browser settings. The website works without it as well. The start view then runs on every page change, and your choice of light or dark is not remembered.</p>

    <h2>More on privacy</h2>
    <p>How access data at the host and details in the enquiry form are processed is set out in the <a href="{P("/datenschutz/")}">privacy policy</a>.</p>'''
    return ("/en/cookies/", "Cookies and storage",
            "Cookies and browser storage on simonmonu.at: no cookies, at most four browser items, no cookie banner needed.",
            _rechtsseite("Cookies and storage", "This website sets no cookies. That is why there is no cookie banner here. This page shows what is stored in the browser, what for and for how long.",
                         COURTESY.format(de="/cookies/", name="Cookies und Speicher"), koerper, "As of: October 2026"),
            {"og": "start", "robots": "noindex, follow"})


def agb():
    koerper = f'''
    <h2>1. Scope</h2>
    <p>These terms apply to all contracts for web design, programming, hosting and maintenance between Simon Monu, {_anschrift_zeile()} (“I”), and you as the client (“you”). A written offer or contract takes precedence over these terms. Your own terms apply only if I confirm them in writing.</p>
    <p>Consumers are persons who conclude the contract predominantly outside their commercial or professional activity (§ 1 of the Austrian Consumer Protection Act). Mandatory consumer rights always apply to them, even where these terms would say otherwise. For the right of withdrawal see <a href="{P("/widerruf/")}">Right of withdrawal</a>.</p>

    <h2>2. Offer and conclusion of contract</h2>
    <p>The packages and prices on my website and in my price list are guide prices (“from” prices). Only my written offer with a fixed price, scope, delivery time and payment plan is binding. It is valid for 14 days from its date unless it states otherwise. The contract is concluded when you accept the offer in writing. An email is enough.</p>

    <h2>3. Services and process</h2>
    <p>The scope is set out in the offer and in the package description. The process: intro call (free), concept for approval, implementation, handover. I do not build further without your approval of the concept. I decide myself which tools and working methods I use.</p>
    <p>New content after approval of the concept, for example an additional subpage or a new section, is not a correction. You will receive a separate offer for it.</p>

    <h2>4. Your cooperation and your content</h2>
    <p>You supply texts, photos, logo and details completely and on time, and you approve the concept and the finished site. If this is delayed, the delivery time moves accordingly.</p>
    <p>You assure me that you hold the necessary rights in the content you supply and that it does not infringe third-party rights, for example in photos, texts, trademarks or images of persons. Business clients indemnify me against third-party claims.</p>
    <p>I do not give legal advice. You are responsible for the legal notice, privacy policy and other mandatory texts of your website. I build them in according to your details and point out gaps I notice. For a review I recommend legal advice or your professional association.</p>

    <h2>5. Delivery time</h2>
    <p>Details marked “approx.” are not binding. A binding date applies only if I confirm it in writing. The delivery time starts when the first payment and all necessary documents are with me. Force majeure and failures of third parties extend it by the duration of the disruption.</p>

    <h2>6. Rounds of corrections</h2>
    <p>The package price includes 2 rounds of corrections for the One-pager, 3 for the Business website, 4 for Premium and 3 for the Shop. A round is one collected list of change requests that you send at once. Requests beyond that you receive as a written offer with a fixed price; I do not bill by the hour. Errors on my side, for example broken links, display or function errors or deviations from approved texts, I always fix free of charge. They never count as a round.</p>

    <h2>7. Prices and payment</h2>
    <p>All prices are final prices. As a small business (§ 6 (1) no. 27 of the Austrian VAT Act) I do not charge VAT. Payment plan: One-pager and Business website 50 % on order and 50 % on completion; Premium and Shop 40 % at start, 30 % after approval of the concept and 30 % on completion. Invoices are payable within 14 days. In case of default, statutory default interest applies.</p>
    <p>The domain always runs in your name, never in mine. Running fees for the domain and costs of payment providers or paid third-party licences are included in the package price only if the offer says so.</p>

    <h2>8. Maintenance (hosting, updates, small changes)</h2>
    <p>Maintenance covers hosting, updates and backups, an availability check, small changes and a quarterly check. The scope of small changes per month is set in the contract; beyond that you receive an offer. The price is payable monthly, starting at handover, and is added to the package price: Business website €60, Premium and Shop €80, optional €60 for the One-pager, “Aktiv” €150. A minimum term of 3 months applies; after that you can cancel at any time by email to the end of the current month.</p>
    <p>After maintenance ends, you receive all files and access. The site can continue with a host of your choice; I help with the move on request by agreement. I strive for high availability but cannot guarantee it, especially not in case of outages at my host.</p>
    <p>If, as part of maintenance, I process personal data of your customers, for example through a contact form, we conclude a data processing agreement under Art. 28 GDPR beforehand.</p>

    <h2>9. Rights in the website</h2>
    <p>Copyright remains with me. Upon full payment you receive the right, unlimited in time, territory and content, to use, change and operate the finished website for your business. Tools, building blocks and program parts that I use for several projects remain with me; you receive the right to use them for this website. Until full payment, the rights of use remain with me and I may withhold the handover.</p>
    <p>I may show the finished website with name and link as a reference. With the introductory offer this is part of the consideration; otherwise only with your consent.</p>

    <h2>10. Warranty and liability</h2>
    <p>The statutory warranty rights apply. Business clients please report obvious defects within 14 days after handover. I am liable under the statutory provisions. Towards business clients I am not liable for slight negligence, except for personal injury. For lost profit and indirect damage I am liable towards business clients only for intent or gross negligence, and liability is limited in amount to the contract value. You are responsible for your content and its backup outside of maintenance.</p>

    <h2>11. Withdrawal before completion</h2>
    <p>If you withdraw from the contract before completion without my having given cause, you pay for the services provided up to then. I credit payments already made against this. Further statutory claims under § 1168 of the Austrian Civil Code remain unaffected. The consumer right of withdrawal is set out on the page <a href="{P("/widerruf/")}">Right of withdrawal</a>.</p>

    <h2>12. Data protection</h2>
    <p>How I process personal data is set out in the <a href="{P("/datenschutz/")}">privacy policy</a>.</p>

    <h2>13. Dispute resolution for consumers</h2>
    <p>I have not undertaken to take part in proceedings before a consumer arbitration body and am not legally obliged to do so. If we cannot settle a dispute, I will name the competent arbitration body in text form and state whether I will take part in proceedings (§ 19 (3) of the Austrian Alternative Dispute Resolution Act). The EU online dispute resolution platform was discontinued on 20 July 2025.</p>

    <h2>14. Final provisions</h2>
    <p>Austrian law applies, excluding its conflict-of-law rules and the UN Convention on Contracts for the International Sale of Goods. For consumers, mandatory consumer protection provisions of the state in which they habitually reside remain unaffected. For business clients the court with subject-matter jurisdiction for my registered office has jurisdiction; for consumers the statutory venue applies. Amendments and additions require written form; an email is enough. If a provision is invalid, the rest remains valid. The version that was on this page when the order was placed applies.</p>'''
    return ("/en/terms/", "Terms and conditions",
            "Terms and conditions for web design by Simon Monu: offer, process, rounds of corrections, payment, maintenance, rights, liability.",
            _rechtsseite("Terms and conditions", "For web design, programming, hosting and maintenance by Simon Monu. A written offer takes precedence over these terms. For consumers the right of withdrawal applies in addition.",
                         COURTESY.format(de="/agb/", name="AGB"), koerper, "As of: October 2026"),
            {"og": "start", "robots": "noindex, follow"})


def widerruf():
    koerper = f'''
    <h2>Who does this apply to?</h2>
    <p>This right of withdrawal exists only for consumers, that is, persons who conclude the contract predominantly outside their commercial or professional activity (§ 1 of the Austrian Consumer Protection Act). Business clients do not have it.</p>

    <h2>Withdrawal information</h2>
    <p><strong>Right of withdrawal.</strong> You have the right to withdraw from this contract within 14 days without giving any reason. The withdrawal period is 14 days from the day of conclusion of the contract.</p>
    <p>To exercise your right of withdrawal, you must inform me, Simon Monu, {_anschrift_zeile()}, email <a href="mailto:{MAIL}">{MAIL}</a>, of your decision to withdraw from this contract by an unequivocal statement (for example a letter sent by post or an email). You may use the attached model withdrawal form, but it is not obligatory. To meet the withdrawal deadline, it is sufficient for you to send your communication concerning your exercise of the right of withdrawal before the withdrawal period has expired.</p>
    <p><strong>Effects of withdrawal.</strong> If you withdraw from this contract, I shall reimburse to you all payments received from you without undue delay and in any event not later than 14 days from the day on which I am informed about your decision to withdraw. I shall carry out such reimbursement using the same means of payment as you used for the initial transaction, unless you have expressly agreed otherwise. In any event, you will not incur any fees as a result of such reimbursement.</p>
    <p>If you requested that the service begin during the withdrawal period, you shall pay me an amount which is in proportion to what has been provided until you have informed me of your withdrawal, in comparison with the full coverage of the contract.</p>
    <p><strong>Early expiry.</strong> For a service contract, the right of withdrawal expires once I have fully performed the service, provided that performance began only after you had given your express consent and at the same time acknowledged that you lose your right of withdrawal once I have fully performed the contract.</p>

    <h2>If you want me to start earlier</h2>
    <p>I start before the withdrawal period has expired only if you expressly request it. To do so, you confirm the following sentence when accepting the offer. Without this express consent I start only after the withdrawal period has expired:</p>
    <blockquote class="zitat-satz"><p>“I expressly request that Simon Monu begin the service before the withdrawal period has expired. I am aware that I lose my right of withdrawal once Simon Monu has fully performed the contract.”</p></blockquote>

    <h2>Model withdrawal form</h2>
    <p>If you want to withdraw from the contract, you can fill in this form and send it back to me.</p>
    <ul>
      <li>To Simon Monu, {_anschrift_zeile()}, email: <a href="mailto:{MAIL}">{MAIL}</a>:</li>
      <li>I/We (*) hereby give notice that I/We (*) withdraw from my/our (*) contract for the provision of the following service (*):</li>
      <li>Ordered on (*) / received on (*):</li>
      <li>Name of consumer(s):</li>
      <li>Address of consumer(s):</li>
      <li>Signature of consumer(s) (only if this form is notified on paper):</li>
      <li>Date:</li>
    </ul>
    <p class="klein">(*) Delete as appropriate.</p>

    <h2>Outside of withdrawal</h2>
    <p>For defects, the statutory warranty rights apply; I fix errors on my side free of charge. For a withdrawal without a right of withdrawal, section 11 of the <a href="{P("/agb/")}">Terms and conditions</a> applies.</p>'''
    return ("/en/withdrawal/", "Right of withdrawal",
            "Withdrawal information and model withdrawal form for consumers: 14-day right of withdrawal for contracts with Simon Monu.",
            _rechtsseite("Right of withdrawal", "For consumers: you can withdraw from a contract with me within 14 days without giving any reason. Business clients do not have this right.",
                         COURTESY.format(de="/widerruf/", name="Widerrufsrecht"), koerper, "As of: October 2026"),
            {"og": "start", "robots": "noindex, follow"})


# ------------------------------------------------------------------------------
# ARBEITEN (Übersicht und drei Cases)
# ------------------------------------------------------------------------------

def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def kontrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return f"{(la + 0.05) / (lb + 0.05):.1f} : 1"


def farbreihe(farben):
    """farben: [(name, hex, text_hex_oder_None, zweck)]. Kontrast gegen den zweiten Wert."""
    z = ""
    for name, hx, geg, zweck in farben:
        kt = f'<span class="mono">{kontrast(hx, geg)} against {geg.upper()}</span>' if geg else ""
        z += (f'<li class="farbe"><span class="farbe-feld f-{hx[1:].upper()}"></span>'
              f'<span class="farbe-text"><strong>{e(name)}</strong> <span class="mono">{hx.upper()}</span> {kt}<br>{e(zweck)}</span></li>')
    return f'<ul class="farbreihe">{z}</ul>'


def case_kopf(titel, marke, sub, id, links):
    """Kopf einer Case-Seite. Darunter läuft die Arbeit live."""
    ein = schaufenster_eintraege([id])
    for x in ein:
        x["case"] = None   # auf der Case-Seite selbst kein Link auf sich selbst
    live = (f'<section class="sek sek-case-bild" aria-label="Live view"><div class="wrap">{fenster(ein)}</div></section>' if ein else "")
    return f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <p class="kicker"><span class="marke{" marke-demo" if "demo" in marke.lower() else ""}">{marke}</span></p>
  <h1 id="h1" class="t-xl">{titel}</h1>
  <p class="lead">{sub}</p>
  <p class="knoepfe">{links}</p>
</div></section>
{live}'''


def case_ende(weiter_titel, weiter_href):
    return f'''<section class="sek sek-schluss" aria-labelledby="h-schluss"><div class="wrap">
  <h2 id="h-schluss" class="t-l">Does an approach like this fit your project?</h2>
  <p class="knoepfe">{knopf("Book an intro call", "/kontakt/")} {textlink(weiter_titel, weiter_href)}</p>
</div></section>'''


def arbeiten():
    n, h, l = ARBEITEN
    hand = [
        ("nickmonu.com", "#0B0A09", "Libre Caslon Display, Instrument Sans", "Brass #BBA883 on black", "Stage, calm, a portrait"),
        ("Tischlerei Hallwirth", "#F5F1F1", "Barlow Condensed, Barlow", "Iron red #943A2C on paper", "Working drawing, dimensions, craft"),
        ("Vera Lindtner Coaching", "#F5F4F0", "Spectral, Hanken Grotesk", "Deep green #1A2E26, orange #E8914A", "Warm, calm, one button"),
        ("simonmonu.at", "#F4F4F1", "Schibsted Grotesk", "Night blue #0C1A33 as stage, cobalt #2D55E8", "Paper, stage, dimensioning"),
    ]
    zeilen = "".join(f'<tr><th scope="row">{e(a)}</th><td><span class="farbe-feld farbe-klein f-{b[1:].upper()}"></span><span class="mono">{b}</span></td><td>{e(c)}</td><td>{e(d)}</td><td>{e(f)}</td></tr>'
                     for a, b, c, d, f in hand)
    live = f'''<div class="werke-live">
    <h2 id="h-live" class="t-l">Try it live</h2>
    <p class="lead">All three sites run here in the window and can be used. Pick one and click into it. The two demos are in German.</p>
    {fenster(schaufenster_eintraege(), "h-live")}
  </div>'''
    arb = werke(werke_liste(), "h-liste",
                '''<h2 id="h-liste" class="t-l">Three projects, three distinct styles.</h2>
    <p class="lead">nickmonu.com is a real project. The joinery and the coaching practice are concept demos with invented businesses, and the sites say so.</p>''', live)
    inhalt = f'''<section class="sek sek-kopfseite" aria-labelledby="h1"><div class="wrap">
  <h1 id="h1" class="t-xl"><span class="h1-dach">Web design portfolio</span>Websites nobody mistakes for a template.</h1>
  <p class="lead">One real project and two concept demos. Each site has its own typeface, colour and motion, because each has a different job.</p>
</div></section>
<section class="sek sek-werke" aria-labelledby="h-liste">{arb}</section>
<section class="sek sek-hand" aria-labelledby="h-hand"><div class="wrap">
  <h2 id="h-hand" class="t-l">Four distinct styles</h2>
  <p class="lead">Four sites, four jobs, four looks. My proof that I do not build from a template.</p>
  <div class="tab-wrap" tabindex="0" role="region" aria-label="Base colour, typefaces and character of the four sites"><table class="tabelle"><caption>Base colour, typefaces and character of the four sites</caption>
  <thead><tr><th scope="col">Site</th><th scope="col">Ground</th><th scope="col">Typefaces</th><th scope="col">Colour</th><th scope="col">Tone</th></tr></thead>
  <tbody>{zeilen}</tbody></table></div>
</div></section>
{case_ende("Services and pricing", "/leistungen/")}'''
    return ("/en/work/", "Web design portfolio and work",
            "Web design portfolio: one real project (nickmonu.com) and two concept demos for a trades business and for coaching, each with starting point and decisions.",
            inhalt, {"og": "arbeiten"})


def case_nickmonu():
    m = MESSWERTE
    kopf = case_kopf("nickmonu.com", "Real project",
                     "Website of actor, director and acting coach Nicholas Monu, Salzburg and Vienna. 14 pages, German and English, live since " + LIVE_SEIT + ".",
                     "nickmonu",
                     knopf("Open nickmonu.com", "https://nickmonu.com", "knopf-2", extern=True))
    a = abschnitt(1, "Starting point", "<p>Nicholas Monu works as an actor, director and acting coach. His website has three jobs: show who he is, show what he offers, and make enquiries possible. Two languages, because his clients are a mix of Salzburg and Vienna.</p>", "h-a")
    b = abschnitt(2, "Decision", "<p>A dark ground with brass as the only accent colour, a serif for the presence, a grotesque for everything that is read and clicked. The reasoning: the site should look like a stage and still stay fast and calm.</p>", "h-b")
    fr = farbreihe([("Ground", "#0B0A09", "#EFE9DF", "Page ground, light text on it"), ("Brass", "#BBA883", "#0B0A09", "Accent for lines and emphasis")])
    c = abschnitt(3, "Build", f'''<p>The colours come from the material of the site and have been checked for contrast:</p>{fr}
{spez_tabelle([("Typefaces", "Libre Caslon Display and Libre Caslon Text, Instrument Sans. All self-hosted."), ("Languages", "German and English, every page in both versions."), ("Structure", "14 pages, generated statically, no site builder."), ("Privacy", "No cookies, no tracking.")])}''', "h-c")
    d = abschnitt(4, f"Rebuild: version 25 → {FASSUNG}", f'''<p>After launch, several people gave the same feedback: the look is convincing, but the important information is not where you would look for it, especially on mobile. So I rebuilt the home page.</p>
<div class="vorher-nachher"><figure>{bild("nickmonu-25-m", "nickmonu.com version 25 on mobile, top section.", "(min-width: 1024px) 280px, 45vw")}<figcaption>Version 25</figcaption></figure><figure>{bild("nickmonu-26-m", f"nickmonu.com version {FASSUNG} on mobile, top section.", "(min-width: 1024px) 280px, 45vw")}<figcaption>Version {FASSUNG}</figcaption></figure></div>''', "h-d")
    f = abschnitt(5, "Result", f'''<dl class="werte werte-breit"><div><dt>Main content visible, desktop</dt><dd>{m["lcp_d"]}</dd></div><div><dt>Layout shift (CLS)</dt><dd>{m["cls"]}</dd></div><div><dt>Blocking time (TBT)</dt><dd>{m["tbt"]}</dd></div></dl>
<p class="klein">Measured with {m["quelle"]}, {m["stand"]}. The site is live and can be measured by anyone at any time.</p>''', "h-f")
    g = abschnitt(6, "Limits", "<p>It is my first project, and it belongs to my family. So what you see here is not client work under market conditions, but what I can achieve without a client's pressure, and how I deal with feedback. I do not yet have a testimonial from an outside client, and I will not invent one.</p>", "h-g")
    ld = [{"@context": "https://schema.org", "@type": "CreativeWork", "name": "nickmonu.com", "creator": {"@type": "Person", "name": NAME},
           "url": "https://nickmonu.com"}]
    return ("/en/work/nickmonu/", "nickmonu.com: case study", "How nickmonu.com came about: starting point, decisions, the rebuild from version 25 to 26 and measured results.",
            "\n".join([kopf, a, b, c, d, f, g, case_ende("To the concept demos", "/arbeiten/hallwirth/")]), {"og": "arbeiten", "jsonld": ld})


def case_hallwirth():
    kopf = case_kopf("Tischlerei Hallwirth", "Concept demo",
                     "An invented joinery in Vienna-Liesing, built as a Business website. Shows how I think about a trades business. Business, team and jobs are not real. The demo is in German.",
                     "hallwirth",
                     knopf("Open demo", "/demos/hallwirth/", "knopf-2", extern=True))
    a = abschnitt(1, "Starting point", "<p>Anyone looking for a joiner searches on their phone and wants to know: does he do what I need, roughly what does it cost, and how do I reach him? Most trades sites answer that only after several clicks.</p>", "h-a")
    b = abschnitt(2, "Decision", "<p>The site takes its vocabulary from the workshop: working drawing, dimensions, graphite on light paper, a single iron red. Phone number and guide prices are where you look first.</p>", "h-b")
    fr = farbreihe([("Paper", "#F5F1F1", "#272120", "Ground, text in graphite"), ("Iron red", "#943A2C", "#F5F1F1", "Accent for emphasis")])
    c = abschnitt(3, "Build", f'''{fr}{spez_tabelle([("Typefaces", "Barlow Condensed and Barlow, self-hosted."), ("Special feature", "The home page measures the browser window and fits the photo into it."), ("Prices", "Guide prices are shown for every service."), ("Labelling", "At the top of every page of the demo it says that the business does not exist.")])}''', "h-c")
    g = abschnitt(4, "Limits", "<p>It is a demo. There is no business, no real photos and no real prices. On a real job the material would come from the business: photos of the workshop and the work, the actual services and prices, a phone that somebody picks up.</p>", "h-g")
    return ("/en/work/hallwirth/", "Tischlerei Hallwirth: concept demo", "Concept demo for a trades business: working drawing, phone number and guide prices visible at once. Business invented.",
            "\n".join([kopf, a, b, c, g, case_ende("Vera Lindtner Coaching", "/arbeiten/lindtner/")]), {"og": "arbeiten"})


def case_lindtner():
    kopf = case_kopf("Vera Lindtner Coaching", "Concept demo",
                     "An invented coaching practice in Vienna-Neubau, built as a one-pager. Shows how I think about freelancers. Person and offers are not real. The demo is in German.",
                     "lindtner",
                     knopf("Open demo", "/demos/lindtner/", "knopf-2", extern=True))
    a = abschnitt(1, "Starting point", "<p>Coaching lives on people trusting the person before they know them. The site has to be calm, say what it costs and offer a single next step.</p>", "h-a")
    b = abschnitt(2, "Decision", "<p>A warm light ground, deep green for seriousness and an orange as the only warmth. Three offers with prices including VAT, one button to get to know each other.</p>", "h-b")
    fr = farbreihe([("Ground", "#F5F4F0", "#1A2E26", "Page ground, text in deep green"), ("Deep green", "#1A2E26", "#F5F4F0", "Surfaces and text"), ("Orange", "#E8914A", "#1A2E26", "Accent, only for the button and emphasis")])
    c = abschnitt(3, "Build", f'''{fr}{spez_tabelle([("Typefaces", "Spectral and Hanken Grotesk, self-hosted."), ("Structure", "A one-pager with several sections."), ("Labelling", "In the footer of the demo and next to the client quotes it says that person and quotes are invented.")])}''', "h-c")
    g = abschnitt(4, "Limits", "<p>It is a demo. Person, offers and prices are invented. On a real job it would be your voice, your photos and your prices, and I would ask you for real client quotes instead of inventing any.</p>", "h-g")
    return ("/en/work/lindtner/", "Vera Lindtner Coaching: concept demo", "Concept demo for a coaching practice: a calm one-pager with three offers and one button. Person invented.",
            "\n".join([kopf, a, b, c, g, case_ende("All work", "/arbeiten/")]), {"og": "arbeiten"})


def alle():
    return [startseite(), leistungen(), handwerk(), ueber_mich(), kontakt(), danke(), impressum(), datenschutz(),
            cookies(), agb(), widerruf(), arbeiten(), case_nickmonu(), case_hallwirth(), case_lindtner()]
