---
layout: default
title: Research
nav: research
permalink: /research/
description: "Research themes of Yoon Lab."
---
<section class="page-hero">
  <div class="container">
    <span class="section-kicker">Research</span>
    <h1>Electrochemical signals as windows into hidden interfacial processes</h1>
    <p>Yoon Lab develops quantitative approaches to understand how interfaces, transport limitations, side reactions, and corrosion determine the performance and lifetime of electrochemical energy systems.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      {% for theme in site.data.research %}
      <article class="theme-card">
        <div class="theme-icon">{% include icon.html name=theme.icon %}</div>
        <div>
          <h3>{{ theme.title }}</h3>
          <p>{{ theme.description }}</p>
        </div>
      </article>
      {% endfor %}
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <span class="section-kicker">Approach</span>
    <h2 class="section-title">From measured signals to mechanistic parameters</h2>
    <p class="section-lead">Our work emphasizes the translation of electrochemical measurements into physically meaningful descriptors such as interfacial resistance, transport limitation, reaction rate, corrosion susceptibility, and degradation mode.</p>
    <div class="grid-2" style="margin-top: 34px;">
      <article class="paper-card">
        <h3>Signal acquisition</h3>
        <p>EIS, DRT, PITT/GITT, chronoamperometry, QCM, RRDE, and operando or post-mortem materials characterization.</p>
      </article>
      <article class="paper-card">
        <h3>Mechanistic interpretation</h3>
        <p>Physics-informed modeling, transport analysis, kinetic decoupling, and degradation/corrosion mapping.</p>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <span class="section-kicker">Evidence</span>
    <h2 class="section-title">Representative publications linked to each research theme</h2>
    <p class="section-lead">Selected papers are shown here to connect the research themes with concrete publications. The complete list is available on the Publications page.</p>

    <div class="research-publication-list">
      {% for theme in site.data.publication_themes %}
      <section class="research-publication-block">
        <div class="research-publication-head">
          <h3>{{ theme.title }}</h3>
          <p>{{ theme.description }}</p>
        </div>

        <div class="research-paper-list">
          {% assign theme_pubs = site.data.publications | where: "category", theme.slug | where: "research_featured", true | sort: "featured_order" %}
          {% for paper in theme_pubs %}
          <article class="research-paper-item">
            <span>{{ paper.year }}</span>
            <div>
              <h4>{{ paper.title }}</h4>
              <p>{{ paper.journal }}</p>
            </div>
          </article>
          {% endfor %}
        </div>
      </section>
      {% endfor %}
    </div>
  </div>
</section>
