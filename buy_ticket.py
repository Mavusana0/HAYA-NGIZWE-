{% extends "base.html" %}
{% block content %}
  <h2>Buy Ticket for Event {{ event_id }}</h2>
  <form method="post">
    <input name="name" placeholder="Your name" required>
    <input name="email" placeholder="Email" required>
    <input name="seat" placeholder="Seat (optional)">
    <button type="submit">Buy</button>
  </form>
{% endblock %}