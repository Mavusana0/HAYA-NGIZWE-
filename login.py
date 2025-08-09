{% extends "base.html" %}
{% block content %}
  <h2>Login</h2>
  <form method="post" action="/user/login">
    <input name="email" placeholder="Email">
    <input name="password" placeholder="Password" type="password">
    <button type="submit">Login</button>
  </form>
{% endblock %}