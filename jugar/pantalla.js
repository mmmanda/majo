// Versión web de los juegos (la agrega ~/juegos/publicar.sh en el servidor):
// en un celular, el primer toque pone el juego en pantalla completa y horizontal, como en la app.
(function () {
  'use strict';
  if (!window.matchMedia || !matchMedia('(pointer: coarse)').matches) return;
  var hecho = false;
  function pedir() {
    if (hecho) return;
    hecho = true;
    var d = document.documentElement, pc = d.requestFullscreen || d.webkitRequestFullscreen;
    if (!pc || document.fullscreenElement) return;
    try {
      var p = pc.call(d, { navigationUI: 'hide' });
      var girar = function () { var o = window.screen && window.screen.orientation; if (o && o.lock) o.lock('landscape').catch(function () {}); };
      if (p && p.then) p.then(girar).catch(function () {}); else girar();
    } catch (e) { /* el navegador no deja: se juega igual */ }
  }
  addEventListener('touchend', pedir, { passive: true });
})();
