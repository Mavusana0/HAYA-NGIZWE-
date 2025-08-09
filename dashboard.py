{% extends "base.html" %}
{% block content %}
  <h2>Admin Dashboard</h2>
  <p>Contacts: {{ contacts }} | Registrations: {{ regs }} | Products: {{ products }}</p>
{% endblock %}