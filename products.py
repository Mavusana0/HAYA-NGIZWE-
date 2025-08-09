{% extends "base.html" %}
{% block content %}
  <h2>Products</h2>
  {% for id,name,category,description,price,image in items %}
    <div class="prod">
      <h4>{{ name }} - R{{ price }}</h4>
      {% if image %}<img src="{{ image }}" style="max-width:160px">{% endif %}
      <form method="post" action="/add_to_cart/{{ id }}">
        <input type="number" name="quantity" value="1" min="1">
        <button type="submit">Add to cart</button>
      </form>
    </div>
  {% else %}
    <p>No items.</p>
  {% endfor %}
{% endblock %}