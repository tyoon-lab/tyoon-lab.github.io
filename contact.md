---
layout: default
title: Contact
permalink: /contact/
---

<section class="page-hero">
  <div class="container">
    <span class="section-kicker">Contact</span>
    <h1>Contact Yoon Lab</h1>
    <p>Department of Chemical Engineering, Kyung Hee University</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="contact-grid">
      <article class="contact-card">
        <h3>Address</h3>
        <p>
          {% if site.lab.address_lines %}
            {% for line in site.lab.address_lines %}
              {{ line }}{% unless forloop.last %}<br>{% endunless %}
            {% endfor %}
          {% else %}
            Department of Chemical Engineering<br>
            Kyung Hee University<br>
            1732, Deogyeong-daero, Giheung-gu<br>
            Yongin-si, Gyeonggi-do 17104<br>
            Republic of Korea
          {% endif %}
        </p>
      </article>

      <article class="contact-card">
        <h3>Email</h3>
        <p>
          <a href="mailto:{{ site.lab.email | default: 'tyoon@khu.ac.kr' }}">{{ site.lab.email | default: 'tyoon@khu.ac.kr' }}</a>
        </p>
        <p>
          For research collaboration, student inquiries, and academic correspondence.
        </p>
      </article>

      <article class="contact-card">
        <h3>Inquiries</h3>
        <p>
          Prospective graduate students, undergraduate researchers, and collaborators are welcome to contact the PI by email.
        </p>
        <p>
          Please include a brief introduction, research interests, and relevant experience when contacting the lab.
        </p>
      </article>
    </div>
  </div>
</section>
