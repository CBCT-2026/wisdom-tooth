// Render the narrated video frames with Chromium and join them with the narration.
// Usage: node video/render.js en|ja [--fps 30] [--still 12.5]
// Needs Playwright, ffmpeg, a local copy of model-viewer 3.5.0 (MODEL_VIEWER_JS) and
// video/build/<lang>/timeline.json + narration.wav from video/tts.py.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const lang = process.argv[2];
const arg = (name, dflt) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : dflt; };
const fps = Number(arg('--fps', 30));
const still = arg('--still');
const MV = process.env.MODEL_VIEWER_JS;
const out = path.join(ROOT, 'video', 'build', lang);
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.glb': 'model/gltf-binary',
  '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.jpg': 'image/jpeg', '.png': 'image/png' };

const server = http.createServer((req, res) => {
  const file = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(ROOT) || !fs.existsSync(file)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = `http://localhost:${server.address().port}`;
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined,
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await page.route(/model-viewer\.min\.js$/, r => r.fulfill({ path: MV, contentType: 'text/javascript' }));
  await page.goto(`${base}/video/render.html`);
  const duration = await page.evaluate(u => window.init(u), `${base}/video/build/${lang}/timeline.json`);

  if (still !== undefined) {
    for (const t of still.split(',').map(Number)) {
      await page.evaluate(t => window.setFrame(t), t);
      await page.screenshot({ path: path.join(out, `still-${t}.png`) });
    }
    await browser.close(); server.close(); return;
  }

  const frames = path.join(out, 'frames');
  fs.rmSync(frames, { recursive: true, force: true });
  fs.mkdirSync(frames, { recursive: true });
  const n = Math.ceil(duration * fps);
  for (let f = 0; f < n; f++) {
    await page.evaluate(t => window.setFrame(t), f / fps);
    await page.screenshot({ path: path.join(frames, `${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
    if (f % 150 === 0) console.log(`${lang}: frame ${f}/${n}`);
  }
  await browser.close(); server.close();

  const mp4 = path.join(out, `narrated-video-${lang}.mp4`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', path.join(frames, '%05d.jpg'),
    '-i', path.join(out, 'narration.wav'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-pix_fmt', 'yuv420p',
    '-profile:v', 'high', '-level', '4.1', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', mp4]);
  // Copy the video, its subtitles and a poster frame to the web page folder.
  const pageDir = path.join(ROOT, 'video', lang);
  fs.copyFileSync(mp4, path.join(pageDir, `narrated-video-${lang}.mp4`));
  fs.copyFileSync(path.join(out, `narrated-video-${lang}.vtt`), path.join(pageDir, `narrated-video-${lang}.vtt`));
  fs.copyFileSync(path.join(frames, '00045.jpg'), path.join(pageDir, `poster-${lang}.jpg`));
  console.log(`${lang}: wrote ${mp4} and copied it to video/${lang}/`);
})();
