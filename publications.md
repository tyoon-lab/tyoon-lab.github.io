---
layout: default
title: Publications
nav: publications
permalink: /publications/
description: "Full publication list from Yoon Lab."
---
<section class="page-hero compact-page-hero">
  <div class="container">
    <span class="section-kicker">Publications</span>
    <h1>Publications</h1>
    <p>Full publication list of Yoon Lab. Selected publications by research direction are highlighted in the Research page.</p>
  </div>
</section>

<section class="section publication-list-section">
  <div class="container">
    <div class="publication-list-head">
      <div>
        <span class="section-kicker">Full List</span>
        <h2 class="section-title">Full publication list</h2>
      </div>
      <p>Publications are shown in reverse chronological order. Thematic selected papers are integrated into the Research page to keep this page concise.</p>
    </div>

    <div class="full-publication-list slim-publication-list">
      {% assign year_groups = site.data.publications | group_by: "year" %}
      {% for group in year_groups %}
      <section class="publication-year-group">
        <h3>{{ group.name }}</h3>
        <div class="publication-entry-list">
          {% for paper in group.items %}
          <article class="publication-entry slim-publication-entry">
            <div class="publication-entry-number">#{{ paper.number }}</div>
            <div class="publication-entry-body">
              <h4>
                {% if paper.link and paper.link != "" %}
                <a href="{{ paper.link }}">{{ paper.title }}</a>
                {% else %}
                {{ paper.title }}
                {% endif %}
              </h4>
              <p class="publication-authors">{{ paper.authors }}</p>
              <p class="publication-journal">
                <em>{{ paper.journal }}</em>{% if paper.volume and paper.volume != "" %}, {{ paper.volume }}{% endif %}{% if paper.issue and paper.issue != "" %}({{ paper.issue }}){% endif %}{% if paper.pages and paper.pages != "" %}, {{ paper.pages }}{% endif %}, {{ paper.year }}.
              </p>
            </div>
          </article>
          {% endfor %}
        </div>
      </section>
      {% endfor %}
    </div>
  </div>
</section>
