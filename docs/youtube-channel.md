---
layout: default
title: ערוץ היוטיוב
---

<!-- youtube-channel.md -->
<div class="section red-section">
    <h1><i class="fab fa-youtube"></i> ערוץ היוטיוב שלנו</h1>
    <p>לימוד אנגלית בקלי קלות! שיעורים איכותיים ומותאמים במיוחד למבוגרים</p>
    <p>ערוץ היוטיוב שלנו מציע לכם ללמוד אנגלית בצורה פשוטה ומהנה.</p>

    <div class="video-categories">
        <h2><i class="fas fa-film"></i> קטגוריות סרטונים</h2>

        {% for category in site.data.video_categories %}
        <div class="video-category">
            <h3><i class="{{ category.icon }}"></i> {{ category.title }}</h3>
            <p>{{ category.description }}</p>
            <div class="video-grid">  <!-- מיכל גריד חדש -->
                {% for video in category.videos %}
                <div class="video-item"> <!-- אין צורך ב <li> -->
                    <div class="video-preview">
                        <iframe src="https://www.youtube.com/embed/{{ video.youtube_id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                    </div>
                    <div class="video-details">
                        <h4>{{ video.title }}</h4>
                        <p>{{ video.description }}</p>
                        <div class="download-buttons">
                            <a href="{{ video.mp4_url }}" class="button download-button small-button" download><i class="fas fa-download"></i> MP4</a>
                            <a href="{{ video.mp3_url }}" class="button download-button small-button" download><i class="fas fa-music"></i> MP3</a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    <div class="home-buttons">
        <a href="https://www.youtube.com/@Ze-Kal?utm_source=ze-kal-site&utm_medium=button" 
        class="button large-button red-button" 
        target="_blank"
        rel="noopener noreferrer">
        <i class="fab fa-youtube"></i> בקרו בערוץ
        </a>
        <a href="https://github.com/NHLOCAL/WatchZekal/" class="button large-button red-button" target="_blank" rel="noopener noreferrer">
            <i class="fab fa-github"></i> ככב בגיטאהב
        </a>
    </div>
</div>