# majo
Web de MaJo Associations

Página estática (HTML + CSS, sin compilar), lista para GitHub Pages.

| Página | Archivo |
|---|---|
| Inicio: juegos, Colectucus, MaJo Associations y privacidad | `index.html` |
| Políticas de privacidad (para Google Play) | `privacidad/*.html` |
| Wiki | `wiki/index.html`, `wiki/chulins-adventure.html`, `wiki/joshua-2d.html`, `wiki/pancho.html`, `wiki/majo-maker.html`, `wiki/colectucus.html`, `wiki/majo-associations.html` |
| Íconos de los logros (de los juegos) | `img/logros/<juego>/` |
| Verificación de Google (Search Console) | `google2c00ac82537642a6.html` (no borrar) |
| Estilo compartido | `css/estilo.css` |
| Logo, íconos y gráficos de la tienda | `img/` |

## Apps y paquetes

| App | Paquete | Política de privacidad |
|---|---|---|
| Chulin's Adventure | `com.chulin.majo` | `privacidad/chulins-adventure.html` |
| Joshua 2D | `com.joshua2d.majo` | `privacidad/joshua-2d.html` |
| Pancho | `com.pancho.majo` | `privacidad/pancho.html` |
| MaJo Maker | `com.majomaker.majo` | `privacidad/majo-maker.html` |

## Publicar con GitHub Pages
1. En GitHub: **Settings → Pages**.
2. En *Source* elige **Deploy from a branch**, la rama `main` y la carpeta `/ (root)`.
3. La web queda en `https://mmmanda.github.io/majo/`. Los enlaces para Play Console son:
   - `https://mmmanda.github.io/majo/privacidad/chulins-adventure.html`
   - `https://mmmanda.github.io/majo/privacidad/joshua-2d.html`
   - `https://mmmanda.github.io/majo/privacidad/pancho.html`
   - `https://mmmanda.github.io/majo/privacidad/majo-maker.html`

## Copia en el servidor (Hetzner) con los juegos jugables

Desde el 2026-11-09 esta rama (`claude/wiki-hetzner`) se sirve también desde el servidor, **por ahora con la IP**:

- Inicio: `https://135.181.107.239/majo/` · Wiki: `https://135.181.107.239/majo/wiki/`
- Juegos para jugar en el navegador (también en el celular), con el botón **«▶ Jugar en la web»** de cada artículo:
  `https://135.181.107.239/majo/jugar/<juego>/` con `chulins-adventure`, `joshua-2d`, `pancho`, `jary` y `majo-maker` (MaJo Maker es exclusivo de la web).
- Los juegos **no se copian a este repo**: el servidor los toma de sus ramas del repo privado `mmmanda/Juegos` y arma todo junto con `herramientas/publicar.sh` (`--traer` hace `git pull` antes). `jugar/pantalla.js` pone pantalla completa y horizontal al primer toque en el celular.
- Cada juego guarda en su propia clave de `localStorage` (`chulins_adventure_v1`, `joshua2d_v1`, `pancho_v1`, `jary_ciudad_muerta_v1`, `majo_maker_v1`).
- GitHub Pages (`mmmanda.github.io/majo`, rama `claude/majo-associations-page-wiki-d7mf2u`) sigue igual: ahí están las políticas de privacidad que usa Play Console y la verificación de Google.
- Pruebas: `node herramientas/prueba-web.js` (cada juego carga, entra a un nivel y se mueve, como un celular).
