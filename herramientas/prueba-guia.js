// Guía avanzada: una respuesta incorrecta no abre, las variantes correctas sí, se recuerda, y la respuesta no está
// en el HTML ni en el JS. Las respuestas se pasan por la variable RESPUESTAS (separadas por «|»), no se guardan.
const { chromium } = require('/home/bondisar/trabajo/bondisar-render/node_modules/playwright-core');
const EXE = '/home/bondisar/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux-arm64/chrome-headless-shell';
const URL = 'https://135.181.107.239/majo/wiki/el-ultimo-timbre-guia.html';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const buenas = (process.env.RESPUESTAS || '').split('|').filter(Boolean);
  const b = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox'] });
  let mal = 0; const log = (ok, t) => { if (!ok) mal++; console.log((ok ? 'OK  ' : 'MAL ') + t); };
  const prob = async (ctx, r) => { const p = await ctx.newPage(); await p.goto(URL); await sleep(300); await p.fill('#rGuia', r); await p.click('#fGuia button'); await sleep(2500);
    const st = await p.evaluate(() => ({ abierta: !document.getElementById('abierta').hidden, msg: document.getElementById('mGuia').textContent, finales: document.querySelectorAll('#abierta .final').length })); return [p, st]; };
  for (const r of ['Pancho', 'Joshua 2D', '']) { const ctx = await b.newContext(); const [, st] = await prob(ctx, r); log(!st.abierta && st.msg === 'Respuesta incorrecta', `incorrecta «${r}»: no abre (${st.msg})`); await ctx.close(); }
  for (const r of buenas) { const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true }); const [p, st] = await prob(ctx, r); log(st.abierta && st.finales === 35, `variante correcta (${r.length} letras): abre con ${st.finales} finales`);
    await p.reload(); await sleep(1500); const rec = await p.evaluate(() => !document.getElementById('abierta').hidden); log(rec, 'se recuerda al recargar'); await p.screenshot({ path: '/home/bondisar/tmp/juegos-capturas/guia-abierta.png' }); await ctx.close(); }
  // la respuesta no aparece en la página ni en sus scripts
  const ctx = await b.newContext(); const p = await ctx.newPage(); const textos = [];
  p.on('response', async (x) => { const t = x.headers()['content-type'] || ''; if (/html|javascript|json|css/.test(t)) textos.push(await x.text().catch(() => '')); });
  await p.goto(URL); await sleep(800);
  const todo = textos.join('\n').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  const pedazos = buenas.length ? buenas[0].toLowerCase().split(/\s+/).filter((w) => w.length >= 5 && !/^(huevo)$/.test(w)) : [];
  const fuga = buenas.some((r) => todo.includes(r.toLowerCase())) || pedazos.some((w) => todo.includes(w));
  log(!fuga && textos.length > 0, `la respuesta no está en el HTML ni en el JS (${textos.length} archivos revisados)`);
  await b.close(); console.log(mal ? mal + ' con problemas' : 'TODO BIEN'); process.exit(mal ? 1 : 0);
})();
