// Prueba de la versión web de cada juego, como un celular en horizontal (táctil):
// carga sin errores, entra a un nivel, el personaje se mueve, y cada juego guarda con su propia clave.
// Uso: node ~/juegos/herramientas/prueba-web.js [base]   (por defecto https://135.181.107.239/majo/)
const { chromium } = require('/home/bondisar/trabajo/bondisar-render/node_modules/playwright-core');
const BASE = process.argv[2] || 'https://135.181.107.239/majo/';
const EXE = '/home/bondisar/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux-arm64/chrome-headless-shell';
const CAP = '/home/bondisar/tmp/juegos-capturas/';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// mantener una tecla apretada
async function tecla(p, k, ms) { await p.keyboard.down(k); await sleep(ms); await p.keyboard.up(k); }

const JUEGOS = {
  'chulins-adventure': { q: '?level=1-1', x: () => G.player.x, skip: () => { if (G.dialog) Input.just.confirm = true; } },
  'joshua-2d': { q: '?level=1-1', x: () => G.player.x, skip: () => { if (G.dialog) Input.just.confirm = true; } },
  'pancho': { q: '?level=1', x: () => G.player.x, skip: () => { if (screen === 'name') { ScreenName.el.value = 'Prueba'; ScreenName.submit(); } if (G.dialog) Input.just.confirm = true; } },
  'jary': {
    q: '', x: () => __G.world.player.x, skip: () => {},
    entrar: async (p) => {
      await p.touchscreen.tap(400, 30); await sleep(600);
      const box = await p.locator('canvas').first().boundingBox();
      const at = (x, y) => [box.x + x * box.width / 384, box.y + y * box.height / 216];
      await p.touchscreen.tap(...at(192, 90)); await sleep(200);
      await p.touchscreen.tap(...at(192, 90)); await sleep(400);
      await p.touchscreen.tap(...at(192, 180)); await sleep(200);
      const press = async (i) => { await p.evaluate((i) => INPUT.nativePad(i, true), i); await sleep(80); await p.evaluate((i) => INPUT.nativePad(i, false), i); await sleep(150); };
      await press(1); await press(0); await sleep(1900);
    },
  },
  'majo-maker': {
    q: '', x: () => Play.A.G.player.x, skip: () => { const G = Play.A.G; if (G.dialog) Play.A.Input.just.confirm = true; },
    entrar: async (p) => { await sleep(1500); await p.evaluate(() => { Store.settings.seen.help = true; Modals.closeAll(); Play.start(EXAMPLES()[2], 'play'); }); await sleep(800); },
  },
};

(async () => {
  const b = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, locale: 'es-AR' });
  let mal = 0;
  for (const [slug, J] of Object.entries(JUEGOS)) {
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', (e) => errs.push(e.message));
    p.on('response', (r) => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
    // primero la portada del juego (como entra alguien desde la wiki)
    await p.goto(BASE + 'jugar/' + slug + '/'); await sleep(1500);
    await p.screenshot({ path: CAP + 'web-' + slug + '-titulo.png' });
    if (J.entrar) await J.entrar(p);
    else { await p.goto(BASE + 'jugar/' + slug + '/' + J.q); await sleep(1500); }
    for (let i = 0; i < 120; i++) { await p.evaluate(J.skip).catch(() => {}); await sleep(30); }
    let x0 = null, x1 = null;
    try {
      x0 = await p.evaluate(J.x);
      await tecla(p, 'ArrowRight', 1200);
      for (let i = 0; i < 30; i++) { await p.evaluate(J.skip).catch(() => {}); await sleep(20); }
      x1 = await p.evaluate(J.x);
    } catch (e) { errs.push('no se pudo leer la posición: ' + e.message); }
    await p.screenshot({ path: CAP + 'web-' + slug + '-juego.png' });
    const claves = await p.evaluate(() => Object.keys(localStorage));
    const ok = !errs.length && x0 != null && x1 > x0 + 20;
    if (!ok) mal++;
    console.log(`${ok ? 'OK ' : 'MAL'} ${slug}: se movió ${x0 == null ? '?' : Math.round(x1 - x0)} px · claves guardadas: ${claves.join(', ') || '(ninguna)'}${errs.length ? '\n    ' + errs.join('\n    ') : ''}`);
    await p.close();
  }
  // la wiki: cada botón «Jugar en la web» lleva a un juego que existe
  const p = await ctx.newPage();
  await p.goto(BASE + 'wiki/'); await sleep(500);
  await p.screenshot({ path: CAP + 'wiki-inicio.png', fullPage: true });
  const enlaces = await p.evaluate(() => [...document.querySelectorAll('a.jugar')].map((a) => a.href));
  for (const art of ['chulins-adventure', 'joshua-2d', 'pancho', 'jary', 'majo-maker']) {
    await p.goto(BASE + 'wiki/' + art + '.html');
    const h = await p.evaluate(() => { const a = document.querySelector('.jugar-web a'); return a && a.href; });
    enlaces.push(h);
  }
  await p.screenshot({ path: CAP + 'wiki-majo-maker.png' });
  for (const h of enlaces) { const r = await p.request.get(h); if (r.status() !== 200) { mal++; console.log('MAL enlace', h, r.status()); } }
  console.log('wiki: ' + enlaces.length + ' botones «Jugar en la web» revisados');
  const ancho = await p.evaluate(() => document.documentElement.scrollWidth);
  console.log('wiki en celular: ancho de la página', ancho, '(pantalla 844)');
  await b.close();
  console.log(mal ? `${mal} con problemas` : 'TODO BIEN');
  process.exit(mal ? 1 : 0);
})().catch((e) => { console.error('FALLÓ:', e.message); process.exit(1); });
