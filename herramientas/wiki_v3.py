#!/usr/bin/env python3
# Wiki de MaJo, tercera tanda (2026-11-09): sección «Juegos extra» (los que solo se juegan en la web),
# artículo de El Último Timbre y Object Khaos jugable en la web (sin multijugador).
# Uso: python3 wiki_v3.py <cuerpo_novela.html>
import os, re, sys
R = os.path.expanduser('~/juegos/majo')
W = os.path.join(R, 'wiki')
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)

EXTRA = [  # (artículo, carpeta en jugar/, título, banner, texto)
    ('el-ultimo-timbre', 'el-ultimo-timbre', 'El Último Timbre', 'el-ultimo-timbre-banner.png',
     'Novela visual en la Academia MaJo: personajes de todos los juegos, muchísimas decisiones, un juicio de clase y 35 finales.'),
    ('object-khaos', 'object-khaos', 'Object Khaos', 'object-khaos-banner.png',
     '¡El concurso de los objetos! Señor Pantalla, Isla Escenario y 20 minijuegos. En la web se juega sin conexión, contra bots.'),
    ('jary', 'jary', 'JARY: Ciudad Muerta', 'jary-banner.png',
     'Jary, su armadura apocalíptica y una ciudad tomada por zombis. Ávila, el diario de 20 páginas y la Segunda Aventura secreta.'),
    ('majo-maker', 'majo-maker', 'MaJo Maker', 'majo-maker-banner.png',
     'El editor de niveles de los tres juegos: activadores, equivalencias, NPCs con diálogos y niveles para compartir.'),
]
NAV_EXTRA = ['jary.html', 'object-khaos.html', 'majo-maker.html', 'el-ultimo-timbre.html']

def armar(slug, cuerpo, titulo, desc):
    p = rd(os.path.join(W, 'pancho.html'))
    cab, pie = p[:p.index('<main')], p[p.index('</main>') + len('</main>'):]
    cab = cab.replace('<title>Pancho · Wiki</title>', f'<title>{titulo} · Wiki</title>')
    cab = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', cab)
    cab = cab.replace(' aria-current="page"', '')
    wr(os.path.join(W, slug + '.html'), cab + cuerpo.strip() + '\n' + pie)

# 1) artículo nuevo (se arma con la cabecera de pancho.html, que ya tiene el menú nuevo)
def menu(s, actual):
    """Menú de la wiki: juegos principales, «Juegos extra» y sus cuatro juegos, y lo demás."""
    nav = ['<a href="./">Inicio de la Wiki</a>', '<a href="chulins-adventure.html">Chulin\'s Adventure</a>', '<a href="joshua-2d.html">Joshua 2D</a>',
           '<a href="pancho.html">Pancho</a>', '<a class="extra" href="./#extra">Juegos extra:</a>', '<a href="el-ultimo-timbre.html">El Último Timbre</a>',
           '<a href="object-khaos.html">Object Khaos</a>', '<a href="jary.html">JARY: Ciudad Muerta</a>', '<a href="majo-maker.html">MaJo Maker</a>',
           '<a href="colectucus.html">Colectucus y Bondis-AR</a>', '<a href="majo-associations.html">MaJo Associations</a>']
    nav = [n.replace(f'href="{actual}">', f'href="{actual}" aria-current="page">') for n in nav]
    return re.sub(r'<nav>.*?</nav>', '<nav>\n      ' + '\n      '.join(nav) + '\n    </nav>', s, count=1, flags=re.S)

for f in os.listdir(W):
    if f.endswith('.html'):
        s = rd(os.path.join(W, f)); wr(os.path.join(W, f), menu(s, f if f != 'index.html' else './'))
armar('el-ultimo-timbre', rd(sys.argv[1]), 'El Último Timbre',
      'Wiki de El Último Timbre: la novela visual de la Academia MaJo, con personajes de Chulin\'s Adventure, Joshua 2D, Pancho, JARY y Object Khaos, 20 finales y un juicio de clase.')
s = rd(os.path.join(W, 'el-ultimo-timbre.html')); wr(os.path.join(W, 'el-ultimo-timbre.html'), menu(s, 'el-ultimo-timbre.html'))

# 2) Object Khaos: ahora se juega en la web (sin multijugador)
s = rd(os.path.join(W, 'object-khaos.html'))
s = s.replace('<p class="jugar-web"><span class="etiqueta pronto">En desarrollo</span><span>Todavía no se puede jugar desde la wiki.</span></p>',
              '<p class="jugar-web"><a class="btn" href="../jugar/object-khaos/">▶ Jugar en la web</a><span>Versión web sin multijugador: se juega sin conexión, contra bots (entrenamiento, Object Party, concursos e historia). El juego sigue <b>en desarrollo</b>.</span></p>')
