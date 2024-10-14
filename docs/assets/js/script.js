// גלילה חלקה לעוגנים
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if(target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});


// פונקציה להקריא את המונח באנגלית בקול גברי ואיטי יותר
function speak(text) {
    if ('speechSynthesis' in window) {
        var msg = new SpeechSynthesisUtterance();
        msg.text = text; // הטקסט שיוקרא
        msg.lang = 'en-US'; // השפה: אנגלית
        msg.rate = 1; // מהירות הקול (ערך קטן מ-1 עושה את הדיבור איטי יותר)
        msg.pitch = 0.8; // גובה הקול (נשאר רגיל)
        window.speechSynthesis.speak(msg);
    } else {
        alert('הדפדפן שלך לא תומך בהקראת טקסטים.');
    }
}

// פונקציה להוסיף כפתור השמעה לכל מונח באנגלית בעמודה השנייה
function addSpeakButtons() {
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        const rows = table.querySelectorAll('tr');
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            
            if (cells.length > 1) { // נוודא שיש יותר מתא אחד בשורה
                const englishTermCell = cells[1]; // תא בעמודה השנייה
                const englishTerm = englishTermCell.innerText;

                // יצירת כפתור השמעה עם סמל רמקול מ-Font Awesome
                const button = document.createElement('button');
                button.classList.add('speak-button'); // הוספת מחלקה ייחודית לכפתור
                button.innerHTML = '<i class="fas fa-volume-up"></i>'; // סמל רמקול
                button.onclick = () => speak(englishTerm);

                // הוספת הכפתור לתא בעמודה השנייה
                englishTermCell.appendChild(button);
            }
        });
    });
}

// להריץ את הפונקציה כשהדף נטען
document.addEventListener('DOMContentLoaded', addSpeakButtons);
