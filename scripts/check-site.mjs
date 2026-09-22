#!/usr/bin/env node
import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';

const ORIGIN = 'https://ze-kal.top';
const CATEGORY_ROUTES = ['ai', 'music', 'computer', 'learning'].map(
  (category) => `/projects/${category}/`,
);
// Keep the existing learning URLs covered even if a page disappears from a build.
const TOPIC_NAMES = [
  'advanced-words-1', 'advanced-words-2', 'artificial-intelligence',
  'basic-words-1', 'basic-words-2', 'cloud-computing', 'computers',
  'cybersecurity', 'databases', 'hardware-components', 'networking',
  'operating-systems', 'programming-languages', 'web-development',
];
const REQUIRED_ROUTES = [
  '/', ...CATEGORY_ROUTES, '/learn/', '/youtube-channel.html', '/404.html',
  ...TOPIC_NAMES.map((name) => `/topics/${name}.html`),
];

function decodeEntities(value) {
  const named = { amp: '&', quot: '"', apos: "'", lt: '<', gt: '>', nbsp: '\u00a0' };
  return value.replace(/&(#x[\da-f]+|#\d+|amp|quot|apos|lt|gt|nbsp);/gi, (entity, key) => {
    if (!key.startsWith('#')) return named[key.toLowerCase()] ?? entity;
    const hexadecimal = key[1].toLowerCase() === 'x';
    const point = Number.parseInt(key.slice(hexadecimal ? 2 : 1), hexadecimal ? 16 : 10);
    return point <= 0x10ffff ? String.fromCodePoint(point) : entity;
  });
}

