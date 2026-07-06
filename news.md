---
layout: default
title: News
nav: news
permalink: /news/
description: "News and updates from Yoon Lab."
---
<section class="page-hero">
  <div class="container">
    <span class="section-kicker">News</span>
    <h1>News, publications, and opportunities</h1>
    <p>Recent updates from Yoon Lab. Edit <code>_data/news.yml</code> to add new items.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="paper-list">
      {% for item in site.data.news %}
      <article class="news-card">
        <span class="category">{{ item.category }}</span>
        <h3>{% if item.link and item.link != '' %}<a href="{{ item.link | relative_url }}">{{ item.title }}</a>{% else %}{{ item.title }}{% endif %}</h3>
        <p>{{ item.summary }}</p>
        <time datetime="{{ item.date }}">{{ item.date }}</time>
      </article>
      {% endfor %}
    </div>
  </div>
</section>
