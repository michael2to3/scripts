// ==UserScript==
// @name         Disable Telegram WebK Swipe (Edge‑Swipe Blocker)
// @version      0.2
// @description  Blocks chat switching/back‑navigation swipes in web.telegram.org/k without breaking vertical scroll.
// @author       michael2to3
// @match        https://web.telegram.org/k/*
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  const onTouchMove = (e) => {
    if (e.touches.length !== 1) return;

      e.preventDefault();
      e.stopImmediatePropagation();
  };

  const opts = { capture: true, passive: false };
  window.addEventListener('touchmove', onTouchMove, opts);
})();