s = s.replace('<dt>Plataformas</dt><dd>PC (Windows, Linux y navegador) y Android</dd>', '<dt>Plataformas</dt><dd>PC (Windows, Linux), Android y la web (sin multijugador)</dd>')
s = s.replace('Por eso todavía no tiene versión para jugar desde esta wiki.', 'Mientras tanto, desde esta wiki se puede jugar la versión web, sin conexión y contra bots: el multijugador queda para la versión completa.')
wr(os.path.join(W, 'object-khaos.html'), s)

# 3) portada de la wiki: principales arriba, «Juegos extra» aparte
s = rd(os.path.join(W, 'index.html'))
main = s[s.index('<main'):s.index('</main>')]
tarj = lambda slug, d, tit, ban, txt: f'''    <article class="tarjeta">
      <img class="banner" src="../img/{ban}" alt="" loading="lazy">
      <div class="cuerpo">
        <h3 style="margin:0">{tit}</h3>
        <p>{txt}</p>
        <div class="pie"><a href="{slug}.html">Leer artículo</a> <a class="jugar" href="../jugar/{d}/">▶ Jugar en la web</a></div>
      </div>
    </article>'''
# saca las tarjetas de los cuatro juegos extra de donde estaban
for slug, *_ in EXTRA:
    main = re.sub(r'\s*<article class="tarjeta">\s*<img class="banner" src="\.\./img/[^"]+" alt="" loading="lazy">\s*<div class="cuerpo">\s*<h3[^>]*>[^<]*(?:<span[^>]*>[^<]*</span>)?</h3>\s*<p>[^<]*</p>\s*<div class="pie"><a href="' + re.escape(slug) + r'\.html">.*?</article>', '', main, flags=re.S)
seccion = '''
  <section id="extra">
    <h2>Juegos extra</h2>
    <p>Los que se juegan solo en la web, acá mismo en el navegador (también en el celular).</p>
    <div class="rejilla">
''' + '\n'.join(tarj(*e) for e in EXTRA) + '''
    </div>
  </section>
'''
i = main.index('<div class="rejilla" style="margin-top:18px">')
main = main[:i] + seccion.strip() + '\n\n  ' + main[i:]
s = s[:s.index('<main')] + main + s[s.index('</main>'):]
s = s.replace('Chulin\'s Adventure, Joshua 2D, Pancho, JARY: Ciudad Muerta y Object Khaos, y artículos', 'Chulin\'s Adventure, Joshua 2D y Pancho, los juegos extra de la web y artículos')
wr(os.path.join(W, 'index.html'), s)

# 4) portada del sitio: «Juegos extra» en el menú y en su propia sección (MaJo Maker pasa ahí)
s = rd(os.path.join(R, 'index.html'))
if 'id="extra"' not in s:
    s = s.replace('<a href="#juegos">Juegos</a>', '<a href="#juegos">Juegos</a>\n      <a href="#extra">Juegos extra</a>', 1)
    i = s.index('<h3>Y además: MaJo Maker</h3>'); j = s.index('</section>', i)
    extra = '''</div>
  </section>

  <section id="extra">
    <div class="contenedor">
      <h2>Juegos extra</h2>
      <p>Solo en la web: se juegan en el navegador, también en el celular.</p>
      <div class="rejilla">
''' + '\n'.join(f'''        <article class="tarjeta">
          <img class="banner" src="img/{ban}" alt="{tit}" loading="lazy">
          <div class="cuerpo">
            <h3 style="margin:0">{tit}</h3>
            <p>{txt}</p>
            <div class="pie">
              <a class="jugar" href="jugar/{d}/">▶ Jugar en la web</a>
              <a href="wiki/{slug}.html">Wiki</a>
            </div>
          </div>
        </article>''' for slug, d, tit, ban, txt in EXTRA) + '''
      </div>
    </div>
'''
    # el bloque «Y además: MaJo Maker» se reemplaza por la sección nueva
    k = s.rindex('</div>', i, j)
    s = s[:i] + extra + s[j:]
    s = s.replace('<p>Tres juegos de plataformas 2D para Android y PC,', '<p>Tres juegos de plataformas 2D para Android, PC y la web,')
wr(os.path.join(R, 'index.html'), s)

# 5) estilo del rótulo «Juegos extra:» en el menú
c = rd(os.path.join(R, 'css', 'estilo.css'))
if 'nav a.extra' not in c:
    c += '\n/* rótulo «Juegos extra» del menú de la wiki */\nnav a.extra { font-weight: 700; opacity: .8; }\n#extra h2 { margin-top: 26px; }\n'
    wr(os.path.join(R, 'css', 'estilo.css'), c)
