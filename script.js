document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    const searchInput = document.getElementById('search');

    // פונקציה לטעינת words.md
    fetch('words.md')
        .then(response => response.text())
        .then(text => {
            const htmlContent = marked(text);
            content.innerHTML = htmlContent;
        })
        .catch(error => {
            content.innerHTML = '<p>אירעה שגיאה בטעינת התוכן.</p>';
            console.error('Error loading words.md:', error);
        });

    // פונקציה לחיפוש מונחים
    searchInput.addEventListener('input', () => {
        const filter = searchInput.value.toLowerCase();
        const rows = content.querySelectorAll('table tbody tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            let match = false;
            cells.forEach(cell => {
                if (cell.textContent.toLowerCase().includes(filter)) {
                    match = true;
                }
            });
            if (match) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});
