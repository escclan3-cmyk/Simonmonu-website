/* ==========================================================================
   ANFRAGEFORMULAR
   Portiert aus AnfrageFormular.tsx (Framer). Kein React.

   Das Formular steht auf allen drei Unterseiten und zeigt je nach
   Buchungsart andere Felder. Sprache und Vorauswahl kommen aus
   data-Attributen am <form>-Element.

   FORMSPREE: den Endpoint unten bei ENDPOINT eintragen.
   Solange er leer ist, öffnet der Knopf eine vorausgefüllte Mail an
   nick@nickmonu.com — Anfragen gehen also nie verloren.
   ========================================================================== */

(function () {
  "use strict";

  // ---- FORMSPREE-ENDPOINT --------------------------------------------
  var ENDPOINT = "";
  // -----------------------------------------------------------------------

  var EMPFAENGER = "nick@nickmonu.com";

  var T = {
    de: {
      art: "Worum geht es?",
      coaching: "Acting Coaching", regie: "Regie", schauspiel: "Schauspiel-Engagement",
      name: "Name", mail: "E-Mail", tel: "Telefon (optional)",
      sprache: "In welcher Sprache soll gearbeitet werden?",
      spracheOpts: ["Deutsch", "Englisch", "Beides", "Andere"],
      ort: "Ort oder Haus (optional)",
      zeitraum: "Zeitraum", zeitraumHint: "z. B. Februar bis April 2027",
      nachricht: "Nachricht (optional)",
      werBucht: "Wer bucht?",
      werBuchtOpts: ["Ich selbst", "Agentur", "Produktion für mehrere Schauspieler"],
      erfahrung: "Wo stehen Sie gerade?",
      erfahrungOpts: ["In Ausbildung", "Erste Engagements", "Seit Jahren im Beruf"],
      anlass: "Anlass",
      anlassOpts: ["Konkrete Rolle", "Casting oder Vorsprechen", "Allgemeine Weiterbildung", "Kurzfristig, E-Casting"],
      format: "Gewünschtes Format",
      formatOpts: ["Einzelcoaching", "Acting I", "Acting II", "Acting III", "Produktionscoaching", "Weiß ich noch nicht"],
      teilnehmer: "Wie viele Teilnehmer",
      haus: "Haus oder Firma",
      produktionsart: "Art der Produktion",
      produktionsartOpts: ["Theater", "Film", "Fernsehen", "Anderes"],
      stoff: "Stoff oder Stück",
      budget: "Budgetrahmen vorhanden?", budgetOpts: ["Ja", "Noch nicht"],
      produktion: "Produktion",
      medium: "Medium", mediumOpts: ["Film", "Fernsehen", "Theater", "Sprachaufnahme"],
      rolle: "Rolle",
      agentur: "Agentur bereits kontaktiert?", agenturOpts: ["Ja", "Nein"],
      teil1: "Worum es geht", teil2: "Zeitraum und Rahmen", teil3: "Kontakt",
      pflicht: "* Pflichtfeld",
      dsgvo: "Ich habe die Datenschutzerklärung gelesen.",
      dsgvoLink: "datenschutz.html",
      senden: "Anfrage senden", sendet: "Wird gesendet …", art2: "Art der Anfrage",
      dankeTitel: "Ihre Anfrage ist bei mir.",
      dankeText: "Ich melde mich innerhalb von drei Werktagen.",
      fehler: "Das hat nicht geklappt. Schreiben Sie mir bitte direkt an"
    },
    en: {
      art: "What is this about?",
      coaching: "Acting coaching", regie: "Directing", schauspiel: "Acting engagement",
      name: "Name", mail: "Email", tel: "Phone (optional)",
      sprache: "Which language should we work in?",
      spracheOpts: ["German", "English", "Both", "Other"],
      ort: "Place or venue (optional)",
      zeitraum: "Timeframe", zeitraumHint: "e.g. February to April 2027",
      nachricht: "Message (optional)",
      werBucht: "Who is booking?",
      werBuchtOpts: ["Myself", "Agency", "Production, several actors"],
      erfahrung: "Where are you right now?",
      erfahrungOpts: ["In training", "First engagements", "Working professionally for years"],
      anlass: "Occasion",
      anlassOpts: ["A specific role", "Casting or audition", "General training", "Short notice, self-tape"],
      format: "Preferred format",
      formatOpts: ["One-to-one coaching", "Acting I", "Acting II", "Acting III", "Production coaching", "Not sure yet"],
      teilnehmer: "Number of participants",
      haus: "Venue or company",
      produktionsart: "Type of production",
      produktionsartOpts: ["Theatre", "Film", "Television", "Other"],
      stoff: "Play or material",
      budget: "Budget in place?", budgetOpts: ["Yes", "Not yet"],
      produktion: "Production",
      medium: "Medium", mediumOpts: ["Film", "Television", "Theatre", "Voice work"],
      rolle: "Role",
      agentur: "Agency already contacted?", agenturOpts: ["Yes", "No"],
      teil1: "What it is about", teil2: "Timing and setting", teil3: "Contact",
      pflicht: "* Required",
      dsgvo: "I have read the privacy policy.",
      dsgvoLink: "privacy.html",
      senden: "Send enquiry", sendet: "Sending …", art2: "Type of enquiry",
      dankeTitel: "Your enquiry has reached me.",
      dankeText: "I will reply within three working days.",
      fehler: "That did not work. Please write to me directly at"
    }
  };

  function el(tag, attrs, kinder) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "class") n.className = attrs[k];
      else if (k === "text") n.textContent = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (kinder || []).forEach(function (c) { n.appendChild(c); });
    return n;
  }

  function eingabe(name, label, pflicht, typ, hint, autocomplete) {
    var id = "nm-" + name;
    var feld = el("div", { class: "feld" });
    feld.appendChild(el("label", { for: id, text: label + (pflicht ? " *" : "") }));
    var i = el("input", { id: id, name: name, type: typ || "text" });
    if (pflicht) i.required = true;
    if (hint) i.placeholder = hint;
    if (autocomplete) i.autocomplete = autocomplete;
    feld.appendChild(i);
    return feld;
  }

  function auswahl(name, label, opts, sprache) {
    var id = "nm-" + name;
    var feld = el("div", { class: "feld" });
    feld.appendChild(el("label", { for: id, text: label }));
    var s = el("select", { id: id, name: name });
    var leer = el("option", { value: "", text: sprache === "en" ? "Please choose" : "Bitte wählen" });
    leer.disabled = true; leer.selected = true;
    s.appendChild(leer);
    opts.forEach(function (o) { s.appendChild(el("option", { value: o, text: o })); });
    feld.appendChild(s);
    return feld;
  }

  document.querySelectorAll("form[data-anfrage]").forEach(function (form) {
    var sprache = form.getAttribute("data-sprache") === "en" ? "en" : "de";
    var t = T[sprache];
    var art = form.getAttribute("data-vorauswahl") || "coaching";
    var artLabels = { coaching: t.coaching, regie: t.regie, schauspiel: t.schauspiel };

    function teil(nr, titel) {
      var f = el("fieldset", { class: "form-teil" });
      var lg = el("legend", { class: "form-teil-titel" });
      lg.appendChild(el("span", { class: "nr", text: nr }));
      lg.appendChild(document.createTextNode(titel));
      f.appendChild(lg);
      return f;
    }

    // --- 1 Worum es geht: Buchungsart und wechselnder Teil -----------------
    var teil1 = teil("1", t.teil1);
    var fs = el("fieldset", { class: "art form-teil" });
    fs.appendChild(el("legend", { class: "feld-beschriftung", text: t.art2 + " *" }));
    var reihe = el("div", { class: "art-reihe" });
    ["coaching", "regie", "schauspiel"].forEach(function (opt) {
      var lab = el("label", { class: "art-wahl" });
      var r = el("input", { type: "radio", name: "art", value: artLabels[opt] });
      if (opt === art) r.checked = true;
      r.addEventListener("change", function () { art = opt; zeichneZweig(); });
      lab.appendChild(r);
      lab.appendChild(document.createTextNode(artLabels[opt]));
      reihe.appendChild(lab);
    });
    fs.appendChild(reihe);
    teil1.appendChild(fs);

    var zweig = el("div", { class: "feld-gruppe" });
    teil1.appendChild(zweig);

    function zeichneZweig() {
      zweig.innerHTML = "";
      if (art === "coaching") {
        zweig.appendChild(auswahl("wer_bucht", t.werBucht, t.werBuchtOpts, sprache));
        zweig.appendChild(auswahl("stand", t.erfahrung, t.erfahrungOpts, sprache));
        zweig.appendChild(auswahl("anlass", t.anlass, t.anlassOpts, sprache));
        zweig.appendChild(auswahl("format", t.format, t.formatOpts, sprache));
        zweig.appendChild(eingabe("teilnehmer", t.teilnehmer, false, "number"));
      } else if (art === "regie") {
        zweig.appendChild(eingabe("haus", t.haus, false, "text", null, "organization"));
        zweig.appendChild(auswahl("produktionsart", t.produktionsart, t.produktionsartOpts, sprache));
        zweig.appendChild(eingabe("stoff", t.stoff));
        zweig.appendChild(auswahl("budget", t.budget, t.budgetOpts, sprache));
      } else {
        zweig.appendChild(eingabe("produktion", t.produktion));
        zweig.appendChild(auswahl("medium", t.medium, t.mediumOpts, sprache));
        zweig.appendChild(eingabe("rolle", t.rolle));
        zweig.appendChild(auswahl("agentur", t.agentur, t.agenturOpts, sprache));
      }
    }
    zeichneZweig();

    // --- 2 Zeitraum und Rahmen --------------------------------------------
    var teil2 = teil("2", t.teil2);
    var rahmen = el("div", { class: "feld-gruppe" });
    rahmen.appendChild(eingabe("zeitraum", t.zeitraum, true, "text", t.zeitraumHint));
    rahmen.appendChild(auswahl("arbeitssprache", t.sprache, t.spracheOpts, sprache));
    var ortFeld = eingabe("ort", t.ort);
    ortFeld.classList.add("feld-breit");
    rahmen.appendChild(ortFeld);
    var nfeld = el("div", { class: "feld feld-breit" });
    nfeld.appendChild(el("label", { for: "nm-nachricht", text: t.nachricht }));
    nfeld.appendChild(el("textarea", { id: "nm-nachricht", name: "nachricht", rows: "5" }));
    rahmen.appendChild(nfeld);
    teil2.appendChild(rahmen);

    // --- 3 Kontakt --------------------------------------------------------
    var teil3 = teil("3", t.teil3);
    var kontakt = el("div", { class: "feld-gruppe" });
    kontakt.appendChild(eingabe("name", t.name, true, "text", null, "name"));
    kontakt.appendChild(eingabe("email", t.mail, true, "email", null, "email"));
    kontakt.appendChild(eingabe("telefon", t.tel, false, "tel", null, "tel"));
    teil3.appendChild(kontakt);

    // Spamfalle
    var falle = el("input", { type: "text", name: "firma", tabindex: "-1",
      autocomplete: "off", "aria-hidden": "true", class: "falle" });

    // Zustimmung
    var zust = el("label", { class: "zustimmung" });
    var cb = el("input", { type: "checkbox", name: "datenschutz", value: "ja" });
    cb.required = true;
    zust.appendChild(cb);
    var zustText = el("span");
    zustText.appendChild(document.createTextNode(t.dsgvo.replace(/(Datenschutzerklärung|privacy policy)/, "§§§").split("§§§")[0]));
    zustText.appendChild(el("a", { href: t.dsgvoLink, text: sprache === "de" ? "Datenschutzerklärung" : "privacy policy" }));
    zustText.appendChild(document.createTextNode((t.dsgvo.split(/Datenschutzerklärung|privacy policy/)[1] || "") + " *"));
    zust.appendChild(zustText);
    teil3.appendChild(zust);

    var knopf = el("button", { type: "submit", class: "senden", text: t.senden });
    var meldung = el("p", { class: "form-fehler", role: "alert", "aria-live": "assertive" });
    meldung.hidden = true;

    form.innerHTML = "";
    form.appendChild(teil1);
    form.appendChild(teil2);
    form.appendChild(teil3);
    form.appendChild(falle);
    form.appendChild(el("input", { type: "hidden", name: "seitensprache", value: sprache }));
    form.appendChild(knopf);
    form.appendChild(el("p", { class: "klein", text: t.pflicht }));
    form.appendChild(meldung);

    // --- Knopf nur aktiv, wenn alles Pflicht ausgefüllt und Haken bei der
    // Datenschutzerklärung gesetzt ist (Checkbox ist required, siehe oben) --
    function pruefen() { knopf.disabled = !form.checkValidity(); }
    pruefen();
    form.addEventListener("input", pruefen);
    form.addEventListener("change", pruefen);

    // --- Absenden ----------------------------------------------------------
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // novalidate steht am <form>, damit wir eigene Fehlertexte zeigen
      // könnten — genutzt wird hier aber die eingebaute Prüfung: ungültige
      // oder fehlende Pflichtfelder (auch eine ungültige E-Mail-Adresse)
      // gehen so nie an Formspree.
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      // simonmonu.at: In der Kopie wird nichts gesendet.
      var hin = sprache === "en"
        ? ["Just a copy.", "This page is a copy of nickmonu.com on simonmonu.at, so your enquiry was not sent. To reach Nick, please use the original site: "]
        : ["Nur eine Kopie.", "Diese Seite ist eine Kopie von nickmonu.com auf simonmonu.at, Ihre Anfrage wurde nicht gesendet. Nick erreichen Sie \u00fcber die Originalseite: "];
      var kopie = el("div", { class: "danke", role: "status", "aria-live": "polite" }, [
        el("p", { text: hin[0] }),
        el("p", null, [document.createTextNode(hin[1]), el("a", { href: "https://nickmonu.com/", target: "_blank", rel: "noopener", text: "nickmonu.com" })])
      ]);
      form.parentNode.replaceChild(kopie, form);
      kopie.scrollIntoView({ behavior: "smooth", block: "center" });
      return;

      var data = new FormData(form);
      data.append("_subject", "Anfrage " + artLabels[art] + " — " +
        (data.get("name") || "") + " — " + (data.get("zeitraum") || ""));

      if (!ENDPOINT) {
        // Kein Formspree hinterlegt: vorausgefüllte Mail statt stillem Verlust.
        var zeilen = [];
        data.forEach(function (v, k) {
          if (k.indexOf("_") === 0 || k === "firma") return;
          if (typeof v === "string" && v.trim() !== "") zeilen.push(k + ": " + v);
        });
        window.location.href = "mailto:" + EMPFAENGER +
          "?subject=" + encodeURIComponent("Anfrage " + artLabels[art] + " — " + (data.get("name") || "")) +
          "&body=" + encodeURIComponent(zeilen.join("\n"));
        return;
      }

      knopf.disabled = true;
      knopf.setAttribute("data-sendet", "");
      knopf.textContent = t.sendet;
      meldung.hidden = true;

      fetch(ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) {
          if (!r.ok) throw new Error("Fehlgeschlagen");
          var danke = el("div", { class: "danke", role: "status", "aria-live": "polite" }, [
            el("p", { text: t.dankeTitel }),
            el("p", { text: t.dankeText })
          ]);
          form.parentNode.replaceChild(danke, form);
          danke.scrollIntoView({ behavior: "smooth", block: "center" });
        })
        ["catch"](function () {
          knopf.removeAttribute("data-sendet");
          knopf.disabled = false;
          knopf.textContent = t.senden;
          meldung.innerHTML = "";
          meldung.appendChild(document.createTextNode(t.fehler + " "));
          meldung.appendChild(el("a", { href: "mailto:" + EMPFAENGER, text: EMPFAENGER }));
          meldung.hidden = false;
        });
    });
  });
})();
