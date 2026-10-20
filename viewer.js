// Light/dark toggle. The label names the mode a tap switches to.
const themeBtn = document.getElementById('theme');
const isDark = () => (document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')) === 'dark';
const showTheme = () => { const d = isDark(); themeBtn.textContent = d ? themeBtn.dataset.light : themeBtn.dataset.dark; themeBtn.setAttribute('aria-pressed', d); };
themeBtn.addEventListener('click', () => {
  const t = isDark() ? 'light' : 'dark';
  document.documentElement.dataset.theme = t;
  try { localStorage.setItem('theme', t); } catch (e) {}
  showTheme();
});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', showTheme);
showTheme();

// Labels and preset views for the 3D model.
const mv = document.getElementById('mv');

mv.addEventListener('progress', e => {
  const bar = mv.querySelector('.progress');
  bar.querySelector('.progress-fill').style.width = (e.detail.totalProgress * 100) + '%';
  if (e.detail.totalProgress === 1) bar.classList.add('done');
});

// Tap a numbered dot to show its name on the model and its notes under the model.
const info = document.getElementById('info');
mv.querySelectorAll('.hotspot').forEach(h => h.addEventListener('click', () => {
  const open = !h.classList.contains('open');
  mv.querySelectorAll('.hotspot').forEach(o => o.classList.remove('open'));
  h.classList.toggle('open', open);
  info.hidden = !open;
  if (!open) return;
  const num = h.getAttribute('slot').split('-')[1];
  const items = [...h.querySelectorAll('.note > span')].map(s => '<li>' + s.innerHTML + '</li>').join('');
  info.innerHTML = '<h3><span class="num">' + num + '</span>' + h.querySelector('.label').innerHTML + '</h3><ul>' + items + '</ul>';
  info.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}));

// Tap the notes box to close it.
info.addEventListener('click', () => {
  info.hidden = true;
  mv.querySelectorAll('.hotspot').forEach(o => o.classList.remove('open'));
});

// Hide or show all the numbered dots.
const labels = document.getElementById('labels');
labels.addEventListener('click', () => {
  const off = mv.classList.toggle('labels-off');
  labels.setAttribute('aria-pressed', off);
  labels.textContent = off ? labels.dataset.off : labels.dataset.on;
  if (off) {
    mv.querySelectorAll('.hotspot').forEach(o => o.classList.remove('open'));
    info.hidden = true;
  }
});

// Preset camera views.
const viewButtons = document.querySelectorAll('[data-orbit]');
viewButtons.forEach(b => b.addEventListener('click', () => {
  mv.cameraOrbit = b.dataset.orbit;
  mv.cameraTarget = b.dataset.target || 'auto auto auto';
  viewButtons.forEach(o => o.setAttribute('aria-pressed', o === b));
}));

// Show a plain message in the viewer box if 3D cannot be shown, instead of an empty box.
function showProblem(text) {
  let box = mv.querySelector('.problem');
  if (!box) {
    box = document.createElement('div');
    box.className = 'problem';
    mv.appendChild(box);
  }
  box.textContent = text;
}
const msg = document.documentElement.lang === 'ja'
  ? { gl: 'このブラウザでは3D表示（WebGL）が使えません。ブラウザの設定で「ハードウェアアクセラレーション」をオンにするか、別のブラウザで開いてください。',
      load: '3Dモデルを読み込めませんでした。ページを再読み込みしてください。' }
  : { gl: 'This browser cannot show 3D (WebGL is off). Turn on hardware acceleration in the browser settings, or open the page in another browser.',
      load: 'The 3D model could not load. Please reload the page.' };
const canvas = document.createElement('canvas');
if (!(canvas.getContext('webgl2') || canvas.getContext('webgl'))) showProblem(msg.gl);
mv.addEventListener('error', e => showProblem(msg.load + ' (' + (e.detail && e.detail.type || 'error') + ')'));

// Extra AR buttons: open the same model turned to another side, in Quick Look (iPhone/iPad)
// or Scene Viewer (Android). They only show when the device can use AR.
const more = document.getElementById('ar-more');
const isIOS = document.createElement('a').relList.supports('ar');
const isAndroid = /android/i.test(navigator.userAgent);
mv.addEventListener('load', () => { if (mv.canActivateAR && (isIOS || isAndroid)) more.hidden = false; });
more.querySelectorAll('[data-ar]').forEach(b => b.addEventListener('click', () => {
  const base = new URL('../models/' + b.dataset.ar, location.href).href;
  if (isIOS) {
    const a = document.createElement('a');
    a.rel = 'ar';
    a.href = base + '.usdz';
    a.appendChild(document.createElement('img'));
    a.click();
  } else {
    const back = location.href.split('#')[0];
    location.href = 'intent://arvr.google.com/scene-viewer/1.0?file=' + encodeURIComponent(base + '.glb') +
      '&mode=ar_preferred#Intent;scheme=https;package=com.google.ar.core;action=android.intent.action.VIEW;' +
      'S.browser_fallback_url=' + encodeURIComponent(back) + ';end;';
  }
}));
