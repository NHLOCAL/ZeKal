// Apply the saved preference before paint. Storage is optional.
(() => {
  let theme;
  try { theme = localStorage.getItem('zekal-theme'); } catch (_) { /* Private browsing. */ }
  if (theme === 'dark' || theme === 'light') document.documentElement.dataset.theme = theme;
  document.documentElement.classList.add('js');
})();
