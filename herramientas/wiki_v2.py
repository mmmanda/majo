#!/usr/bin/env python3
# Wiki de MaJo, segunda tanda (2026-11-09): JARY exclusivo de la web, artículo de Object Khaos,
# artículo de Colectucus y Bondis-AR al día. Uso: python3 wiki_v2.py <ok_cuerpo.html> <colectucus_cuerpo.html>
import os, re, sys
R = os.path.expanduser('~/juegos/majo')
W = os.path.join(R, 'wiki')
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

def armar(slug, cuerpo, titulo, desc, actual):
    """Página con la cabecera y el pie de pancho.html y el cuerpo dado."""
    p = rd(os.path.join(W, 'pancho.html'))
    cab, pie = p[:p.index('<main')], p[p.index('</main>') + len('</main>'):]
    cab = cab.replace('<title>Pancho · Wiki</title>', f'<title>{titulo} · Wiki</title>')
    cab = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', cab)
    cab = cab.replace(' aria-current="page"', '')
    cab = cab.replace(f'<a href="{actual}">', f'<a href="{actual}" aria-current="page">', 1)
    assert 'aria-current="page"' in cab, slug
    wr(os.path.join(W, slug + '.html'), cab + cuerpo.strip() + '\n' + pie)

# 1) menú: Object Khaos después de JARY; «Colectucus» pasa a «Colectucus y Bondis-AR»
for f in os.listdir(W):
    if not f.endswith('.html'): continue
    s = rd(os.path.join(W, f))
    if 'href="object-khaos.html"' not in s:
        s = re.sub(r'(\n(\s*)<a href="jary.html"[^>]*>JARY: Ciudad Muerta</a>)', r'\1\n\2<a href="object-khaos.html">Object Khaos</a>', s, count=1)
    s = re.sub(r'(<a href="colectucus.html"[^>]*>)Colectucus</a>', r'\1Colectucus y Bondis-AR</a>', s)
    wr(os.path.join(W, f), s)

# 2) JARY: exclusivo de la web
s = rd(os.path.join(W, 'jary.html'))
s = s.replace('<dt>Plataformas</dt><dd>Navegador y Android (APK)</dd>', '<dt>Plataformas</dt><dd>Web (exclusivo del navegador)</dd>')
s = s.replace('Se juega con teclado, con control o con los botones táctiles del celular, y el progreso se guarda solo en el navegador.',
              'Es <strong>exclusivo de la web</strong>: se juega en el navegador, en la computadora o en el celular, con teclado, con control o con los botones táctiles, y el progreso se guarda solo en el navegador.')
assert 'Android' not in s.split('<main', 1)[1].split('</main>')[0], 'quedó Android en JARY'
wr(os.path.join(W, 'jary.html'), s)
c = os.path.join(R, 'herramientas', 'jary_cuerpo.html')
t = rd(c).replace('<dt>Plataformas</dt><dd>Navegador y Android (APK)</dd>', '<dt>Plataformas</dt><dd>Web (exclusivo del navegador)</dd>')
wr(c, t)

# 3) artículos nuevos o reescritos
armar('object-khaos', rd(sys.argv[1]), 'Object Khaos',
      'Wiki de Object Khaos: el concurso de los objetos. Modos, 20 minijuegos, 17 concursantes, el modo historia en Isla Escenario y el estado del desarrollo.',
      'object-khaos.html')
armar('colectucus', rd(sys.argv[2]), 'Colectucus y Bondis-AR',
      'Wiki de Colectucus y Bondis-AR: colectivos de 18 provincias, cómo llegar, mapas, GPS en vivo y horarios, la app para Android, el panel para empresas y la API para socios.',
      'colectucus.html')

# 4) portada de la wiki
s = rd(os.path.join(W, 'index.html'))
if 'object-khaos.html' not in s.split('<main', 1)[1]:
    tarjeta = '''    <article class="tarjeta">
      <img class="banner" src="../img/object-khaos-banner.png" alt="" loading="lazy">
      <div class="cuerpo">
        <h3 style="margin:0">Object Khaos <span class="etiqueta pronto">En desarrollo</span></h3>
        <p>¡El concurso de los objetos! Señor Pantalla, Isla Escenario, 20 minijuegos, votaciones, eliminaciones y La Producción.</p>
        <div class="pie"><a href="object-khaos.html">Leer artículo</a></div>
      </div>
    </article>
'''
    i = s.index('<h3 style="margin:0">MaJo Maker</h3>')
    j = s.index('<article class="tarjeta">', s.index('<div class="rejilla" style="margin-top:18px">'))
    s = s[:j] + tarjeta.lstrip() + '    ' + s[j:]
s = re.sub(r'<h3 style="margin:0">Colectucus</h3>\s*<p>[^<]*</p>',
           '<h3 style="margin:0">Colectucus y Bondis-AR</h3>\n        <p>Los colectivos de 18 provincias: cómo llegar, mapas, GPS en vivo y horarios, la app para Android y el panel para empresas.</p>', s)
s = s.replace('Pancho y JARY: Ciudad Muerta, y artículos', 'Pancho, JARY: Ciudad Muerta y Object Khaos, y artículos')
s = s.replace('artículos de MaJo Maker y Colectucus.', 'artículos de MaJo Maker y Colectucus y Bondis-AR.')
wr(os.path.join(W, 'index.html'), s)

# 5) portada del sitio: el aviso viejo de «solo Tucumán» ya no es cierto
s = rd(os.path.join(R, 'index.html'))
s = re.sub(r'<div class="aviso">\s*<strong>Por ahora, solo la web y solo Tucumán\.</strong>.*?</div>',
           '<div class="aviso">\n            <strong>Colectucus es la parte tucumana de Bondis-AR.</strong> Hoy hay sitio en 18 provincias, en <a href="https://bondisar.com.ar/" target="_blank" rel="noopener">bondisar.com.ar</a>, y una app para Android.\n          </div>', s, flags=re.S)
s = s.replace('<tr><td>Otras provincias</td><td><span class="etiqueta pronto">Próximamente</span></td></tr>',
              '<tr><td>Otras 17 provincias · <a href="https://bondisar.com.ar/" target="_blank" rel="noopener">bondisar.com.ar</a></td><td><span class="etiqueta ok">Disponible</span></td></tr>')
s = s.replace('<tr><td>App para Android</td><td><span class="etiqueta pronto">Próximamente</span></td></tr>',
              '<tr><td>App Bondis-AR para Android</td><td><span class="etiqueta ok">Disponible</span></td></tr>')
wr(os.path.join(R, 'index.html'), s)
