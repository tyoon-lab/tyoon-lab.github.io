---
layout: default
title: Contact
nav: contact
permalink: /contact/
description: "Contact information for Yoon Lab."
---
<section class="page-hero">
  <div class="container">
    <span class="section-kicker">Contact</span>
    <h1>Contact Yoon Lab</h1>
    <p>{{ site.lab.institution }}</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="contact-grid">
      <article class="contact-card">
  <h3>Address</h3>
  <p>
    {% for line in site.lab.address_lines %}
      {{ line }}{% unless forloop.last %}<br>{% endunless %}
    {% endfor %}
  </p>
</article>
      <article class="contact-card">
        <h3>Email</h3>
        <p><a href="mailto:{{ site.lab.email }}">{{ site.lab.email }}</a></p>
      </article>
      <article class="contact-card">
        <h3>Current Website</h3>
        <p><a href="{{ site.lab.current_site }}">Google Sites archive</a></p>
      </article>
    </div>
  </div>
</section>
