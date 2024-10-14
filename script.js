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

    function generatePDF() {
        const { jsPDF } = window.jspdf;
        const activeSection = document.querySelector('.content-section.active table'); // מצא את הטבלה הפעילה
        const rows = activeSection.querySelectorAll('tr');
        
        const headers = [];
        const data = [];
    
        // הוספת הכותרות
        rows[0].querySelectorAll('th').forEach(th => {
            headers.push(th.innerText);
        });
    
        // הוספת תוכן השורות
        rows.forEach((row, index) => {
            if (index === 0) return; // דילוג על כותרות השורות
            const rowData = [];
            row.querySelectorAll('td').forEach(td => {
                rowData.push(td.innerText);
            });
            data.push(rowData);
        });
    
        const pdf = new jsPDF({
            orientation: 'p',
            unit: 'pt',
            format: 'a4',
            // הגדרת כיווניות RTL
            lang: 'he',
        });
    
        // הגדרת הגופן Rubik
        pdf.setFontSize(12);
    
        // הוספת טקסט עם כיווניות RTL
        pdf.text(`מונחים - ${currentTab}`, pdf.internal.pageSize.getWidth() - 40, 40, {
            align: 'right',
        });
    
        // היפוך סדר העמודות כדי להתאים ל-RTL
        const reversedHeaders = headers.slice().reverse();
        const reversedData = data.map(row => row.slice().reverse());
    
        // הוספת טבלה ל-PDF עם jsPDF autoTable
        pdf.autoTable({
            head: [reversedHeaders],
            body: reversedData,
            startY: 60,
            styles: {
                font: 'Rubik',
                fontStyle: 'normal',
                textColor: [0, 0, 0],
            },
            headStyles: {
                fillColor: [76, 175, 80], // צבע ירוק לכותרות
                textColor: [255, 255, 255],
                halign: 'right',
            },
            bodyStyles: {
                halign: 'right',
            },
            columnStyles: {
                // הגדרת רוחב עמודות אם נדרש
            },
            didDrawCell: function (data) {
                // פונקציה ליישור טקסט מימין לשמאל
                data.cell.text = data.cell.text.map(function (t) {
                    return t.split('').reverse().join('');
                });
            },
        });
    
        // שמירת ה-PDF
        pdf.save(`${currentTab}.pdf`);
    }
    

    // האזנה לכפתור ההורדה
    document.getElementById('download-pdf').addEventListener('click', generatePDF);

    // טעינת התוכן
    loadMarkdown();
});
