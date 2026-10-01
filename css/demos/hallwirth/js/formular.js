/* ==========================================================================
   ANFRAGEFORMULAR
   - Prüft Pflichtfelder beim Verlassen und beim Absenden, Fehler stehen als
     Text unter dem Feld (nicht nur rot), der Fokus springt zum ersten Fehler.
   - ?art=kuechen in der Adresse wählt „Worum geht es?“ vor (von der
     Leistungsseite aus).
   - data-endpoint leer = Demo: nichts wird gesendet, das steht auch so da.
     Mit Endpoint (z. B. Formspree) wird per fetch gesendet, bei Fehler gibt
     es den Weg per Telefon und E-Mail.
   ========================================================================== */
(function () {
  "use strict";
  var form = document.getElementById("formular");
  if (!form) return;
  var status = document.getElementById("formular-status");
  var senden = form.querySelector("[data-senden]");
  var endpoint = form.getAttribute("data-endpoint") || "";
  var demo = form.getAttribute("data-demo") === "1";
  if (senden) senden.hidden = false;

  var art = form.querySelector("#f-art");
  var param = new URLSearchParams(window.location.search).get("art");
  if (param && art && art.querySelector('option[value="' + CSS.escape(param) + '"]')) art.value = param;

  var TEXTE = {
    name: { leer: "Bitte geben Sie Ihren Namen an." },
    email: { leer: "Bitte geben Sie Ihre E-Mail-Adresse an, damit wir antworten können.",
             falsch: "Diese E-Mail-Adresse sieht unvollständig aus, zum Beispiel: name@beispiel.at" },
    telefon: { falsch: "Bitte nur Ziffern, Leerzeichen und + / ( ) - verwenden." },
    projektart: { leer: "Bitte wählen Sie, worum es geht." },
    nachricht: { leer: "Ein, zwei Sätze reichen: Was soll wohin?", kurz: "Etwas mehr bitte, ein, zwei Sätze reichen: Was soll wohin?" }
  };

  function fehlerText(feld) {
    var wert = (feld.value || "").trim();
    var t = TEXTE[feld.name];
    if (!t) return "";
    if (feld.required && !wert) return t.leer;
    if (feld.name === "email" && wert && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(wert)) return t.falsch;
    if (feld.name === "telefon" && wert && !/^[0-9+\/()\-\s]{6,}$/.test(wert)) return t.falsch;
    if (feld.name === "nachricht" && wert && wert.length < 10) return t.kurz;
    return "";
  }
  function zeige(feld, text) {
    var ziel = document.getElementById(feld.id + "-fehler");
    if (ziel) ziel.textContent = text;
    if (text) feld.setAttribute("aria-invalid", "true");
    else feld.removeAttribute("aria-invalid");
  }
  var felder = Array.prototype.slice.call(form.querySelectorAll("input:not([name=firma]), select, textarea"));
  felder.forEach(function (feld) {
    feld.addEventListener("blur", function () {
      if ((feld.value || "").trim() || feld.getAttribute("aria-invalid")) zeige(feld, fehlerText(feld));
    });
    feld.addEventListener("input", function () {
      if (feld.getAttribute("aria-invalid")) zeige(feld, fehlerText(feld));
    });
    feld.addEventListener("change", function () {
      if (feld.getAttribute("aria-invalid")) zeige(feld, fehlerText(feld));
    });
  });

  function zeigeStatus(titel, saetze, mitZurueck) {
    status.innerHTML = "";
    var h = document.createElement("h3");
    h.textContent = titel;
    status.appendChild(h);
    saetze.forEach(function (s) {
      var p = document.createElement("p");
      if (typeof s === "string") p.textContent = s; else p.appendChild(s);
      status.appendChild(p);
    });
    if (mitZurueck) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "knopf knopf-leise"; b.textContent = "Formular wieder anzeigen";
      b.addEventListener("click", function () {
        status.hidden = true; form.hidden = false;
        var erstes = form.querySelector("#f-name"); if (erstes) erstes.focus();
      });
      status.appendChild(b);
    }
    status.hidden = false;
    status.focus({ preventScroll: true });
    status.scrollIntoView({ block: "center", behavior: "auto" });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var erster = null;
    felder.forEach(function (feld) {
      var t = fehlerText(feld);
      zeige(feld, t);
      if (t && !erster) erster = feld;
    });
    if (erster) { erster.focus(); return; }
    if (form.querySelector("[name=firma]").value) return;   // Spamfalle

    var vorname = (form.querySelector("#f-name").value.trim().split(/\s+/)[0]) || "";

    if (demo || !endpoint) {
      form.hidden = true;
      zeigeStatus("Danke" + (vorname ? ", " + vorname : "") + ".",
        ["Auf der echten Website wäre Ihre Anfrage jetzt bei der Werkstatt, und Sie hätten eine Bestätigung per E-Mail bekommen.",
         "Das hier ist eine Demo: Es wurde nichts gesendet und nichts gespeichert."], true);
      return;
    }

    var knopf = form.querySelector("button[type=submit]");
    knopf.disabled = true;
    fetch(endpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
      .then(function (r) {
        if (!r.ok) throw new Error("Fehlgeschlagen");
        form.hidden = true;
        zeigeStatus("Danke" + (vorname ? ", " + vorname : "") + ". Ihre Anfrage ist bei uns.",
          ["Wir melden uns innerhalb von zwei Werktagen, meistens schneller."], false);
      })
      ["catch"](function () {
        knopf.disabled = false;
        var tel = document.querySelector(".kontakt-tel a");
        var p = document.createElement("span");
        p.textContent = "Das Senden hat nicht geklappt. Ihre Eingaben sind noch da. Rufen Sie uns bitte an" + (tel ? " unter " + tel.textContent : "") + " oder schreiben Sie direkt eine E-Mail.";
        zeigeStatus("Nicht gesendet", [p], false);
        form.hidden = false;
      });
  });
})();
