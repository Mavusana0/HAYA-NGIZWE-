{% extends "base.html" %}
{% block content %}
  <h2>Poetry Slam Registration</h2>
  <form method="post">
    <input name="name" placeholder="Full name" required>
    <input name="email" placeholder="Email" required>
    <input name="phone" placeholder="Phone">
    <input name="location" placeholder="Location">
    <textarea name="bio" placeholder="Short bio"></textarea>
    <button type="submit">Register</button>
  </form>
{% endblock %}