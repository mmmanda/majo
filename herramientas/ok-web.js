// Versión web de Object Khaos SIN multijugador. Lo agrega publicar.sh SOLO en la copia publicada (no está en el código del juego).
// 1) Corta toda conexión a internet que no sea a esta misma página (Firebase, servidores, WebRTC): el juego queda sin conexión.
// 2) Entra directo a «Jugar sin conexión» (bots, entrenamiento, Object Party e historia).
// 3) Esconde lo que necesita conexión: cuenta, salas, amigos, tienda, rankings y la dirección del servidor.
(function () {
  'use strict';
  var aqui = location.origin;
  function local(u) { try { return new URL(String(u), location.href).origin === aqui; } catch (e) { return false; } }
  function sinRed() { return Promise.reject(new TypeError('Sin conexión (versión web)')); }
  var f0 = window.fetch;
  window.fetch = function (u) { var url = u && u.url ? u.url : u; return local(url) ? f0.apply(this, arguments) : sinRed(); };
  var o0 = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) { if (!local(u)) throw new Error('Sin conexión (versión web)'); return o0.apply(this, arguments); };
  function Muerto() { var s = this; s.readyState = 3; setTimeout(function () { if (s.onerror) s.onerror(new Event('error')); if (s.onclose) s.onclose({ code: 1006 }); }, 0); }
  Muerto.prototype = { send: function () {}, close: function () {}, addEventListener: function () {}, removeEventListener: function () {} };
  Muerto.CONNECTING = 0; Muerto.OPEN = 1; Muerto.CLOSING = 2; Muerto.CLOSED = 3;
  window.WebSocket = Muerto; window.EventSource = Muerto;
  window.RTCPeerConnection = undefined; window.webkitRTCPeerConnection = undefined;
  if (navigator.sendBeacon) navigator.sendBeacon = function () { return false; };
  // (por las dudas: el juego no tiene sesión guardada de Firebase en esta página)
  try { for (var i = localStorage.length - 1; i >= 0; i--) { var k = localStorage.key(i); if (k && /^firebase:/.test(k)) localStorage.removeItem(k); } } catch (e) { /* nada */ }

  var OCULTAR_BOTONES = /^(Ingresar|Crear cuenta|Entrar como invitado|Reintentar|Configurar servidor|Unirse|Mirar como espectador|Cerrar sesi[oó]n)$/;
  var OCULTAR_TARJETAS = /^\S*\s*(Tienda|Amigos|Rankings|Buscar salas|Crear sala|Partida r[aá]pida)/;
  var OCULTAR_TEXTOS = /(Unirse con c[oó]digo|requieren cuenta online|Direcci[oó]n del servidor|Servidor propio|Cuenta online)/i;
  function limpiar() {
    var bs = document.querySelectorAll('button');
    for (var i = 0; i < bs.length; i++) {
      var b = bs[i], t = (b.textContent || '').trim();
      if (/^Jugar sin conexi[oó]n$/.test(t) && !b.__ok) { b.__ok = 1; setTimeout(function (x) { return function () { x.click(); }; }(b), 0); }
      if (OCULTAR_BOTONES.test(t) || OCULTAR_TARJETAS.test(t)) b.style.display = 'none';
    }
    var cs = document.querySelectorAll('.panel, .chip, label.field, .seg');
    for (var j = 0; j < cs.length; j++) if (OCULTAR_TEXTOS.test(cs[j].textContent || '') || (cs[j].classList.contains('seg') && /Ingresar/.test(cs[j].textContent))) cs[j].style.display = 'none';
    // el formulario de cuenta (si aparece un instante) no se ve
    var ins = document.querySelectorAll('input[type=password]');
    for (var k = 0; k < ins.length; k++) { var l = ins[k].closest('label'); if (l) l.style.display = 'none'; }
  }
  new MutationObserver(limpiar).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
  document.addEventListener('DOMContentLoaded', limpiar);
})();
