{% extends "base.html" %}
{% block content %}
  <h2>Contact</h2>
  <form method="post">
    <input name="name" placeholder="Your name" required>
    <input name="email" placeholder="Email" required>
    <input name="phone" placeholder="Phone">
    <textarea name="message" placeholder="Message" required></textarea>
    <button type="submit">Send</button>
  </form>
{% endblock %}