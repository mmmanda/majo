#!/usr/bin/env python3
# Página de la guía avanzada de El Último Timbre (bloqueada por una pregunta). La guía va CIFRADA:
# acá solo entra el texto cifrado (sal, iv y datos) que arma novela/tools/guia/armar-guia.js. La respuesta no está.
# Uso: python3 armar_guia_wiki.py <guia-cifrada.json>
import os, re, sys, json
R = os.path.expanduser('~/juegos/majo'); W = os.path.join(R, 'wiki')
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
d = json.load(open(sys.argv[1]))
base = rd(os.path.join(W, 'el-ultimo-timbre.html'))
cab, pie = base[:base.index('<main')], base[base.index('</main>') + len('</main>'):]
cab = re.sub(r'<title>[^<]*</title>', '<title>Guía avanzada de El Último Timbre · Wiki</title>', cab)
cab = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Guía avanzada para conseguir los 35 finales de El Último Timbre. Se desbloquea respondiendo una pregunta.">', cab)
cab = cab.replace(' aria-current="page"', '')
cuerpo = '''<main class="contenedor">
  <article class="articulo" style="max-width:900px;margin:0 auto">
    <p><a href="el-ultimo-timbre.html">← El Último Timbre</a></p>
    <h1>Guía avanzada: los 35 finales</h1>
    <div id="cerrada" class="tarjeta"><div class="cuerpo">
      <p>La guía está bloqueada. Para abrirla, responde:</p>
      <p><b>¿Cuál fue el primer juego de Manda en Julian's Editor?</b></p>
      <form id="fGuia" autocomplete="off"><input id="rGuia" type="text" aria-label="Respuesta" style="font:inherit;padding:8px 10px;border:2px solid #222;border-radius:10px;width:min(360px,100%)"> <button class="btn" type="submit">Abrir la guía</button></form>
      <p id="mGuia" role="status" style="min-height:1.4em;font-weight:700"></p>
    </div></div>
    <div id="abierta" hidden></div>
  </article>
</main>
<style>
#abierta h2{margin-top:28px} #abierta .final{border:2px solid #222;border-radius:14px;padding:10px 14px;margin:12px 0;background:#fff}
#abierta .final h3{margin:0 0 6px} #abierta .pasos{margin:6px 0;padding-left:22px} #abierta details summary{cursor:pointer;font-weight:700}
#abierta .etq{font-size:.75em;border:2px solid #222;border-radius:999px;padding:1px 8px;margin-left:6px}
</style>
<script>
(function () {
  'use strict';
  var D = ''' + json.dumps(d) + ''';
  var CLAVE = 'guia_ultimo_timbre_v1';
  function b64(s) { var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
  function a64(buf) { var u = new Uint8Array(buf), s = ''; for (var i = 0; i < u.length; i++) s += String.fromCharCode(u[i]); return btoa(s); }
  // misma normalización que al cifrar: minúsculas, sin tildes, «+» = «plus», sin signos ni espacios de más
  function norm(t) { return String(t).normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase().replace(/\\+/g, ' plus ').replace(/[^a-z0-9 ]+/g, ' ').replace(/\\s+/g, ' ').trim(); }
  function mostrar(html) { var a = document.getElementById('abierta'); a.innerHTML = html; a.hidden = false; document.getElementById('cerrada').hidden = true; }
  function descifrar(key) { return crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64(D.iv) }, key, b64(D.ct)).then(function (p) { return new TextDecoder().decode(p); }); }
  function derivar(resp) {
    return crypto.subtle.importKey('raw', new TextEncoder().encode(norm(resp)), 'PBKDF2', false, ['deriveKey']).then(function (k) {
      return crypto.subtle.deriveKey({ name: 'PBKDF2', salt: b64(D.salt), iterations: D.iter, hash: 'SHA-256' }, k, { name: 'AES-GCM', length: 256 }, true, ['decrypt']);
    });
  }
  // si ya se abrió antes en este navegador, se guarda la clave (no la respuesta)
  try {
    var g = localStorage.getItem(CLAVE);
    if (g) crypto.subtle.importKey('raw', b64(g), 'AES-GCM', false, ['decrypt']).then(descifrar).then(mostrar).catch(function () { try { localStorage.removeItem(CLAVE); } catch (e) {} });
  } catch (e) { /* sin almacenamiento: se pregunta cada vez */ }
  document.getElementById('fGuia').addEventListener('submit', function (ev) {
    ev.preventDefault();
    var m = document.getElementById('mGuia'); m.textContent = 'Comprobando…'; m.style.color = '';
    var key;
    derivar(document.getElementById('rGuia').value).then(function (k) { key = k; return descifrar(k); }).then(function (html) {
      mostrar(html);
      crypto.subtle.exportKey('raw', key).then(function (raw) { try { localStorage.setItem(CLAVE, a64(raw)); } catch (e) {} });
    }).catch(function () { m.textContent = 'Respuesta incorrecta'; m.style.color = '#c1121f'; });
  });
})();
</script>
'''
wr(os.path.join(W, 'el-ultimo-timbre-guia.html'), cab + cuerpo + pie)
# enlaces: desde el artículo y desde «Juegos extra» (wiki y portada del sitio)
s = rd(os.path.join(W, 'el-ultimo-timbre.html'))
if 'el-ultimo-timbre-guia.html' not in s:
    s = s.replace('<section id="finales">\n      <h2>Los 20 finales</h2>', '<section id="finales">\n      <h2>Los 20 finales</h2>')
    s = re.sub(r'(<section id="finales">\s*<h2>[^<]*</h2>)', r'\1\n      <p><a class="btn" href="el-ultimo-timbre-guia.html">📘 Guía avanzada de los 35 finales</a> <small>(se abre respondiendo una pregunta)</small></p>', s, count=1)
    wr(os.path.join(W, 'el-ultimo-timbre.html'), s)
s = rd(os.path.join(W, 'index.html'))
if 'el-ultimo-timbre-guia.html' not in s:
    s = s.replace('<a href="el-ultimo-timbre.html">Leer artículo</a>', '<a href="el-ultimo-timbre.html">Leer artículo</a> <a href="el-ultimo-timbre-guia.html">Guía avanzada</a>', 1)
    wr(os.path.join(W, 'index.html'), s)
s = rd(os.path.join(R, 'index.html'))
if 'el-ultimo-timbre-guia.html' not in s:
    s = s.replace('<a href="wiki/el-ultimo-timbre.html">Wiki</a>', '<a href="wiki/el-ultimo-timbre.html">Wiki</a>\n              <a href="wiki/el-ultimo-timbre-guia.html">Guía avanzada</a>', 1)
    wr(os.path.join(R, 'index.html'), s)
print('ok', os.path.getsize(os.path.join(W, 'el-ultimo-timbre-guia.html')))
