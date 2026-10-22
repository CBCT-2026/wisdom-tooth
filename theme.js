// Light/dark toggle. Pages open in light mode; the choice lasts for this browser tab only,
// and the home page resets it, so each participant starts in light mode.
// The button text names the mode it switches to, so it has no aria-pressed.
const themeBtn = document.getElementById('theme');
const isDark = () => document.documentElement.dataset.theme === 'dark';
const showTheme = () => {
  const k = isDark() ? 'light' : 'dark';
  const en = themeBtn.dataset[k], ja = themeBtn.dataset[k + 'Ja'];
  themeBtn.textContent = en;
  if (ja) { const s = document.createElement('span'); s.lang = 'ja'; s.textContent = ja; themeBtn.append(' / ', s); }
};
themeBtn.addEventListener('click', () => {
  const t = isDark() ? 'light' : 'dark';
  document.documentElement.dataset.theme = t;
  try { sessionStorage.setItem('theme', t); } catch (e) {}
  showTheme();
});
showTheme();
