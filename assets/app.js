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

/* --- Nagyító (lightbox) a képgalériához ---------------------------------- */
(function () {
  "use strict";

  var grid = document.querySelector("[data-lightbox]");
  if (!grid) return;

  var items = Array.prototype.slice.call(grid.querySelectorAll(".album__item"));
  if (!items.length) return;

  var index = 0;
  var lastFocus = null;

  var ICON = {
    close: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    prev: '<path d="m15 18-6-6 6-6"/>',
    next: '<path d="m9 18 6-6-6-6"/>'
  };
  function svg(name) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + "</svg>";
  }
  function btn(cls, name, label) {
    return '<button type="button" class="lb__btn ' + cls + '" data-lb-' + name +
      ' aria-label="' + label + '">' + svg(name) + "</button>";
  }

  var box = document.createElement("div");
  box.className = "lb";
  box.hidden = true;
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.setAttribute("aria-label", "Képnézegető");
  box.innerHTML =
    '<div class="lb__inner">' +
      '<div class="lb__top"><span class="lb__count" data-lb-count></span>' +
        '<span class="lb__spacer"></span>' + btn("", "close", "Bezárás") + "</div>" +
      '<div class="lb__stage">' +
        '<img class="lb__img" data-lb-img alt="">' +
        btn("lb__side lb__side--prev", "prev", "Előző kép") +
        btn("lb__side lb__side--next", "next", "Következő kép") +
      "</div>" +
      '<div class="lb__bottom">' +
        '<p class="lb__caption" data-lb-caption></p>' +
        '<div class="lb__controls">' +
          btn("lb__btn--nav", "prev", "Előző kép") +
          btn("lb__btn--nav", "next", "Következő kép") +
        "</div>" +
      "</div>" +
    "</div>";
  document.body.appendChild(box);

  var img = box.querySelector("[data-lb-img]");
  var caption = box.querySelector("[data-lb-caption]");
  var counter = box.querySelector("[data-lb-count]");

  function render() {
    var item = items[index];
    var thumb = item.querySelector("img");
    img.src = item.getAttribute("href");
    img.alt = thumb ? thumb.alt : "";
    caption.textContent = item.dataset.caption || "";
    counter.textContent = (index + 1) + " / " + items.length;
    box.querySelectorAll("[data-lb-prev]").forEach(function (b) { b.disabled = items.length < 2; });
    box.querySelectorAll("[data-lb-next]").forEach(function (b) { b.disabled = items.length < 2; });
  }

  function open(i) {
    index = i;
    lastFocus = document.activeElement;
    box.hidden = false;
    document.body.style.overflow = "hidden";
    document.documentElement.classList.add("lb-open");
    render();
    box.querySelector("[data-lb-close]").focus();
  }

  function close() {
    box.hidden = true;
    document.body.style.overflow = "";
    document.documentElement.classList.remove("lb-open");
    img.removeAttribute("src");
    if (lastFocus) lastFocus.focus();
  }

  function step(delta) {
    index = (index + delta + items.length) % items.length;
    render();
  }

  items.forEach(function (item, i) {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      open(i);
    });
  });

  box.addEventListener("click", function (e) {
    if (e.target.closest("[data-lb-close]")) return close();
    if (e.target.closest("[data-lb-prev]")) return step(-1);
    if (e.target.closest("[data-lb-next]")) return step(1);
    // Kattintás a képen kívülre: bezárás
    if (!e.target.closest(".lb__img") && !e.target.closest(".lb__btn")) close();
  });

  document.addEventListener("keydown", function (e) {
    if (box.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); close(); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); step(-1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); step(1); }
    else if (e.key === "Tab") {
      // A fókusz maradjon a nézegetőn belül
      var focusable = box.querySelectorAll("button:not(:disabled)");
      if (!focusable.length) return;
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Ujjal húzás telefonon
  var startX = null;
  box.addEventListener("touchstart", function (e) { startX = e.touches[0].clientX; }, { passive: true });
  box.addEventListener("touchend", function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 45) step(dx < 0 ? 1 : -1);
    startX = null;
  }, { passive: true });
})();
