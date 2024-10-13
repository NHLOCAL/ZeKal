// script.js

document.addEventListener('DOMContentLoaded', () => {
    const tabButtonsContainer = document.getElementById('tab-buttons');
    const contentSectionsContainer = document.getElementById('content-sections');
    let currentTab = null;

    // פונקציה לטעינת קובץ Markdown
    function loadMarkdown() {
        fetch('words.md')
            .then(response => {
                if (!response.ok) {
                    throw new Error('לא ניתן לטעון את הקובץ words.md');
                }
                return response.text();
            })
            .then(markdown => {
                const groups = extractGroups(markdown);
                renderTabs(groups);
                renderContent(groups);
                setActiveTab(Object.keys(groups)[0]); // הפעלת הטאב הראשון כברירת מחדל
            })
            .catch(error => {
                console.error('שגיאה בטעינת התוכן:', error);
                tabButtonsContainer.innerHTML = '<p>נוצרה שגיאה בטעינת התוכן. אנא נסה שוב מאוחר יותר.</p>';
            });
    }

    // פונקציה לחילוץ קבוצות מהקובץ Markdown
    function extractGroups(markdown) {
        const groups = {};
        const regex = /# (.*?)\n([\s\S]*?)(?=# |$)/g;
        let match;

        while ((match = regex.exec(markdown)) !== null) {
            const groupName = match[1].trim();
            const groupContent = match[2].trim();
            groups[groupName] = groupContent;
        }
        return groups;
    }

    // פונקציה ליצירת הכפתורים דינמית
    function renderTabs(groups) {
        tabButtonsContainer.innerHTML = '';
        Object.keys(groups).forEach(groupName => {
            const button = document.createElement('button');
            button.classList.add('tab-button');
            button.innerText = groupName;
            button.addEventListener('click', () => {
                setActiveTab(groupName);
            });
            tabButtonsContainer.appendChild(button);
        });
    }

    // פונקציה ליצירת התוכן דינמית
    function renderContent(groups) {
        contentSectionsContainer.innerHTML = '';
        Object.entries(groups).forEach(([groupName, groupContent]) => {
            const section = document.createElement('section');
            section.id = groupName;
            section.classList.add('content-section');
            section.innerHTML = marked.parse(groupContent);
            contentSectionsContainer.appendChild(section);
        });
    }

    // פונקציה לשינוי הטאב הפעיל
    function setActiveTab(groupName) {
        if (currentTab === groupName) return;

        currentTab = groupName;

        // עדכון כפתורי הניווט
        document.querySelectorAll('.tab-button').forEach(button => {
            button.classList.remove('active');
            if (button.innerText === groupName) {
                button.classList.add('active');
            }
        });

        // עדכון התוכן המוצג
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
            if (section.id === groupName) {
                section.classList.add('active');
            }
        });
    }

    // פונקציה ליצירת PDF מהתוכן הנבחר
    function generatePDF() {
        const { jsPDF } = window.jspdf; // ייבוא jsPDF מהמודול של הספרייה
        const activeSection = document.querySelector('.content-section.active');
        const pdf = new jsPDF('p', 'pt', 'a4');
        pdf.html(activeSection, {
            callback: function (doc) {
                doc.save(`${currentTab}.pdf`);
            },
            x: 10,
            y: 10
        });
    }

    // האזנה לכפתור ההורדה
    document.getElementById('download-pdf').addEventListener('click', generatePDF);

    // טעינת התוכן
    loadMarkdown();
});
