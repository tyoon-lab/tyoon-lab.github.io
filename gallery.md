---
layout: default
title: Gallery
permalink: /gallery/
nav: gallery
---

<section class="page-hero">
  <div class="container">
    <span class="section-kicker">Gallery</span>
    <h1>Lab moments and activities</h1>
    <p>
      A visual record of research activities, conferences, experiments, and everyday life in Yoon Lab.
    </p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="gallery-intro">
      <div>
        <span class="section-kicker">Yoon Lab Gallery</span>
        <h2 class="section-title">Research, people, and lab life</h2>
      </div>
      <p class="section-lead">
        Photos can be added gradually as the lab homepage grows. Each card is managed from
        <code>_data/gallery.yml</code>, while image files are stored in
        <code>assets/images/gallery/</code>.
      </p>
    </div>

    <div class="gallery-grid">
      {% for item in site.data.gallery %}
      <article class="gallery-card">
        {% if item.image and item.image != "" %}
          <img src="{{ item.image | relative_url }}" alt="{{ item.title | escape }}" class="gallery-image">
        {% else %}
          <div class="gallery-placeholder" aria-hidden="true">
            <span>{{ item.category | default: 'Gallery' }}</span>
          </div>
        {% endif %}
        <div class="gallery-card-body">
          <div class="gallery-meta">
            <span>{{ item.category }}</span>
            {% if item.date and item.date != "" %}<time>{{ item.date }}</time>{% endif %}
          </div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </div>
      </article>
      {% endfor %}
    </div>
  </div>
</section>