function attributes(source) {
  const result = new Map();
  const pattern = /([^\s=\/"'<>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  for (const match of source.matchAll(pattern)) {
    result.set(match[1].toLowerCase(), decodeEntities(match[2] ?? match[3] ?? match[4] ?? ''));
  }
  return result;
}

function parseDocument(html) {
  const withoutComments = html.replace(/<!--[\s\S]*?-->/g, '');
  const structuredData = [];
  for (const match of withoutComments.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)) {
    const type = attributes(match[1]).get('type')?.split(';')[0].trim().toLowerCase();
    if (type === 'application/ld+json') structuredData.push(match[2]);
  }
  // Inspect HTML attributes, not markup-looking strings in JavaScript or CSS url() values.
  const markup = withoutComments.replace(
    /<(script|style)\b([^>]*)>[\s\S]*?<\/\1\s*>/gi,
    '<$1$2></$1>',
  );
  const tags = [...markup.matchAll(/<([a-z][\w:-]*)\b((?:[^"'<>]|"[^"]*"|'[^']*')*)>/gi)]
    .map((match) => ({ name: match[1].toLowerCase(), attrs: attributes(match[2]) }));
  const ids = new Map();
  const anchors = new Set();
  for (const tag of tags) {
    if (tag.attrs.has('id')) {
      const id = tag.attrs.get('id');
      ids.set(id, (ids.get(id) ?? 0) + 1);
      anchors.add(id);
    }
    if (tag.name === 'a' && tag.attrs.has('name')) anchors.add(tag.attrs.get('name'));
  }
  return { html: withoutComments, tags, ids, anchors, structuredData };
}

function* jsonObjects(value) {
  if (value === null || typeof value !== 'object') return;
  if (!Array.isArray(value)) yield value;
  for (const child of Object.values(value)) yield* jsonObjects(child);
}

async function fileInfo(file) {
  try {
    return await stat(file);
  } catch (error) {
    if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return null;
    throw error;
  }
}

async function checkSite(siteRoot) {
  const errors = new Set();
  const counts = { required: REQUIRED_ROUTES.length, pages: 0, jsonLd: 0, references: 0, cards: 0, visibleCards: 0, websites: 0, sitemap: 0 };
  const fail = (location, message) => errors.add(`${location}: ${message}`);
  const documentCache = new Map();
  const resourceCache = new Map();

  async function resourceFor(urlPath) {
    if (resourceCache.has(urlPath)) return resourceCache.get(urlPath);
    const decoded = decodeURIComponent(urlPath);
    let target = path.resolve(siteRoot, `.${decoded}`);
    const relative = path.relative(siteRoot, target);
    if (relative === '..' || relative.startsWith(`..${path.sep}`) || path.isAbsolute(relative)) {
      throw new Error('local path escapes the site directory');
    }
    let info = await fileInfo(target);
    if (info?.isDirectory()) {
      target = path.join(target, 'index.html');
      info = await fileInfo(target);
    }
    const resolved = info?.isFile() ? target : null;
    resourceCache.set(urlPath, resolved);
    return resolved;
  }

  async function documentFor(file) {
    if (!documentCache.has(file)) {
      documentCache.set(file, parseDocument(await readFile(file, 'utf8')));
    }
    return documentCache.get(file);
  }

  async function checkReference(route, value, attribute) {
    if (!value.trim()) {
      if (attribute === 'src') fail(route, 'empty src attribute');
      return;
    }
    let url;
    try {
      url = new URL(value, `${ORIGIN}${route}`);
    } catch {
      fail(route, `invalid ${attribute} URL ${JSON.stringify(value)}`);
      return;
    }
    // External URLs, including font providers, and non-HTTP schemes need no network checks.
    if (!['https:', 'http:'].includes(url.protocol) || url.hostname !== 'ze-kal.top') return;
    counts.references += 1;
    let target;
    try {
      target = await resourceFor(url.pathname);
    } catch (error) {
      fail(route, `${attribute} ${JSON.stringify(value)}: ${error.message}`);
      return;
    }
    if (!target) {
      fail(route, `missing local target for ${attribute} ${JSON.stringify(value)}`);
      return;
    }
    if (!/\.html?$/i.test(target) || !url.hash) return;
    let fragment;
    try {
      // Text fragments and a bare # do not require a corresponding element ID.
      fragment = decodeURIComponent(url.hash.slice(1).split(':~:text=')[0]);
    } catch {
      fail(route, `invalid fragment in ${JSON.stringify(value)}`);
      return;
    }
    if (!fragment || fragment.toLowerCase() === 'top') return;
    const destination = await documentFor(target);
    if (!destination.anchors.has(fragment)) {
      fail(route, `missing fragment target ${JSON.stringify(value)}`);
    }
  }

  const routes = new Set(REQUIRED_ROUTES);
  const topicDirectory = path.join(siteRoot, 'topics');
  if ((await fileInfo(topicDirectory))?.isDirectory()) {
    for (const entry of await readdir(topicDirectory, { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith('.html')) routes.add(`/topics/${entry.name}`);
    }
  }

  for (const route of routes) {
    const file = await resourceFor(route);
    if (!file) {
      fail(route, 'required HTML page is missing');
      continue;
    }
    counts.pages += 1;
    const document = await documentFor(file);
    const { tags, ids, structuredData } = document;
    const headingCount = tags.filter((tag) => tag.name === 'h1').length;
    if (headingCount !== 1) fail(route, `expected one H1, found ${headingCount}`);

    // SVG title elements label icons and are not document titles.
    const head = document.html.match(/<head\b[^>]*>([\s\S]*?)<\/head\s*>/i)?.[1] ?? '';
    const titles = parseDocument(head).tags.filter((tag) => tag.name === 'title');
    if (titles.length !== 1) fail(route, `expected one title, found ${titles.length}`);
    const titleText = head.match(/<title\b[^>]*>([\s\S]*?)<\/title\s*>/i)?.[1];
    if (!titleText || !decodeEntities(titleText).trim()) fail(route, 'title is empty or unclosed');

    const descriptions = tags.filter((tag) => tag.name === 'meta'
      && tag.attrs.get('name')?.toLowerCase() === 'description');
    if (descriptions.length !== 1) fail(route, `expected one meta description, found ${descriptions.length}`);
    if (descriptions.some((tag) => !tag.attrs.get('content')?.trim())) fail(route, 'meta description is empty');

    const canonicals = tags.filter((tag) => tag.name === 'link'
      && tag.attrs.get('rel')?.toLowerCase().split(/\s+/).includes('canonical'));
    if (canonicals.length !== 1) fail(route, `expected one canonical link, found ${canonicals.length}`);
    for (const canonical of canonicals) {
      const href = canonical.attrs.get('href') ?? '';
      try {
        const url = new URL(href);
        if (url.origin !== ORIGIN || /[?#]/.test(href)) {
          fail(route, `canonical must use ${ORIGIN} without query or fragment`);
        } else if (url.href !== new URL(route, ORIGIN).href) {
          fail(route, `canonical points to ${JSON.stringify(href)} instead of this page`);
        }
      } catch {
        fail(route, 'canonical is not an absolute URL');
      }
    }

    for (const [id, occurrences] of ids) {
      if (occurrences > 1) fail(route, `duplicate id ${JSON.stringify(id)} (${occurrences} occurrences)`);
    }
    if (!structuredData.length) fail(route, 'no JSON-LD block found');
    const schemaObjects = [];
    for (const [index, source] of structuredData.entries()) {
      counts.jsonLd += 1;
      try {
        const data = JSON.parse(source);
        if (data === null || typeof data !== 'object') throw new Error('expected an object or array');
        schemaObjects.push(...jsonObjects(data));
      } catch (error) {
        fail(route, `JSON-LD block ${index + 1} is invalid: ${error.message}`);
      }
    }
    if (route === '/') {
      const cards = tags.filter((tag) => tag.attrs.has('data-project'));
      counts.cards = cards.length;
      counts.visibleCards = cards.filter((card) => !card.attrs.has('hidden')).length;
      if (counts.cards < 34) fail(route, `expected at least 34 data-project cards, found ${counts.cards}`);
      if (counts.visibleCards !== counts.cards) {
        fail(route, `${counts.cards - counts.visibleCards} project card(s) have hidden in raw HTML; the no-JS catalog must expose all cards`);
      }
      const websites = schemaObjects.filter((item) => [].concat(item['@type'] ?? []).some(
        (type) => type === 'WebSite' || /^https?:\/\/schema\.org\/WebSite$/.test(type),
      ));
      counts.websites = websites.length;
      if (websites.length !== 1) fail(route, `expected one WebSite JSON-LD entity, found ${websites.length}`);
      if (websites.some((website) => website.name !== 'זה קל!')) fail(route, 'WebSite name must be "זה קל!"');
      for (const item of schemaObjects) {
        const logo = typeof item.logo === 'string' ? item.logo : item.logo?.url ?? item.logo?.contentUrl;
        if (typeof logo !== 'string') continue;
        if (logo !== `${ORIGIN}/assets/images/brand-mark.svg`) fail(route, 'JSON-LD logo must point to the current canonical brand mark');
        await checkReference(route, logo, 'JSON-LD logo');
      }
    }
    for (const tag of tags) {
      for (const attribute of ['href', 'src']) {
        if (tag.attrs.has(attribute)) await checkReference(route, tag.attrs.get(attribute), attribute);
      }
      if (tag.name === 'meta') {
        const imageMeta = [tag.attrs.get('property'), tag.attrs.get('name')]
          .map((name) => name?.toLowerCase()).find((name) => ['og:image', 'twitter:image'].includes(name));
        if (imageMeta) {
          const image = tag.attrs.get('content') ?? '';
          if (!image.trim()) fail(route, `${imageMeta} image URL is empty`);
          else await checkReference(route, image, imageMeta);
        }
      }
    }
  }

  const robotsPath = await resourceFor('/robots.txt');
  if (!robotsPath) {
    fail('/robots.txt', 'file is missing');
  } else {
    const robots = await readFile(robotsPath, 'utf8');
    const declared = [...robots.matchAll(/^\s*Sitemap:\s*(\S+)/gim)].map((match) => match[1]);
    if (!declared.includes(`${ORIGIN}/sitemap.xml`)) {
      fail('/robots.txt', `must declare Sitemap: ${ORIGIN}/sitemap.xml`);
    }
  }

  const sitemapPath = await resourceFor('/sitemap.xml');
  if (!sitemapPath) {
    fail('/sitemap.xml', 'file is missing');
  } else {
    const sitemap = await readFile(sitemapPath, 'utf8');
    const locations = [...sitemap.matchAll(/<loc\b[^>]*>([\s\S]*?)<\/loc\s*>/gi)]
      .map((match) => decodeEntities(match[1].trim()));
    counts.sitemap = locations.length;
    if (!/<urlset\b/i.test(sitemap) || !/<\/urlset\s*>/i.test(sitemap) || !locations.length) {
      fail('/sitemap.xml', 'expected a nonempty sitemap urlset');
    }
    for (const route of CATEGORY_ROUTES) {
      if (!locations.includes(`${ORIGIN}${route}`)) fail('/sitemap.xml', `missing category ${route}`);
    }
    for (const location of locations) {
      try {
        const url = new URL(location);
        if (url.origin !== ORIGIN || /[?#]/.test(location)) {
          fail('/sitemap.xml', `noncanonical URL ${JSON.stringify(location)}`);
        }
        if (/^\/404(?:\.html)?\/?$/i.test(url.pathname)) fail('/sitemap.xml', '404 page must not be indexed');
      } catch {
        fail('/sitemap.xml', `invalid URL ${JSON.stringify(location)}`);
      }
    }
  }
  return { errors: [...errors], counts };
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 1 && ['--help', '-h'].includes(args[0])) {
    console.log('Usage: node scripts/check-site.mjs [built-site-directory]\nDefault: docs/_site\nRuns local checks only; no network requests or file writes.');
    return;
  }
  if (args.length > 1) throw new Error('Expected at most one built-site-directory argument');
  const siteRoot = path.resolve(args[0] ?? 'docs/_site');
  if (!(await fileInfo(siteRoot))?.isDirectory()) throw new Error(`Built site directory does not exist: ${siteRoot}`);
  const { errors, counts } = await checkSite(siteRoot);
  console.log(`Site: ${siteRoot}`);
  for (const error of errors) console.log(`ERROR ${error}`);
  console.table([
    { check: 'Required routes', count: counts.required },
    { check: 'HTML pages checked', count: counts.pages },
    { check: 'JSON-LD blocks', count: counts.jsonLd },
    { check: 'Local references', count: counts.references },
    { check: 'Homepage project cards', count: counts.cards },
    { check: 'Cards visible without JS', count: counts.visibleCards },
    { check: 'Homepage WebSite entities', count: counts.websites },
    { check: 'Sitemap URLs', count: counts.sitemap },
    { check: 'Errors', count: errors.length },
  ]);
  console.log(errors.length ? `FAIL: ${errors.length} error(s)` : 'PASS: static site checks passed');
  if (errors.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error(`ERROR ${error.message}`);
  process.exitCode = 1;
});
