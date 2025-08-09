{% extends "base.html" %}
{% block content %}
  <h2>Feedback</h2>
  <form method="post">
    <input name="name" placeholder="Your name">
    <input name="email" placeholder="Email">
    <input name="location" placeholder="Location">
    <label>Rating
      <select name="rating">
        <option>5</option><option>4</option><option>3</option><option>2</option><option>1</option>
      </select>
    </label>
    <textarea name="comments" placeholder="Comments"></textarea>
    <button type="submit">Submit</button>
  </form>
{% endblock %}