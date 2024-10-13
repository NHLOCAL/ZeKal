// script.js

document.addEventListener('DOMContentLoaded', () => {
    const sections = {
        group1: document.getElementById('group1'),
        group2: document.getElementById('group2'),
    };

    // פוקנציה לטעינת קובץ Markdown
    function loadMarkdown(group, section) {
        fetch('words.md')
            .then(response => {
                if (!response.ok) {
                    throw new Error('לא ניתן לטעון את הקובץ words.md');
                }
                return response.text();
            })
            .then(markdown => {
                // חילוץ החלק המתאים של הקבוצה מהקובץ
                const regex = new RegExp(`# ${group}:([\\s\\S]*?)(#|$)`);
                const match = markdown.match(regex);
                const groupMarkdown = match ? match[1].trim() : 'קבוצה לא נמצאה';
                
                // המרה ל-HTML באמצעות Marked.js
                const htmlContent = marked.parse(groupMarkdown);
                section.innerHTML = htmlContent;
            })
            .catch(error => {
                console.error('שגיאה בטעינת התוכן:', error);
                section.innerHTML = '<p>נוצרה שגיאה בטעינת התוכן. אנא נסה שוב מאוחר יותר.</p>';
            });
    }

    // טעינת התוכן עבור קבוצה 1 ו-2
    loadMarkdown('קבוצה 1', sections.group1);
    loadMarkdown('קבוצה 2', sections.group2);

    // טיפול בלחיצה על כפתור לשינוי קבוצה
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // הסרת ה-Active מכל הכפתורים והוספת Active לכפתור הנוכחי
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // הסתרת כל התכנים והצגת התוכן הנבחר
            const target = this.getAttribute('data-target');
            Object.values(sections).forEach(section => section.classList.remove('active'));
            sections[target].classList.add('active');
        });
    });
});
