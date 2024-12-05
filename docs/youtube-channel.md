---
layout: default
title: ערוץ היוטיוב
---

<div class="section red-section">
    <h1><i class="fab fa-youtube"></i> ערוץ היוטיוב שלנו</h1>
    <p>לימוד אנגלית בקלי קלות! שיעורים איכותיים ומותאמים במיוחד למבוגרים</p>
    <p>ערוץ היוטיוב שלנו מציע לכם ללמוד אנגלית בצורה פשוטה ומהנה.</p>

    <div class="video-categories">
        {% for playlist in site.data.videos.playlists %}
        <div class="video-category">
            <h3><a href="{{ playlist.url }}" target="_blank" rel="noopener noreferrer"><i class="fas fa-list"></i> {{ playlist.title }}</a></h3>
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

    <div class="home-buttons">
        </div>
</div>