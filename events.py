{% extends "base.html" %}
{% block content %}
  <h2>Events</h2>
  {% for title,date,location,details,img in events %}
    <div class="event">
      <h3>{{ title }} — {{ date }}</h3>
      <p>{{ location }}</p>
      <p>{{ details }}</p>
    </div>
  {% else %}
    <p>No events yet.</p>
  {% endfor %}
{% endblock %}