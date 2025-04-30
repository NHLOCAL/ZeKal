---
layout: default
title: "זה קל! - ערוץ היוטיוב"
---

<div class="youtube-intro-section">
    <h1><i class="fab fa-youtube"></i> לימוד אנגלית בכיף עם "זה קל!"</h1>
    <p>ברוכים הבאים לערוץ היוטיוב הייחודי שלנו! כאן תמצאו מגוון רחב של סרטונים ללימוד אנגלית, שנוצרו כולם באמצעות בינה מלאכותית (AI), כדי להפוך את חווית הלמידה שלכם לפשוטה, מהנה ויעילה יותר מאי פעם.</p>
</div>

<!-- Playlist Quick Links -->
<div class="playlist-links">
    <h3><i class="fas fa-tags"></i> קישורים מהירים לפלייליסטים:</h3>
    {% for playlist in site.data.videos.playlists %}
        <a href="#{{ playlist.title | slugify }}" class="button small-button">{{ playlist.title }}</a>
    {% endfor %}
</div>
<!-- Removed the <hr> here -->

<!-- Video Categories -->
<div class="video-categories section"> <!-- Added section class for consistency -->
    {% for playlist in site.data.videos.playlists %}
    <div class="video-category" id="{{ playlist.title | slugify }}">
         <h3><a href="{{ playlist.url }}&utm_source=ze-kal-site&utm_medium=link" target="_blank" rel="noopener noreferrer"><i class="fas fa-list-ul"></i> {{ playlist.title }}</a></h3>
         <p>{{ playlist.description | newline_to_br | strip_newlines }}</p>

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
                        <a href="{{ video.mp4_url }}" class="button download-button" download title="הורד כקובץ MP4"><i class="fas fa-download"></i> MP4</a>
                        {% else %}
                        <button class="button download-button" disabled title="קובץ MP4 אינו זמין להורדה"><i class="fas fa-download"></i> MP4 (בקרוב)</button>
                        {% endif %}
                        {% assign mp3_url = video.mp4_url | replace: '.mp4', '.mp3' %}
                        {% comment %} Check if an mp3_url field exists, otherwise assume based on mp4 {% endcomment %}
                        {% assign final_mp3_url = video.mp3_url | default: mp3_url %}
                        {% if video.mp4_url or video.mp3_url %}
                           {% if video.mp4_url == final_mp3_url and video.mp4_url != nil %} {# Heuristic: if replaced URL is same as mp4, likely no separate MP3 yet #}
                               <button class="button download-button" disabled title="קובץ MP3 אינו זמין להורדה"><i class="fas fa-music"></i> MP3 (בקרוב)</button>
                           {% else %}
                               <a href="{{ final_mp3_url }}" class="button download-button" download title="הורד כקובץ MP3"><i class="fas fa-music"></i> MP3</a>
                           {% endif %}
                        {% else %}
                           <button class="button download-button" disabled title="קובץ MP3 אינו זמין להורדה"><i class="fas fa-music"></i> MP3 (בקרוב)</button>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <!-- Removed the <hr> here -->
    {% endfor %}

    <!-- Final Call to Action -->
    <div class="youtube-final-cta">
        <a href="https://www.youtube.com/@Ze-Kal?sub_confirmation=1&utm_source=ze-kal-site&utm_medium=button"
           class="button large-button accent-button" target="_blank" rel="noopener noreferrer">
            <i class="fab fa-youtube"></i> הירשמו לערוץ (חינם!)
        </a>
        <a href="https://github.com/NHLOCAL/WatchZekal/" class="button large-button github-button" target="_blank" rel="noopener noreferrer">
            <i class="fab fa-github"></i> קוד המקור (GitHub)
        </a>
    </div>
</div>