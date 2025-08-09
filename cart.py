{% extends "base.html" %}
{% block content %}
  <h2>Your Cart</h2>
  {% if cart %}
    <ul>
    {% for pid, item in cart.items() %}
      <li>{{ item.name }} x {{ item.quantity }} — R{{ item.price * item.quantity }}</li>
    {% endfor %}
    </ul>
    <p>Total: R{{ total }}</p>
    <a href="/checkout">Checkout</a>
  {% else %}
    <p>Your cart is empty.</p>
  {% endif %}
{% endblock %}