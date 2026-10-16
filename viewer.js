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
