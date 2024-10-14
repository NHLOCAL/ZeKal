title: "זה קל!"
description: "קבל את כל המידע על מונחי טכנולוגיה ומחשבים בפשטות ובקלות"
baseurl: "/ZeKal" # נדרש עבור GitHub Pages
url: "https://nhlocal.github.io" # URL האתר
language: "he"

# תבנית Jekyll שתשמש (נשתמש בעיצוב מותאם אישית)
theme: null

# תוספים
plugins:
  - jekyll-feed
  - jekyll-seo-tag

# הגדרות ניווט
navbar:
  - title: "בית"
    url: "/"
  - title: "שפות תכנות"
    url: "/topics/programming-languages.html"
  - title: "פיתוח אתרים"
    url: "/topics/web-development.html"
  - title: "רשתות"
    url: "/topics/networking.html"
  - title: "אבטחת מידע"
    url: "/topics/cybersecurity.html"
  - title: "מסדי נתונים"
    url: "/topics/databases.html"
  - title: "מחשוב ענן"
    url: "/topics/cloud-computing.html"
  - title: "בינה מלאכותית"
    url: "/topics/artificial-intelligence.html"
  - title: "רכיבי חומרה"
    url: "/topics/hardware-components.html"
  - title: "מתודולוגיות פיתוח תוכנה"
    url: "/topics/software-development-methodologies.html"
  - title: "מערכות הפעלה"
    url: "/topics/operating-systems.html"

# הגדרות שפה וכיוון טקסט
markdown: kramdown
kramdown:
  input: GFM
  hard_wrap: false

# פלט אתר
permalink: /:categories/:title.html
