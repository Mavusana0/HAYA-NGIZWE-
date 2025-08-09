{% extends "base.html" %}
{% block content %}
  <h2>Gallery</h2>
  {% for title,img,video,desc in items %}
    <div class="gallery-item">
      <h4>{{ title }}</h4>
      {% if img %}<img src="{{ img }}" alt="{{ title }}" style="max-width:300px;">{% endif %}
      {% if video %}<p>Video: <a href="{{ video }}" target="_blank">Watch</a></p>{% endif %}
      <p>{{ desc }}</p>
    </div>
  {% else %}
    <p>No media yet.</p>
  {% endfor %}
{% endblock %}