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

  const THRESHOLD = 10;
  let startX = 0;
  let startY = 0;

  const onTouchStart = (e) => {
    if (e.touches.length !== 1) return;
    const t = e.touches[0];
    startX = t.clientX;
    startY = t.clientY;
  };

  const onTouchMove = (e) => {
    if (e.touches.length !== 1) return;

    const t = e.touches[0];
    const dx = t.clientX - startX;
    const dy = t.clientY - startY;

    if (Math.abs(dx) > Math.abs(dy) + THRESHOLD) {
      if (e.target.closest('input, textarea, [contenteditable="true"]')) return;

      e.preventDefault();
      e.stopImmediatePropagation();
    }
  };

  const opts = { capture: true, passive: false };
  window.addEventListener('touchstart', onTouchStart, opts);
  window.addEventListener('touchmove', onTouchMove, opts);
})();
