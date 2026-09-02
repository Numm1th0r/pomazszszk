/* Szociális Szolgáltatási Központ Pomáz — akadálymentesítés és navigáció */
(function () {
  "use strict";

  var root = document.documentElement;
  var STORE = "szszk-prefs";

  /* --- Beállítások megőrzése (biztonságosan, ha a tároló nem elérhető) --- */
  function readPrefs() {
    try { return JSON.parse(localStorage.getItem(STORE)) || {}; }
    catch (e) { return {}; }
  }
  function writePrefs(p) {
    try { localStorage.setItem(STORE, JSON.stringify(p)); } catch (e) {}
  }

  var prefs = readPrefs();

  function apply(prefs) {
    if (prefs.textsize && prefs.textsize !== "m") root.setAttribute("data-textsize", prefs.textsize);
    else root.removeAttribute("data-textsize");

    if (prefs.contrast === "high") root.setAttribute("data-contrast", "high");
    else root.removeAttribute("data-contrast");

    syncButtons();
  }

  function syncButtons() {
    var size = prefs.textsize || "m";
    document.querySelectorAll("[data-textsize-btn]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.textsizeBtn === size));
    });
    document.querySelectorAll("[data-contrast-btn]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(prefs.contrast === "high"));
    });
  }

  document.addEventListener("click", function (e) {
    var sizeBtn = e.target.closest("[data-textsize-btn]");
    if (sizeBtn) {
      prefs.textsize = sizeBtn.dataset.textsizeBtn;
      writePrefs(prefs); apply(prefs); return;
    }
    var contrastBtn = e.target.closest("[data-contrast-btn]");
    if (contrastBtn) {
      prefs.contrast = prefs.contrast === "high" ? "normal" : "high";
      writePrefs(prefs); apply(prefs); return;
    }
  });

  apply(prefs);

  /* --- Mobil menü ------------------------------------------------------- */
  var nav = document.getElementById("fomenu");
  var toggle = document.querySelector("[data-nav-toggle]");
  var scrim = document.querySelector("[data-nav-scrim]");

  function setNav(open) {
    if (!nav) return;
    nav.dataset.open = String(open);
    if (scrim) scrim.dataset.open = String(open);
    if (toggle) toggle.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open && window.innerWidth <= 1000 ? "hidden" : "";
    if (open) {
      var first = nav.querySelector("a, button");
      if (first) first.focus();
    }
  }

  if (toggle) toggle.addEventListener("click", function () { setNav(nav.dataset.open !== "true"); });
  if (scrim) scrim.addEventListener("click", function () { setNav(false); });
  document.querySelectorAll("[data-nav-close]").forEach(function (b) {
    b.addEventListener("click", function () { setNav(false); if (toggle) toggle.focus(); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && nav && nav.dataset.open === "true") { setNav(false); if (toggle) toggle.focus(); }
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 1000) { document.body.style.overflow = ""; }
  });
})();
