{% extends "base.html" %}
{% block content %}
  <h1>{{ content }}</h1>
  <p>Language: {{ lang }}</p>
  <p><a href="/admin/login">Admin</a> | <a href="/register">Register</a></p>
{% endblock %}