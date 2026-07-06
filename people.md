---
layout: default
title: People
nav: people
permalink: /people/
description: "Members of Yoon Lab."
---
<section class="page-hero">
  <div class="container">
    <span class="section-kicker">People</span>
    <h1>Members of Yoon Lab</h1>
    <p>Our group brings together students and researchers interested in electrochemical interfaces, degradation, corrosion, and advanced diagnostic methods.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    {% for group in site.data.members %}
    <section class="member-group">
      <h2>{{ group.group }}</h2>
      <div class="member-grid">
        {% for person in group.people %}
        <article class="member-card">
          <img class="member-photo" src="{{ person.photo | relative_url }}" alt="Photo placeholder for {{ person.name }}">
          <h3>{{ person.name }}</h3>
          <p class="role">{{ person.role }}</p>
          <p>{{ person.affiliation }}</p>
          <p style="margin-top: 10px;">{{ person.interests }}</p>
        </article>
        {% endfor %}
      </div>
    </section>
    {% endfor %}
  </div>
</section>
