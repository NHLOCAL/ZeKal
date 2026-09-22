# ZeKal project gateway

The homepage becomes the public entry point to NH Local's projects. The existing Jekyll and GitHub Pages deployment from `main:/docs` remains the publishing path. Existing `/topics/*.html` and `/youtube-channel.html` URLs stay available.

## Direction

Lead with the visitor's task, then the project that solves it. The user confirmed four featured projects: Alef Bot, the toolbox, Shir Bot, and Singles Sorter. Organize the full directory into AI and content, music, computer tools, and learning. Add useful category guides, search by name or need, and clear destination/platform labels. The full directory is rendered at build time; JavaScript only enhances filtering.

Keep the direct Hebrew voice and Rubik typography seen across the existing sites. Use a warm light canvas, deep ink, teal accents, precise borders, and a small connected project map as the homepage signature. Project colors identify destinations. Support dark mode, RTL, keyboard navigation, narrow screens, and reduced motion.

## Delivery sequence

1. Verify public project destinations and centralize the catalog and category content.
2. Build the shared shell, homepage, project cards, and category templates.
3. Add progressive search and filters with shareable state and accessible feedback.
4. Bring the existing learning pages into the new navigation without changing their URLs.
5. Verify canonical metadata, structured data, sitemap, internal links, and asset performance.
6. Build and test desktop/mobile flows, fix findings, and commit each coherent stage.

## Sources and boundaries

- https://nhlocal.github.io/ supplies the public project inventory and creator identity.
- https://tools.ze-kal.top/ supplies current tool destinations and practical visual references.
- https://alef-bot.top/, https://shir-bot.ze-kal.top/, and https://singles-sorter.ze-kal.top/ supply product descriptions.
- https://developers.google.com/search/docs/crawling-indexing/links-crawlable explains crawlable, descriptive links.
- https://developers.google.com/search/docs/crawling-indexing/url-structure explains stable, intelligible URL structure.

Do not claim that all projects are free, currently maintained, or browser apps. Use product landing pages for downloads rather than pinning release files. Do not add analytics, tracking query parameters, or third-party runtime dependencies. Preserve the existing feedback endpoint without submitting test messages. Production deployment is separate from local implementation and commits.
