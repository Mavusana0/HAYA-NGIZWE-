{% extends "base.html" %}
{% block content %}
  <h2>Checkout</h2>
  <p>Total: R{{ total }}</p>
  <form method="post">
    <input name="name" placeholder="Full name">
    <input name="email" placeholder="Email">
    <button type="submit">Pay (placeholder)</button>
  </form>
{% endblock %}