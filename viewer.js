// Light/dark toggle. Pages open in light mode; the choice lasts for this browser tab only,
// so the next participant on the same device starts in light mode once the tab is closed.
const themeBtn = document.getElementById('theme');
const isDark = () => document.documentElement.dataset.theme === 'dark';
const showTheme = () => { const d = isDark(); themeBtn.textContent = d ? themeBtn.dataset.light : themeBtn.dataset.dark; themeBtn.setAttribute('aria-pressed', d); };
themeBtn.addEventListener('click', () => {
  const t = isDark() ? 'light' : 'dark';
  document.documentElement.dataset.theme = t;
  try { sessionStorage.setItem('theme', t); } catch (e) {}
  showTheme();
});
showTheme();

// Labels and preset views for the 3D model.
const mv = document.getElementById('mv');

mv.addEventListener('progress', e => {
  const bar = mv.querySelector('.progress');
  bar.querySelector('.progress-fill').style.width = (e.detail.totalProgress * 100) + '%';
  if (e.detail.totalProgress === 1) bar.classList.add('done');
});

// Hide or show the labels on the model.
const labels = document.getElementById('labels');
labels.addEventListener('click', () => {
  const off = mv.classList.toggle('labels-off');
  labels.setAttribute('aria-pressed', off);
  labels.textContent = off ? labels.dataset.off : labels.dataset.on;
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
mv.addEventListener('error', e => {
  console.warn('model-viewer error', e.detail && e.detail.type);
  showProblem(msg.load);
});
// If the 3D viewer script itself does not start (blocked or offline), say so instead of an empty box.
setTimeout(() => {
  if (customElements.get('model-viewer')) return;
  showProblem(msg.load);
  document.querySelector('.controls').hidden = true;
}, 10000);

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

// A tap on a source number opens the closed list of sources first.
document.querySelectorAll('.cite a').forEach(a => a.addEventListener('click', () => {
  const d = document.querySelector('.refs details');
  if (d) d.open = true;
}));
