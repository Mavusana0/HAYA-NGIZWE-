{% extends "base.html" %}
{% block content %}
  <h2>Services</h2>
  {% for t,d in services %}
    <article class="service-card">
      <h3>{{ t }}</h3>
      <p>{{ d }}</p>
    </article>
  {% else %}
    <p>No services added yet.</p>
  {% endfor %}
{% endblock %}