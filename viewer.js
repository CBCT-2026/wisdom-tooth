// Labels, preset views and the tooth-removal animation for the 3D model.
const mv = document.getElementById('mv');

mv.addEventListener('progress', e => {
  const bar = mv.querySelector('.progress');
  bar.querySelector('.progress-fill').style.width = (e.detail.totalProgress * 100) + '%';
  if (e.detail.totalProgress === 1) bar.classList.add('done');
});

// Tap a numbered dot to show or hide its label.
mv.querySelectorAll('.hotspot').forEach(h => h.addEventListener('click', () => {
  const open = !h.classList.contains('open');
  mv.querySelectorAll('.hotspot').forEach(o => o.classList.remove('open'));
  h.classList.toggle('open', open);
}));

// Preset camera views.
const viewButtons = document.querySelectorAll('[data-orbit]');
viewButtons.forEach(b => b.addEventListener('click', () => {
  mv.cameraOrbit = b.dataset.orbit;
  mv.cameraTarget = b.dataset.target || 'auto auto auto';
  viewButtons.forEach(o => o.setAttribute('aria-pressed', o === b));
}));

// Play the extraction once, then return to the start.
const play = document.getElementById('play');
function stop() {
  mv.pause();
  mv.currentTime = 0;
  mv.classList.remove('playing');
  play.disabled = false;
}
play.addEventListener('click', () => {
  mv.animationName = 'extraction';
  mv.currentTime = 0;
  mv.classList.add('playing');
  play.disabled = true;
  mv.play();
  let last = 0;
  const watch = () => {
    const t = mv.currentTime;
    if (t < last || t >= mv.duration - 0.05) return stop();
    last = t;
    requestAnimationFrame(watch);
  };
  requestAnimationFrame(watch);
});

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
