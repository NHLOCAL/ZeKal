(() => {
  'use strict';
  const themeButton = document.querySelector('.theme-toggle');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  const isDark = () => document.documentElement.dataset.theme
    ? document.documentElement.dataset.theme === 'dark' : systemTheme.matches;
  const updateThemeButton = () => {
    if (!themeButton) return;
    themeButton.hidden = false;
    themeButton.setAttribute('aria-pressed', String(isDark()));
    themeButton.setAttribute('aria-label', isDark() ? 'מעבר למצב בהיר' : 'מעבר למצב כהה');
    document.querySelector('meta[name="theme-color"]').content = isDark() ? '#132422' : '#f7f8f2';
  };
  themeButton?.addEventListener('click', () => {
    const theme = isDark() ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('zekal-theme', theme); } catch (_) { /* Preference is optional. */ }
    updateThemeButton();
  });
  systemTheme.addEventListener('change', updateThemeButton);
  updateThemeButton();

  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.main-nav');
  function closeMenu() {
    navigation?.classList.remove('is-open');
    menuButton?.setAttribute('aria-expanded', 'false');
    menuButton?.setAttribute('aria-label', 'פתיחת תפריט');
  }
  if (menuButton && navigation) {
    menuButton.hidden = false;
    menuButton.addEventListener('click', () => {
      const open = navigation.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.setAttribute('aria-label', open ? 'סגירת תפריט' : 'פתיחת תפריט');
    });
    navigation.addEventListener('click', event => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('click', event => {
      if (!event.target.closest('.site-header')) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        menuButton.focus();
      }
    });
  }

  // Preserve horizontal table scrolling and English pronunciation on learning pages.
  document.querySelectorAll('.reading-content table').forEach((table, index) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-scroll';
    wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region');
    wrapper.setAttribute('aria-label', 'טבלת מושגים ' + (index + 1) + ', אפשר לגלול אופקית');
    table.before(wrapper);
    wrapper.append(table);
    if (!('speechSynthesis' in window)) return;
    const headers = Array.from(table.querySelectorAll('thead th'));
    const column = headers.findIndex(header => /אנגלית|English/i.test(header.textContent));
    if (column < 0) return;
    table.querySelectorAll('tbody tr').forEach(row => {
      const cell = row.cells[column];
      const text = cell?.textContent.trim();
      if (!text) return;
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'speak-button';
      button.textContent = '♪';
      button.setAttribute('aria-label', 'הקראת ' + text);
      button.title = 'הקראת ' + text;
      button.addEventListener('click', () => {
        window.speechSynthesis.cancel();
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'en-US';
        speech.rate = 0.9;
        window.speechSynthesis.speak(speech);
      });
      cell.append(button);
    });
  });
})();
