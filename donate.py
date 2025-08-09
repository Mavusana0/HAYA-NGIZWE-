{% extends "base.html" %}
{% block content %}
  <h2>Donate</h2>
  <form method="post">
    <input name="name" placeholder="Your name" required>
    <input name="email" placeholder="Email">
    <input name="amount" placeholder="Amount (ZAR)">
    <select name="payment_method"><option value="offline">Offline</option><option value="payfast">PayFast</option></select>
    <textarea name="message" placeholder="Message (optional)"></textarea>
    <button type="submit">Donate</button>
  </form>
{% endblock %}