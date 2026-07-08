---
layout: default
title: People
permalink: /people/
---

<section class="page-hero compact-page-hero">
  <div class="container">
    <span class="section-kicker">People</span>
    <h1>Team members</h1>
    <p>Yoon Lab brings together researchers working on electrochemical interfaces, degradation, corrosion, and quantitative diagnostics for energy materials and devices.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    {% assign pi = site.data.people.pi %}
    <div class="people-section-head">
      <span class="section-kicker">Principal Investigator</span>
      <h2 class="section-title">{{ pi.name }}</h2>
    </div>

    <article class="pi-profile-card">
      <div class="pi-photo-block">
        {% if pi.photo and pi.photo != "" %}
          <img src="{{ pi.photo | relative_url }}" alt="{{ pi.name }}" class="pi-photo">
        {% else %}
          <div class="pi-photo-placeholder">{{ pi.initials }}</div>
        {% endif %}
      </div>

      <div class="pi-profile-main">
        <p class="pi-title">{{ pi.degrees }} · {{ pi.title }}</p>
        <h3>Electrochemical Engineering Lab</h3>
        <p class="pi-affiliation">{{ pi.department }}, {{ pi.institution }}</p>
        <p><a class="text-link" href="mailto:{{ pi.email }}">{{ pi.email }}</a></p>

        <div class="pi-link-buttons" aria-label="Principal investigator academic profiles">
          <a href="https://scholar.google.com/citations?hl=ko&user=XYBKq3EAAAAJ" target="_blank" rel="noopener">Google Scholar</a>
          <a href="https://orcid.org/0000-0002-9403-9250" target="_blank" rel="noopener">ORCID</a>
        </div>

        <div class="people-tag-list">
          {% for interest in pi.research_interests %}
            <span>{{ interest }}</span>
          {% endfor %}
        </div>
      </div>

      <div class="pi-profile-details">
        <div>
          <h4>Education</h4>
          <ul class="compact-list">
            {% for item in pi.education %}
              <li><strong>{{ item.degree }}</strong>, {{ item.institution }} <span>{{ item.period }}</span></li>
            {% endfor %}
          </ul>
        </div>

        <div>
          <h4>Professional History</h4>
          <ul class="compact-list">
            {% for item in pi.professional_history %}
              <li><strong>{{ item.period }}</strong> · {{ item.position }}, {{ item.institution }}</li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </article>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="people-section-head">
      <span class="section-kicker">Current Members</span>
      <h2 class="section-title">Students and researchers</h2>
    </div>

    <div class="member-group-block">
      <h3>Graduate Students</h3>
      <div class="people-grid">
        {% for person in site.data.people.graduate_students %}
          <article class="person-card-v2">
            {% if person.photo and person.photo != "" %}
              <img src="{{ person.photo | relative_url }}" alt="{{ person.name }}" class="person-photo-v2">
            {% else %}
              <div class="person-photo-placeholder">{{ person.name | slice: 0, 1 }}</div>
            {% endif %}
            <div>
              <p class="person-role">{{ person.role }}</p>
              <h4>{{ person.name }}</h4>
              {% if person.topic and person.topic != "" %}<p>{{ person.topic }}</p>{% endif %}
              {% if person.email and person.email != "" %}<a class="text-link" href="mailto:{{ person.email }}">{{ person.email }}</a>{% endif %}
            </div>
          </article>
        {% endfor %}
      </div>
    </div>

    <div class="member-group-block">
      <h3>Undergraduate Researchers</h3>
      <div class="people-grid compact-people-grid">
        {% for person in site.data.people.undergraduate_students %}
          <article class="person-card-v2">
            {% if person.photo and person.photo != "" %}
              <img src="{{ person.photo | relative_url }}" alt="{{ person.name }}" class="person-photo-v2">
            {% else %}
              <div class="person-photo-placeholder">{{ person.name | slice: 0, 1 }}</div>
            {% endif %}
            <div>
              <p class="person-role">{{ person.role }}</p>
              <h4>{{ person.name }}</h4>
              {% if person.topic and person.topic != "" %}<p>{{ person.topic }}</p>{% endif %}
              {% if person.email and person.email != "" %}<a class="text-link" href="mailto:{{ person.email }}">{{ person.email }}</a>{% endif %}
            </div>
          </article>
        {% endfor %}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="people-section-head">
      <span class="section-kicker">Alumni</span>
      <h2 class="section-title">Former members</h2>
      <p class="section-lead">Former members of Yoon Lab continue their careers in academia, research institutes, and the battery industry.</p>
    </div>

    <div class="alumni-block-list">
      {% for group in site.data.people.alumni_groups %}
        <section class="alumni-block">
          <h3>{{ group.title }}</h3>
          <div class="alumni-table-wrap">
            <table class="alumni-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Program / Role</th>
                  <th>Period</th>
                  <th>Current affiliation</th>
                  <th>Email</th>
                </tr>
              </thead>
              <tbody>
                {% for person in group.people %}
                  <tr>
                    <td><strong>{{ person.name }}</strong></td>
                    <td>{{ person.role }}</td>
                    <td>{{ person.period }}</td>
                    <td>{% if person.current and person.current != "" %}{{ person.current }}{% else %}—{% endif %}</td>
                    <td>{% if person.email and person.email != "" %}<a href="mailto:{{ person.email }}">{{ person.email }}</a>{% else %}—{% endif %}</td>
                  </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </section>
      {% endfor %}
    </div>
  </div>
</section>
