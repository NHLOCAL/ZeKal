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
            const groups = parseMarkdown(markdown);
            populateSidebar(groups);
            displayGroup(groups[0]); // תצוגת הקבוצה הראשונה כברירת מחדל
        })
        .catch(error => {
            console.error('שגיאה בטעינת התוכן:', error);
            document.getElementById('content').innerHTML = '<p>נוצרה שגיאה בטעינת התוכן. אנא נסה שוב מאוחר יותר.</p>';
        });

    // פונקציה לפרק את קובץ ה-Markdown לקבוצות
    function parseMarkdown(markdown) {
        const lines = markdown.split('\n');
        const groups = [];
        let currentGroup = null;

        lines.forEach(line => {
            const groupMatch = line.match(/^# קבוצה\s*\d+:\s*(.+)/);
            if (groupMatch) {
                if (currentGroup) {
                    groups.push(currentGroup);
                }
                currentGroup = {
                    name: groupMatch[1].trim(),
                    terms: []
                };
            } else if (currentGroup && line.startsWith('|') && !line.startsWith('| English Term')) {
                const cells = line.split('|').map(cell => cell.trim()).filter(cell => cell !== '');
                if (cells.length === 3) {
                    currentGroup.terms.push({
                        english: cells[0],
                        hebrew: cells[1],
                        explanation: cells[2]
                    });
                }
            }
        });

        if (currentGroup) {
            groups.push(currentGroup);
        }

        return groups;
    }

    // פונקציה למילוי הניווט הצדדי ברשימת הקבוצות
    function populateSidebar(groups) {
        const groupList = document.getElementById('group-list');
        groups.forEach((group, index) => {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#';
            a.textContent = group.name;
            a.addEventListener('click', (e) => {
                e.preventDefault();
                displayGroup(group);
                highlightActiveGroup(index);
            });
            li.appendChild(a);
            groupList.appendChild(li);
        });
    }

    // פונקציה להצגת קבוצה מסוימת
    function displayGroup(group) {
        const termsSection = document.getElementById('terms');
        termsSection.innerHTML = ''; // ניקוי התוכן הקודם

        const groupDiv = document.createElement('div');
        groupDiv.classList.add('group');

        const groupTitle = document.createElement('h2');
        groupTitle.textContent = group.name;
        groupDiv.appendChild(groupTitle);

        const table = document.createElement('table');

        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        ['מונח באנגלית', 'תרגום לעברית', 'הסבר בעברית'].forEach(text => {
            const th = document.createElement('th');
            th.textContent = text;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        group.terms.forEach(term => {
            const tr = document.createElement('tr');

            const tdEnglish = document.createElement('td');
            tdEnglish.textContent = term.english;
            tr.appendChild(tdEnglish);

            const tdHebrew = document.createElement('td');
            tdHebrew.textContent = term.hebrew;
            tr.appendChild(tdHebrew);

            const tdExplanation = document.createElement('td');
            tdExplanation.textContent = term.explanation;
            tr.appendChild(tdExplanation);

            tbody.appendChild(tr);
        });
        table.appendChild(tbody);

        groupDiv.appendChild(table);
        termsSection.appendChild(groupDiv);
    }

    // פונקציה להדגשת הקבוצה הפעילה ב-sidebar
    function highlightActiveGroup(activeIndex) {
        const links = document.querySelectorAll('#group-list a');
        links.forEach((link, index) => {
            if (index === activeIndex) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // חיפוש
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');

    searchButton.addEventListener('click', () => {
        const query = searchInput.value.trim().toLowerCase();
        if (query === '') return;

        fetch('words.md')
            .then(response => response.text())
            .then(markdown => {
                const groups = parseMarkdown(markdown);
                const results = [];

                groups.forEach(group => {
                    group.terms.forEach(term => {
                        if (
                            term.english.toLowerCase().includes(query) ||
                            term.hebrew.includes(query) ||
                            term.explanation.includes(query)
                        ) {
                            results.push({
                                group: group.name,
                                ...term
                            });
                        }
                    });
                });

                displaySearchResults(results);
                highlightActiveGroup(-1); // הסרת ההדגשה מכל קבוצה
            })
            .catch(error => {
                console.error('שגיאה בחיפוש:', error);
                alert('נוצרה שגיאה בחיפוש. אנא נסה שוב מאוחר יותר.');
            });
    });

    // פונקציה להצגת תוצאות החיפוש
    function displaySearchResults(results) {
        const termsSection = document.getElementById('terms');
        termsSection.innerHTML = ''; // ניקוי התוכן הקודם

        const groupDiv = document.createElement('div');
        groupDiv.classList.add('group');

        const groupTitle = document.createElement('h2');
        groupTitle.textContent = 'תוצאות חיפוש';
        groupDiv.appendChild(groupTitle);

        if (results.length === 0) {
            const noResults = document.createElement('p');
            noResults.textContent = 'לא נמצאו תוצאות לחיפוש שלך.';
            groupDiv.appendChild(noResults);
        } else {
            const table = document.createElement('table');

            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            ['קבוצה', 'מונח באנגלית', 'תרגום לעברית', 'הסבר בעברית'].forEach(text => {
                const th = document.createElement('th');
                th.textContent = text;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            const tbody = document.createElement('tbody');
            results.forEach(result => {
                const tr = document.createElement('tr');

                const tdGroup = document.createElement('td');
                tdGroup.textContent = result.group;
                tr.appendChild(tdGroup);

                const tdEnglish = document.createElement('td');
                tdEnglish.textContent = result.english;
                tr.appendChild(tdEnglish);

                const tdHebrew = document.createElement('td');
                tdHebrew.textContent = result.hebrew;
                tr.appendChild(tdHebrew);

                const tdExplanation = document.createElement('td');
                tdExplanation.textContent = result.explanation;
                tr.appendChild(tdExplanation);

                tbody.appendChild(tr);
            });
            table.appendChild(tbody);

            groupDiv.appendChild(table);
        }

        termsSection.appendChild(groupDiv);
    }
});
