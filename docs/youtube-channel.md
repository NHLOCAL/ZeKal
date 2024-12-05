---
layout: default
title: ערוץ היוטיוב
---

<div class="section red-section">
    <div class="header-section"> <!-- מיכל חדש עבור הכותרת והתיאור -->
        <h1 style="text-align: center;"><i class="fab fa-youtube"></i> ערוץ היוטיוב שלנו</h1>
        <p style="text-align: center;">לימוד אנגלית בקלי קלות! שיעורים איכותיים ומותאמים במיוחד למבוגרים. ערוץ היוטיוב שלנו מציע לכם ללמוד אנגלית בצורה פשוטה ומהנה.</p>
    </div>

    <div class="playlist-links">
        {% for playlist in site.data.videos.playlists %}
            <a href="#{{ playlist.title | slugify }}" class="button small-button">{{ playlist.title }}</a>
        {% endfor %}
    </div>

    <div class="video-categories">
        {% for playlist in site.data.videos.playlists %}
        <div class="video-category" id="{{ playlist.title | slugify }}">
            <h3><a href="{{ playlist.url }}" target="_blank" rel="noopener noreferrer"><i class="fas fa-play-circle"></i> {{ playlist.title }}</a></h3>
            <p>{{ playlist.description | markdownify }}</p>
            <div class="video-grid">
                {% for video in playlist.videos %}
                <div class="video-item">
                    <a href="{{ video.url }}" target="_blank" rel="noopener noreferrer">
                        <div class="video-preview" style="background-image: url('{{ video.thumbnail }}');">
                            <i class="fas fa-play play-icon"></i>
                        </div>
                    </a>
                    <div class="video-details">
                        <h4>{{ video.title }}</h4>
                        <p>{{ video.description | markdownify }}</p>
                        <div class="download-buttons">
                            {% if video.mp4_url %}
                            <a href="{{ video.mp4_url }}" class="button download-button small-button" download><i class="fas fa-download"></i> MP4</a>
                            {% else %}
                            <button class="button download-button small-button" disabled><i class="fas fa-download"></i> MP4</button>
                            {% endif %}
                            {% if video.mp3_url %}
                            <a href="{{ video.mp3_url }}" class="button download-button small-button" download><i class="fas fa-music"></i> MP3</a>
                            {% else %}
                            <button class="button download-button small-button" disabled><i class="fas fa-music"></i> MP3</button>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>

    <div class="home-buttons">  <!-- החזרת כפתורי "הכנס לערוץ" ו"ככב בגיטאהב" -->
        <a href="https://www.youtube.com/@Ze-Kal?utm_source=ze-kal-site&utm_medium=button" 
           class="button large-button red-button" target="_blank" rel="noopener noreferrer">
            <i class="fab fa-youtube"></i> בקרו בערוץ
        </a>
        <a href="https://github.com/NHLOCAL/WatchZekal/" class="button large-button red-button" target="_blank" rel="noopener noreferrer">
            <i class="fab fa-github"></i> ככב בגיטאהב
        </a>
    </div>
</div>