---
layout: default
title: Publications
nav: publications
permalink: /publications/
description: "Selected publications from Yoon Lab."
---
<section class="page-hero">
  <div class="container">
    <span class="section-kicker">Publications</span>
    <h1>Selected papers and research highlights</h1>
    <p>This page lists selected publications. The list can be updated by editing <code>_data/publications.yml</code>.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="paper-list">
      {% assign pubs = site.data.publications | sort: 'year' | reverse %}
      {% for paper in pubs %}
      <article class="paper-card">
        <div class="paper-meta">{{ paper.year }} · {{ paper.journal }}{% if paper.highlight %} · Highlight{% endif %}</div>
        <h3>{% if paper.link and paper.link != '' %}<a href="{{ paper.link }}">{{ paper.title }}</a>{% else %}{{ paper.title }}{% endif %}</h3>
        <p>{{ paper.authors }} · {{ paper.type }}</p>
      </article>
      {% endfor %}
    </div>
  </div>
</section>
