#!/bin/bash
# Arma la versión web de Object Khaos SIN tocar su código (lo llama publicar.sh).
# - ~/juegos/ok es un worktree SOLO DE LECTURA de la rama claude/new-session-351pqh (HEAD suelto, nunca se commitea ahí).
# - Compila client/dist con npm ci + vite build en una copia aparte (~/juegos/ok-build), así node_modules no ensucia el worktree.
# - Solo vuelve a compilar si cambió el commit. El resultado queda en ~/juegos/ok-dist.
#   --traer: antes trae la rama de GitHub.
set -euo pipefail
J=/home/bondisar/juegos
RAMA=origin/claude/new-session-351pqh
cd $J/repo
if [ "${1:-}" = "--traer" ]; then git fetch -q origin claude/new-session-351pqh || echo "No se pudo traer Object Khaos (sigue con lo que hay)"; fi
[ -d $J/ok ] || git worktree add -q --detach $J/ok $RAMA
git -C $J/ok checkout -q --detach $RAMA
C=$(git -C $J/ok rev-parse HEAD)
if [ -f $J/ok-dist/.commit ] && [ "$(cat $J/ok-dist/.commit)" = "$C" ]; then echo "Object Khaos ya armado ($C)"; exit 0; fi
echo "Armando Object Khaos $C ..."
mkdir -p $J/ok-build
rsync -a --delete --exclude node_modules --exclude client/dist --exclude client/android --exclude desktop $J/ok/object-show-online/ $J/ok-build/
cd $J/ok-build
# (sin .env: ningún VITE_* del servidor; el juego queda con su configuración por defecto)
npm ci --ignore-scripts --no-audit --no-fund --loglevel=error
(cd client && npx vite build --logLevel warn)
rm -rf $J/ok-dist.nuevo && cp -r client/dist $J/ok-dist.nuevo && echo "$C" > $J/ok-dist.nuevo/.commit
rm -rf $J/ok-dist && mv $J/ok-dist.nuevo $J/ok-dist
echo "Object Khaos armado en $J/ok-dist"
