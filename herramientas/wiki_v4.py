# El Último Timbre en la wiki: Mateo en lugar de Chispa, 35 finales en árbol, temas y expresiones propias.
import os
R = os.path.expanduser('~/juegos/majo')
REP = [
 ('<dt>Finales</dt><dd>20</dd>', '<dt>Finales</dt><dd>35, en un árbol de rutas</dd>'),
 ('<td>Verity (no puede mentir), Candado (no confía en nadie) y Chispa (no se queda quieta)</td>', '<td>Verity (no puede mentir), Candado (no confía en nadie) y Mateo (alegre, aunque a veces le dan bajones)</td>'),
 ('y Verity, Candado y Chispa desde Isla Escenario.', 'y Verity, Candado y Mateo desde Isla Escenario.'),
 ('<li>La <strong>Galería de finales</strong> muestra los que ya encontraste.</li>', '<li>La <strong>Galería de finales</strong> es un árbol de rutas: muestra desde qué rama se llega a cada final y cuáles ya encontraste.</li>\n        <li>El miércoles te puedes <strong>cambiar de club</strong>: las rutas se cruzan y desde una se llega a otras.</li>'),
 ('<p>Hay 14 finales con personajes (románticos, y alguno de amistad), un final de amistad con todo el club, tres finales malos, un <strong>final secreto</strong> y un <strong>final verdadero</strong>, que solo aparece cuando ya viste bastante de la academia.</p>',
  '<p>Son <strong>35 finales</strong>: 14 con personajes (románticos, y alguno de amistad), 5 de club completo, 5 triángulos agridulces (cuando dos te quieren a la vez), 5 ramas especiales del jueves a la noche (una por club), un final de amistad, tres finales malos, un <strong>final secreto</strong> y un <strong>final verdadero</strong>, que solo aparece cuando ya viste bastante de la academia.</p>'),
 ('Jary, Ávila, Verity, Candado y Chispa se adaptaron', 'Jary, Ávila, Verity, Candado y Mateo se adaptaron'),
 ('los ojos negros y la boca de Verity. Los fondos de la escuela y la música se hacen dentro del juego, como en los demás juegos de MaJo.</p>',
  'los ojos negros y la boca de Verity, la luna y el gorro de dormir de Mateo. Cada uno tiene además una <strong>expresión exclusiva</strong> que aparece en un momento clave de su ruta (Chulin en modo eléctrico, la sonrisa forzada de Mateo en un bajón, el visor rojo de Jary…).</p>\n      <p>La música es propia de la novela, compuesta dentro del juego: temas para el menú, la escuela, los momentos tranquilos, la tensión, el juicio, el romance y los finales, y un tema para cada uno de los 14 personajes.</p>'),
 ('<p>Es una historia de romance escolar sana: citas, confesiones, celos y amistad, sin contenido sexual ni violencia.',
  '<p>Es una historia de romance escolar sana: citas, confesiones, celos y amistad, sin contenido sexual ni violencia. La ruta de Mateo habla de los días bajones con cuidado: muestra que hablar y pedir ayuda está bien.'),
]
for f in ['wiki/el-ultimo-timbre.html', 'herramientas/novela_cuerpo.html']:
    p = os.path.join(R, f); s = open(p, encoding='utf-8').read()
    for a, b in REP:
        assert a in s, (f, a[:50]); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
for f in ['wiki/index.html', 'index.html']:
    p = os.path.join(R, f); s = open(p, encoding='utf-8').read()
    s = s.replace('muchísimas decisiones, un juicio de clase y 20 finales.', 'muchísimas decisiones, un juicio de clase y 35 finales.')
    open(p, 'w', encoding='utf-8').write(s)
p = os.path.join(R, 'herramientas/wiki_v3.py'); s = open(p, encoding='utf-8').read()
s = s.replace('un juicio de clase y 20 finales.', 'un juicio de clase y 35 finales.'); open(p, 'w', encoding='utf-8').write(s)
