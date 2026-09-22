(() => {
  'use strict';
  const catalog = document.querySelector('[data-catalog]');
  if (!catalog) return;

  const search = catalog.querySelector('#project-search');
  const controls = catalog.querySelector('.catalog-controls');
  const buttons = Array.from(catalog.querySelectorAll('[data-filter]'));
  const count = catalog.querySelector('.results-count');
  const empty = catalog.querySelector('.empty-state');
  const more = catalog.querySelector('.catalog-more');
  const showMore = catalog.querySelector('.show-more');
  const shownCount = catalog.querySelector('.shown-count');
  const clear = catalog.querySelector('.clear-search');
  const guide = catalog.querySelector('.category-guide-link');
  const fixedCategory = catalog.dataset.category;
  const pageSize = 12;
  let visibleLimit = pageSize;
  let category = fixedCategory || 'all';
  let timer;

  const normalize = text => text.normalize('NFKD').toLocaleLowerCase('he')
    .replace(/[\u0591-\u05c7]/g, '').replace(/['"\u05f3\u05f4]/g, '')
    .replace(/[^a-z0-9\u05d0-\u05ea\s]/g, ' ').replace(/\s+/g, ' ').trim();
  const synonyms = new Map([
    ['מוסיקה', 'מוזיקה'], ['לתמלל', 'תמלול'], ['לתמלול', 'תמלול'],
    ['ללמוד', 'לימוד'], ['להוריד', 'הורדה'], ['לגבות', 'גיבוי'],
    ['לסדר', 'סידור'], ['מבולגנת', 'סידור'], ['המוזיקה', 'מוזיקה'],
    ['אלפבוט', 'אלף']
  ]);
  const tokensFor = value => normalize(value).split(' ').filter(Boolean)
    .map(token => synonyms.get(token) || token);
  const projects = Array.from(catalog.querySelectorAll('[data-project]')).map(element => ({
    element,
    categories: element.dataset.categories.split(' '),
    search: normalize(element.dataset.search)
  }));
  const allowedCategories = new Set(['all', ...projects.flatMap(project => project.categories)]);
  const categories = new Map(Array.from(document.querySelectorAll('.intent-strip a')).map(link => [
    link.getAttribute('href').split('/').filter(Boolean).pop(),
    link.getAttribute('href')
  ]));

  function readLocation() {
    const parameters = new URL(window.location.href).searchParams;
    search.value = (parameters.get('q') || '').slice(0, 120);
    const requested = parameters.get('category') || 'all';
    category = fixedCategory || (allowedCategories.has(requested) ? requested : 'all');
    visibleLimit = pageSize;
  }

  function writeLocation(push = false) {
    const url = new URL(window.location.href);
    const query = search.value.trim();
    query ? url.searchParams.set('q', query) : url.searchParams.delete('q');
    if (!fixedCategory && category !== 'all') url.searchParams.set('category', category);
    else url.searchParams.delete('category');
    url.hash = 'projects';
    if (url.href !== window.location.href) {
      // Filtering still works if history changes are disabled by the host.
      try { window.history[push ? 'pushState' : 'replaceState']({}, '', url); } catch (_) { /* Optional shareable state. */ }
    }
  }

  function render() {
    const tokens = tokensFor(search.value);
    const matches = projects.filter(project =>
      (category === 'all' || project.categories.includes(category)) &&
      tokens.every(token => project.search.includes(token)));
    const limit = tokens.length || category !== 'all' ? matches.length : visibleLimit;
    const visible = new Set(matches.slice(0, limit));
    projects.forEach(project => { project.element.hidden = !visible.has(project); });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    const active = tokens.length > 0 || (!fixedCategory && category !== 'all');
    count.textContent = active
      ? (matches.length === 1 ? 'נמצא פרויקט אחד' : 'נמצאו ' + matches.length + ' פרויקטים')
      : matches.length + ' פרויקטים לגלות';
    empty.hidden = matches.length !== 0;
    clear.hidden = search.value.length === 0;
    more.hidden = matches.length <= limit;
    shownCount.textContent = 'מוצגים ' + visible.size + ' מתוך ' + matches.length;
    showMore.textContent = 'לכל ' + matches.length + ' הפרויקטים ↓';
    guide.hidden = !categories.has(category);
    if (!guide.hidden) guide.href = categories.get(category);
  }

  function searchChanged() {
    visibleLimit = pageSize;
    render();
    window.clearTimeout(timer);
    timer = window.setTimeout(() => writeLocation(), 200);
  }
  search.addEventListener('input', searchChanged);
  search.addEventListener('search', searchChanged);
  search.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      search.value = '';
      searchChanged();
    }
    if (event.key === 'Enter') {
      window.clearTimeout(timer);
      writeLocation();
      catalog.querySelector('[data-project]:not([hidden]) a')?.focus();
    }
  });
  clear.addEventListener('click', () => {
    search.value = '';
    searchChanged();
    search.focus();
  });
  buttons.forEach(button => button.addEventListener('click', () => {
    window.clearTimeout(timer);
    category = button.dataset.filter;
    visibleLimit = pageSize;
    writeLocation(true);
    render();
  }));
  showMore.addEventListener('click', () => {
    const next = projects.find(project => project.element.hidden);
    visibleLimit = projects.length;
    render();
    next?.element.querySelector('a')?.focus({ preventScroll: true });
  });
  catalog.querySelector('.reset-filters').addEventListener('click', () => {
    window.clearTimeout(timer);
    search.value = '';
    category = fixedCategory || 'all';
    visibleLimit = pageSize;
    writeLocation();
    render();
    search.focus();
  });
  window.addEventListener('popstate', () => {
    window.clearTimeout(timer);
    readLocation();
    render();
  });
  document.addEventListener('keydown', event => {
    if (event.key !== '/' || event.ctrlKey || event.metaKey || event.altKey ||
        event.target.closest('input,textarea,select,[contenteditable]')) return;
    event.preventDefault();
    search.focus();
    search.scrollIntoView({ block: 'center', behavior: 'instant' });
  });

  readLocation();
  render();
  controls.hidden = false;
  if (window.location.search && (search.value || category !== 'all') && window.location.hash === '#projects') {
    catalog.scrollIntoView({ block: 'start', behavior: 'instant' });
  }
})();
