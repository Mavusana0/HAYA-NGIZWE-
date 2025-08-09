{% extends "base.html" %}
{% block content %}
  <h2>Register</h2>
  <form method="post">
    <input name="name" placeholder="Full name">
    <input name="email" placeholder="Email">
    <input name="password" placeholder="Password" type="password">
    <textarea name="bio" placeholder="Bio"></textarea>
    <button type="submit">Register</button>
  </form>
{% endblock %}