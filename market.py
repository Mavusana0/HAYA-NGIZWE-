{% extends "base.html" %}
{% block content %}
  <h2>Market</h2>
  <h3>Sell something</h3>
  <form method="post" enctype="multipart/form-data">
    <input name="name" placeholder="Product name" required>
    <input name="category" placeholder="Category">
    <textarea name="description" placeholder="Description"></textarea>
    <input name="price" placeholder="Price">
    <input name="seller_name" placeholder="Your name">
    <input name="seller_email" placeholder="Your email">
    <input type="file" name="image">
    <button type="submit">Post</button>
  </form>
  <hr>
  <h3>Products</h3>
  {% for id,name,category,description,price,image in products %}
    <div class="product-card">
      <h4>{{ name }} ({{ category }}) - R{{ price }}</h4>
      {% if image %}<img src="{{ image }}" style="max-width:200px">{% endif %}
      <p>{{ description }}</p>
    </div>
  {% else %}
    <p>No products yet.</p>
  {% endfor %}
{% endblock %}