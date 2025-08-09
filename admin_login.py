{% extends "base.html" %}
{% block content %}
  <h2>Admin Login</h2>
  <form method="post">
    <input name="username" placeholder="username">
    <input name="password" placeholder="password" type="password">
    <button type="submit">Login</button>
  </form>
{% endblock %}