// Pancho web sin multijugador + artículos nuevos de la wiki en celular
const { chromium } = require('/home/bondisar/trabajo/bondisar-render/node_modules/playwright-core');
const EXE = '/home/bondisar/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux-arm64/chrome-headless-shell';
const B = 'https://135.181.107.239/majo/', CAP = '/home/bondisar/tmp/juegos-capturas/';
(async () => {
  const b = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  const ctx = await b.newContext({ viewport: { width: 844, height: 390 }, isMobile: true, hasTouch: true, locale: 'es-AR' });
  let mal = 0;
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
  const red = []; p.on('request', (r) => { if (/pancho-red/.test(r.url())) red.push(r.url()); });
  await p.goto(B + 'jugar/pancho/'); await p.waitForTimeout(1500);
  const r = await p.evaluate(async () => {
    Save.data.done = Save.data.done || {}; setScreen('modes'); await new Promise((r) => setTimeout(r, 400));
    Online.open(); await new Promise((r) => setTimeout(r, 300));
    return { web: !!window.WEB_BUILD, screen };
  });
  await p.screenshot({ path: CAP + 'v2-pancho-modos.png' });
  // tocar donde antes estaba el botón de Multijugador (mitad derecha de la fila de abajo)
  await p.touchscreen.tap(640, 300); await p.waitForTimeout(400);
  const tras = await p.evaluate(() => screen);
  const ok = r.web && r.screen === 'modes' && tras !== 'online' && !red.length && !errs.length;
  if (!ok) mal++;
  console.log(`${ok ? 'OK ' : 'MAL'} Pancho web: WEB_BUILD=${r.web}, tras Online.open() sigue en «${r.screen}», tras tocar: «${tras}», pedidos a pancho-red: ${red.length}${errs.length ? ' errores: ' + errs.join(' | ') : ''}`);
  for (const a of ['object-khaos', 'colectucus', 'jary', 'index']) {
    const q = await ctx.newPage(); const e2 = []; q.on('pageerror', (e) => e2.push(e.message));
    q.on('response', (x) => { if (x.status() >= 400 && x.url().includes('/majo/')) e2.push(x.status() + ' ' + x.url()); });
    await q.goto(B + 'wiki/' + a + '.html'); await q.waitForTimeout(600);
    await q.setViewportSize({ width: 390, height: 844 }); await q.waitForTimeout(300);
    const info = await q.evaluate(() => ({ w: document.documentElement.scrollWidth, t: document.body.innerText }));
    await q.screenshot({ path: CAP + 'v2-wiki-' + a + '.png', fullPage: true });
    const prohib = ['Red Bus', 'SUBE', 'Netlify', 'Gómez', 'Sansone', '135.181', 'USD'].filter((x) => info.t.includes(x));
    const okA = info.w <= 390 && !e2.length && !prohib.length && !(a === 'jary' && /APK|Android/.test(info.t.split('JARY: Ciudad Muerta').slice(1).join('')));
    if (!okA) mal++;
    console.log(`${okA ? 'OK ' : 'MAL'} wiki/${a}: ancho ${info.w}/390${prohib.length ? ' prohibidos: ' + prohib : ''}${e2.length ? ' ' + e2.join(' | ') : ''}`);
    await q.close();
  }
  await b.close();
  console.log(mal ? mal + ' con problemas' : 'TODO BIEN'); process.exit(mal ? 1 : 0);
})();
