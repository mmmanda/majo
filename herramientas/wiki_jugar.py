#!/usr/bin/env python3
# Agrega «Jugar en la web» a la wiki de MaJo (repo mmmanda/majo) y el artículo de JARY: Ciudad Muerta.
import os, re
R = os.path.expanduser('~/juegos/majo')
def rd(p): return open(os.path.join(R, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(R, p), 'w', encoding='utf-8').write(s)

JUEGOS = {  # artículo -> carpeta en jugar/
    'chulins-adventure': 'chulins-adventure', 'joshua-2d': 'joshua-2d', 'pancho': 'pancho',
    'jary': 'jary', 'majo-maker': 'majo-maker',
}
def boton(slug, nota=True):
    s = f'<p class="jugar-web"><a class="btn" href="../jugar/{slug}/">▶ Jugar en la web</a>'
    if nota: s += '<span>En el navegador, también en el celular (mejor en horizontal). Tu progreso queda guardado en este navegador.</span>'
    return s + '</p>'

# 1) estilo
css = rd('css/estilo.css')
if '.jugar-web' not in css:
    css += '''
/* Botón «Jugar en la web» de la wiki */
.jugar-web { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; margin: 6px 0 18px; }
.jugar-web span { font-size: .9rem; color: var(--suave); }
.pie .jugar { font-weight: 700; }
'''
    wr('css/estilo.css', css)

# 2) menú de la wiki: JARY después de Pancho
paginas = [f for f in os.listdir(os.path.join(R, 'wiki')) if f.endswith('.html')]
for f in paginas:
    s = rd('wiki/' + f)
    if 'href="jary.html"' not in s:
        s = re.sub(r'(\n(\s*)<a href="pancho.html"[^>]*>Pancho</a>)', r'\1\n\2<a href="jary.html">JARY: Ciudad Muerta</a>', s, count=1)
    art = f[:-5]
    if art in JUEGOS and 'class="jugar-web"' not in s:
        s = re.sub(r'(<h1>[^<]*</h1>)', lambda m: m.group(1) + '\n    ' + boton(JUEGOS[art]), s, count=1)
    if art == 'majo-maker':
        s = s.replace('<dt>Plataformas</dt><dd>Android (7.0 o superior) y PC (navegador)</dd>',
                      '<dt>Plataformas</dt><dd>Web (exclusivo del navegador)</dd>')
    wr('wiki/' + f, s)

# 3) portada de la wiki: tarjeta de JARY y botón en cada tarjeta
s = rd('wiki/index.html')
for art, slug in JUEGOS.items():
    s = s.replace(f'<div class="pie"><a href="{art}.html">Leer artículo</a></div>',
                  f'<div class="pie"><a href="{art}.html">Leer artículo</a> <a class="jugar" href="../jugar/{slug}/">▶ Jugar en la web</a></div>')
if 'jary.html' not in s.split('<main', 1)[1]:
    tarjeta = '''    <article class="tarjeta">
      <img class="banner" src="../img/jary-banner.png" alt="" loading="lazy">
      <div class="cuerpo">
        <h3 style="margin:0">JARY: Ciudad Muerta</h3>
        <p>Jary, su armadura apocalíptica y una ciudad tomada por zombis. Ávila, el diario de 20 páginas y la Segunda Aventura secreta.</p>
        <div class="pie"><a href="jary.html">Leer artículo</a> <a class="jugar" href="../jugar/jary/">▶ Jugar en la web</a></div>
      </div>
    </article>
  </div>

  <div class="rejilla" style="margin-top:18px">'''
    # va al final de la primera rejilla (después de Pancho)
    i = s.index('<h3 style="margin:0">Pancho</h3>')
    j = s.index('  </div>\n\n  <div class="rejilla" style="margin-top:18px">', i)
    s = s[:j] + tarjeta + s[j + len('  </div>\n\n  <div class="rejilla" style="margin-top:18px">'):]
s = s.replace('Chulin\'s Adventure, Joshua 2D y Pancho, y artículos', 'Chulin\'s Adventure, Joshua 2D, Pancho y JARY: Ciudad Muerta, y artículos')
s = s.replace('<p class="lema">Todo sobre los juegos y proyectos de MaJo Associations: historias completas, personajes, mundos, jefes, finales, secretos y logros.</p>',
              '<p class="lema">Todo sobre los juegos y proyectos de MaJo Associations: historias completas, personajes, mundos, jefes, finales, secretos y logros. Y cada juego se puede jugar acá mismo, en el navegador.</p>')
wr('wiki/index.html', s)

# 4) portada del sitio: «Jugar en la web» en cada juego
s = rd('index.html')
for art, slug in JUEGOS.items():
    s = s.replace(f'<a href="wiki/{art}.html">Wiki</a>', f'<a class="jugar" href="jugar/{slug}/">▶ Jugar en la web</a>\n              <a href="wiki/{art}.html">Wiki</a>', 1) if f'href="jugar/{slug}/"' not in s else s
wr('index.html', s)
