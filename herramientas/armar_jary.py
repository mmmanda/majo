#!/usr/bin/env python3
# Arma wiki/jary.html con la cabecera y el pie de wiki/pancho.html y el cuerpo de jary_cuerpo.html
import os, re, sys
R = os.path.expanduser('~/juegos/majo/wiki')
p = open(os.path.join(R, 'pancho.html'), encoding='utf-8').read()
cuerpo = open(sys.argv[1], encoding='utf-8').read().strip()
cab = p[:p.index('<main')]
pie = p[p.index('</main>') + len('</main>'):]
cab = cab.replace('<title>Pancho · Wiki</title>', '<title>JARY: Ciudad Muerta · Wiki</title>')
cab = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Wiki de JARY: Ciudad Muerta: Jary, Ávila y Fausta, el diario de 20 páginas, los dos finales, la Segunda Aventura, armas, enemigos y controles.">', cab)
cab = cab.replace('<a href="pancho.html" aria-current="page">Pancho</a>', '<a href="pancho.html">Pancho</a>')
cab = cab.replace('<a href="jary.html">JARY: Ciudad Muerta</a>', '<a href="jary.html" aria-current="page">JARY: Ciudad Muerta</a>')
assert 'aria-current="page">JARY' in cab
cuerpo = cuerpo.replace('<h1>JARY: Ciudad Muerta</h1>', '<h1>JARY: Ciudad Muerta</h1>\n    <p class="jugar-web"><a class="btn" href="../jugar/jary/">▶ Jugar en la web</a><span>En el navegador, también en el celular (mejor en horizontal). Tu progreso queda guardado en este navegador.</span></p>')
open(os.path.join(R, 'jary.html'), 'w', encoding='utf-8').write(cab + cuerpo + '\n' + pie)
