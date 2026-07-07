---
layout: default
title: News
nav: news
permalink: /news/
description: "News, publications, recruiting, conferences, awards, and selected milestones from Yoon Lab."
---

<section class="page-hero compact-page-hero">
  <div class="container">
    <span class="section-kicker">News & Updates</span>
    <h1>News, publications, and opportunities</h1>
    <p>Recent publications, recruiting notices, conference activities, awards, thesis defenses, graduations, and selected milestones from Yoon Lab.</p>
  </div>
</section>

<section class="section news-page-section">
  <div class="container">
    <div class="news-page-intro clean-news-intro">
      <div>
        <span class="section-kicker">Latest updates</span>
        <h2 class="section-title">What is new in Yoon Lab</h2>
      </div>
      <p>Selected updates on publications, recruiting, conferences, awards, thesis defenses, graduations, and major lab milestones.</p>
    </div>

    <div class="news-category-grid" aria-label="News categories">
      <article class="news-category-card">
        <span>01</span>
        <h3>Publications</h3>
        <p>Accepted and published papers from the lab.</p>
      </article>
      <article class="news-category-card">
        <span>02</span>
        <h3>Recruiting & members</h3>
        <p>Graduate recruiting, new members, and student milestones.</p>
      </article>
      <article class="news-category-card">
        <span>03</span>
        <h3>Milestones</h3>
        <p>Conference participation, awards, thesis defenses, and graduations.</p>
      </article>
    </div>

    <div class="news-timeline-head">
      <span class="section-kicker">Timeline</span>
      <h3>Recent news</h3>
    </div>

    {% assign news_items = site.data.news | sort: "date" | reverse %}
    <div class="news-timeline">
      {% for item in news_items %}
      <article class="news-timeline-item">
        <div class="news-date-block">
          <time datetime="{{ item.date }}">{% if item.display_date %}{{ item.display_date }}{% else %}{{ item.date | date: "%Y.%m.%d" }}{% endif %}</time>
          <span>{{ item.category }}</span>
        </div>
        <div class="news-content-block">
          <h3>
            {% if item.link and item.link != "" %}
              <a href="{{ item.link | relative_url }}">{{ item.title }}</a>
            {% else %}
              {{ item.title }}
            {% endif %}
          </h3>
          <p>{{ item.summary }}</p>
        </div>
      </article>
      {% endfor %}
    </div>
  </div>
</section>
