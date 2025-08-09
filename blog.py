{% extends "base.html" %}
{% block content %}
  <h2>Blog</h2>
  {% for title,content,image,post_date in posts %}
    <article class="post">
      <h3>{{ title }}</h3>
      <p>{{ content }}</p>
      <p><small>{{ post_date }}</small></p>
    </article>
  {% else %}
    <p>No posts yet.</p>
  {% endfor %}
{% endblock %}