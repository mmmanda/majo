#!/bin/bash
# Publica la web de MaJo (wiki + juegos jugables) en https://135.181.107.239/majo/
#   bash ~/juegos/publicar.sh            -> arma con lo que hay en las carpetas
#   bash ~/juegos/publicar.sh --traer    -> antes hace git pull (solo avance rápido) en cada carpeta
# Fuentes (cada una es un clon o un worktree de su rama):
#   majo/       repo mmmanda/majo, rama claude/wiki-hetzner (la wiki y la portada)
#   chulin/     Juegos, rama ccr-0c5c1338-aqjm86  -> chulins-adventure/web
#   joshua/     Juegos, rama ccr-4a9b8917-8yx35y  -> joshua-2d/web
#   pancho/     Juegos, rama ccr-dd9e4f9e-6wlhop  -> pancho/web
#   jary/       Juegos, rama ccr-2215454e-jwei9k  -> juego
#   majomaker/  Juegos, rama ccr-a7eeaab2-6k86nu  -> majo-maker/web
#   novela/     Juegos, rama claude/novela-visual  -> novela/web (El Último Timbre)
#   ok/         Juegos, rama claude/new-session-351pqh, SOLO LECTURA: armar-ok.sh compila su web en ok-dist/
# Object Khaos: se publica y se lee, pero NUNCA se modifica su código ni se commitea en su rama.
# Su versión web sale de ok-dist con ok-web.js inyectado (sin multijugador ni pedidos a Firebase).
set -euo pipefail
cd /home/bondisar/juegos
exec 9>.publicar.candado; flock 9
if [ "${1:-}" = "--traer" ]; then
  for d in majo chulin joshua pancho jary majomaker novela; do (cd $d && git pull -q --ff-only) || echo "No se pudo traer $d (sigue con lo que hay)"; done
fi
N=publico.nuevo
rm -rf "$N"; mkdir -p "$N/jugar"
rsync -a --exclude .git --exclude README.md --exclude CLAUDE.md --exclude herramientas majo/ "$N/"
copiar() { rsync -a --delete "$1/" "$N/jugar/$2/"; }
copiar chulin/chulins-adventure/web chulins-adventure
copiar joshua/joshua-2d/web joshua-2d
copiar pancho/pancho/web pancho
copiar jary/juego jary
copiar majomaker/majo-maker/web majo-maker
copiar novela/novela/web el-ultimo-timbre
# Object Khaos: se compila solo si cambió su rama (con --traer, la trae antes)
bash majo/herramientas/armar-ok.sh $( [ "${1:-}" = "--traer" ] && echo --traer ) || echo "No se pudo armar Object Khaos (se publica la versión anterior si existe)"
if [ -d ok-dist ]; then
  rsync -a --delete --exclude .commit ok-dist/ "$N/jugar/object-khaos/"
  cp majo/herramientas/ok-web.js "$N/jugar/object-khaos/web-solo.js"
  sed -i "s#<script type=\"module\"#<script src=\"./web-solo.js\"></script>\n    <script type=\"module\"#" "$N/jugar/object-khaos/index.html"
fi
# en el celular: pantalla completa y horizontal al primer toque (jugar/pantalla.js viene del repo majo; este script está en majo/herramientas)
for f in "$N"/jugar/*/index.html; do
  grep -q 'pantalla.js' "$f" || sed -i 's#</body>#<script src="../pantalla.js"></script>\n</body>#' "$f"
done
# Pancho en la web: sin multijugador (window.WEB_BUILD lo esconde; el servidor pancho-red queda para Android)
f="$N/jugar/pancho/index.html"
grep -q WEB_BUILD "$f" || sed -i "0,/<script src=/s##<script>window.WEB_BUILD = true;</script>\n<script src=#" "$f"
chmod -R go+rX "$N"
rm -rf publico.viejo
[ -d publico ] && mv publico publico.viejo
mv "$N" publico
rm -rf publico.viejo
echo "Publicado: https://135.181.107.239/majo/"
