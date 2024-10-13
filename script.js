// script.js

document.addEventListener('DOMContentLoaded', () => {
    fetch('words.md')
        .then(response => {
            if (!response.ok) {
                throw new Error('לא ניתן לטעון את הקובץ words.md');
            }
            return response.text();
        })
        .then(markdown => {
            // עיבוד Markdown ל-HTML
            const htmlContent = marked.parse(markdown);
            document.getElementById('content').innerHTML = htmlContent;
        })
        .catch(error => {
            console.error('שגיאה בטעינת התוכן:', error);
            document.getElementById('content').innerHTML = '<p>נוצרה שגיאה בטעינת התוכן. אנא נסה שוב מאוחר יותר.</p>';
        });
});
