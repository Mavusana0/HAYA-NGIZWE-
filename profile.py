{% extends "base.html" %}
{% block content %}
  <h2>Profile</h2>
  <form method="post">
    <input name="name" value="{{ user[1] }}">
    <textarea name="bio">{{ user[3] }}</textarea>
    <button type="submit">Save</button>
  </form>
{% endblock %}