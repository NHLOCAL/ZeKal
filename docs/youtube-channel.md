---
layout: default
title: "זה קל! - ערוץ היוטיוב"
---

<section class="section youtube-section">
    <div class="header-section" style="text-align: center; margin-bottom: 40px;">
        <h1><i class="fab fa-youtube"></i> לימוד אנגלית עם "זה קל!"</h1>
        <p>ברוכים הבאים לערוץ היוטיוב שלנו! כאן תמצאו מגוון רחב של סרטונים ללימוד אנגלית, שנוצרו כולם בעזרת בינה מלאכותית, כדי להפוך את הלמידה שלכם לפשוטה, מהנה ויעילה.</p>
    </div>

    <!-- Playlist Quick Links -->
    <div class="playlist-links">
        {% for playlist in site.data.videos.playlists %}
            <a href="#{{ playlist.title | slugify }}" class="button small-button">{{ playlist.title }}</a>
        {% endfor %}
    </div>

    <!-- Video Categories -->
    <div class="video-categories">
        {% for playlist in site.data.videos.playlists %}
        <div class="video-category" id="{{ playlist.title | slugify }}">
             <h3><a href="{{ playlist.url }}&utm_source=ze-kal-site&utm_medium=link" target="_blank" rel="noopener noreferrer"><i class="fas fa-play-circle"></i> {{ playlist.title }}</a></h3>
             <p style="margin-bottom: 25px;">{{ playlist.description | newline_to_br | strip_newlines }}</p> <!-- Use newline_to_br for better formatting -->

            <!-- Video Grid for the Playlist -->
            <div class="video-grid">
                {% for video in playlist.videos %}
                <div class="video-item">
                    <!-- Video Preview/Link -->
                    <a href="{{ video.url }}&utm_source=ze-kal-site&utm_medium=link" target="_blank" rel="noopener noreferrer" aria-label="צפה בסרטון {{ video.title }}">
                        <div class="video-preview" style="background-image: url('{{ video.thumbnail | default: '/assets/images/placeholder.png' }}');">
                            <i class="fas fa-play play-icon" aria-hidden="true"></i>
                        </div>
                    </a>
                    <!-- Video Details -->
                    <div class="video-details">
                        <h4>{{ video.title }}</h4>
                        {% if video.description %}
                            <p>{{ video.description | newline_to_br | strip_newlines }}</p>
                        {% endif %}
                        <!-- Download Buttons -->
                        <div class="download-buttons">
                            {% if video.mp4_url %}
                            <a href="{{ video.mp4_url }}" class="button download-button small-button" download title="הורד כקובץ MP4"><i class="fas fa-download"></i> MP4</a>
                            <a href="{{ video.mp4_url | replace: '.mp4', '.mp3' }}" class="button download-button small-button" download title="הורד כקובץ MP3"><i class="fas fa-music"></i> MP3</a>
                            {% else %}
                            <button class="button download-button small-button" disabled title="קובץ MP4 אינו זמין להורדה"><i class="fas fa-download"></i> MP4</button>
                            <button class="button download-button small-button" disabled title="קובץ MP3 אינו זמין להורדה"><i class="fas fa-music"></i> MP3</button>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% unless forloop.last %}<hr style="margin: 40px 0; border: 0; border-top: 1px solid var(--color-border);">{% endunless %}
        {% endfor %}
    </div>

    <!-- Final Call to Action -->
    <div class="home-buttons" style="margin-top: 50px;">
        <a href="https://www.youtube.com/@Ze-Kal?sub_confirmation=1&utm_source=ze-kal-site&utm_medium=button"
           class="button large-button" target="_blank" rel="noopener noreferrer">
            <i class="fab fa-youtube"></i> הירשמו לערוץ
        </a>
        <a href="https://github.com/NHLOCAL/WatchZekal/" class="button large-button github-button" target="_blank" rel="noopener noreferrer">
            <i class="fab fa-github"></i> צפו בקוד המקור (GitHub)
        </a>
    </div>
</section>