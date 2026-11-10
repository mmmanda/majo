const { chromium } = require('/home/bondisar/trabajo/bondisar-render/node_modules/playwright-core');
const EXE = '/home/bondisar/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux-arm64/chrome-headless-shell';
const URL = 'https://135.181.107.239/majo/wiki/el-ultimo-timbre-guia.html', CAP = '/home/bondisar/tmp/juegos-capturas/';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  let mal = 0;
  for (const tema of ['dark', 'light']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, colorScheme: tema });
    const p = await ctx.newPage(); await p.goto(URL); await sleep(500);
    await p.screenshot({ path: CAP + `guia-${tema}-bloqueada.png` });
    await p.fill('#rGuia', process.env.R); await p.click('#fGuia button'); await sleep(2500);
    await p.evaluate(() => { const d = document.querySelector('#abierta details'); if (d) d.open = true; document.querySelector('#abierta .final').scrollIntoView(); });
    await sleep(200); await p.screenshot({ path: CAP + `guia-${tema}-abierta.png` });
    await p.reload(); await sleep(1500);
    await p.evaluate(() => { const f = document.querySelector('#abierta .final'); if (f) f.scrollIntoView(); });
    await p.screenshot({ path: CAP + `guia-${tema}-recargada.png` });
    // contraste: color del texto de un final contra su fondo
    const c = await p.evaluate(() => { const f = document.querySelector('#abierta .final'); const cs = getComputedStyle(f); const lum = (s) => { const m = s.match(/\d+(\.\d+)?/g).map(Number); return (0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2]) / 255; }; return { fondo: cs.backgroundColor, texto: cs.color, dif: Math.abs(lum(cs.backgroundColor) - lum(cs.color)), cerrada: document.getElementById('cerrada').hidden }; });
    const ok = c.dif > 0.5 && c.cerrada;
    if (!ok) mal++;
    console.log(`${ok ? 'OK ' : 'MAL'} tema ${tema}: texto ${c.texto} sobre ${c.fondo} (contraste ${c.dif.toFixed(2)}), candado oculto: ${c.cerrada}`);
    await ctx.close();
  }
  await b.close(); console.log(mal ? 'con problemas' : 'TODO BIEN'); process.exit(mal ? 1 : 0);
})();
