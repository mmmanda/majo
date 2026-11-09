// Juegos extra en la wiki + Object Khaos web sin multijugador (PC y celular) + Pancho web sin multijugador.
// Uso: node ~/juegos/majo/herramientas/prueba-v3.js
const { chromium } = require('/home/bondisar/trabajo/bondisar-render/node_modules/playwright-core');
const EXE = '/home/bondisar/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux-arm64/chrome-headless-shell';
const B = 'https://135.181.107.239/majo/', CAP = '/home/bondisar/tmp/juegos-capturas/';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  let mal = 0;
  const log = (ok, t) => { if (!ok) mal++; console.log((ok ? 'OK  ' : 'MAL ') + t); };
  // ---- wiki en celular ----
  const cel = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, locale: 'es-AR' });
  for (const a of ['index', 'el-ultimo-timbre', 'object-khaos']) {
    const p = await cel.newPage(); const e = [];
    p.on('response', (x) => { if (x.status() >= 400 && x.url().includes('/majo/')) e.push(x.status() + ' ' + x.url()); });
    await p.goto(B + 'wiki/' + a + '.html'); await sleep(500);
    const w = await p.evaluate(() => document.documentElement.scrollWidth);
    await p.screenshot({ path: CAP + 'v3-wiki-' + a + '.png', fullPage: true });
    log(w <= 390 && !e.length, `wiki/${a} en celular: ancho ${w}/390 ${e.join(' ')}`);
    await p.close();
  }
  {
    const p = await cel.newPage(); await p.goto(B + 'wiki/'); await sleep(300);
    const extra = await p.$$eval('#extra .tarjeta h3', (x) => x.map((h) => h.textContent.trim()));
    const botones = await p.$$eval('#extra a.jugar', (x) => x.map((a) => a.href));
    let ok = extra.length === 4;
    for (const h of botones) { const r = await p.request.get(h); if (r.status() !== 200) ok = false; }
    const menu = await p.$$eval('nav a', (x) => x.map((a) => a.textContent.trim()));
    log(ok && menu.includes('Juegos extra:'), `wiki: «Juegos extra» = ${extra.join(', ')}; botones OK; menú con «Juegos extra»`);
    await p.goto(B); await sleep(300);
    const home = await p.$$eval('#extra .tarjeta h3', (x) => x.map((h) => h.textContent.trim()));
    log(home.length === 4, `portada del sitio: «Juegos extra» = ${home.join(', ')}`);
    await p.close();
  }
  // ---- Object Khaos web: PC y celular ----
  for (const [nombre, opc] of [['PC', { viewport: { width: 1280, height: 720 } }], ['celular', { viewport: { width: 844, height: 390 }, isMobile: true, hasTouch: true }]]) {
    const ctx = await b.newContext(Object.assign({ locale: 'es-AR' }, opc));
    const p = await ctx.newPage(); const afuera = [], errs = [];
    p.on('request', (r) => { const u = r.url(); if (!u.startsWith('https://135.181.107.239/') && !u.startsWith('data:') && !u.startsWith('blob:')) afuera.push(u); });
    p.on('pageerror', (e) => errs.push(e.message));
    await p.goto(B + 'jugar/object-khaos/'); await sleep(1500);
    if (opc.isMobile) await p.touchscreen.tap(400, 200); else await p.mouse.click(640, 360);
    await sleep(1500);
    const visibles = await p.$$eval('button', (x) => x.filter((b) => b.offsetParent !== null).map((b) => b.textContent.trim()));
    const prohibidos = visibles.filter((t) => /Amigos|Rankings|Tienda|Ingresar|Crear cuenta|invitado/.test(t));
    await p.screenshot({ path: CAP + `v3-ok-menu-${nombre}.png` });
    // jugar: Jugar → Party con bots
    const jugar = await p.$('button:has-text("Jugar")'); if (jugar) await jugar.click(); await sleep(800);
    const party = await p.$('button:has-text("Party con bots")'); if (party) await party.click(); await sleep(6000);
    await p.screenshot({ path: CAP + `v3-ok-partida-${nombre}.png` });
    const enJuego = await p.evaluate(() => !document.querySelector('.menu-grid'));
    log(!prohibidos.length && !afuera.length && enJuego, `Object Khaos ${nombre}: menú sin conexión (${visibles.slice(0, 8).join(' · ')}), ocultos: ${prohibidos.length ? 'NO ' + prohibidos : 'sí'}, pedidos fuera del servidor: ${afuera.length}${afuera.length ? ' ' + afuera.slice(0, 3) : ''}, partida con bots: ${enJuego}${errs.length ? ' errores: ' + errs.slice(0, 2) : ''}`);
    await ctx.close();
  }
  // ---- Pancho web: sigue sin multijugador ----
  {
    const ctx = await b.newContext({ viewport: { width: 844, height: 390 } }); const p = await ctx.newPage();
    await p.goto(B + 'jugar/pancho/'); await sleep(1200);
    const r = await p.evaluate(() => { setScreen('modes'); Online.open(); return { web: !!window.WEB_BUILD, screen }; });
    log(r.web && r.screen === 'modes', 'Pancho web: sin multijugador (WEB_BUILD, Online.open no hace nada)');
    await ctx.close();
  }
  await b.close();
  console.log(mal ? mal + ' con problemas' : 'TODO BIEN'); process.exit(mal ? 1 : 0);
})();
