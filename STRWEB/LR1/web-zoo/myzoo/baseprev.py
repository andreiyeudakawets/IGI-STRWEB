"""

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Zoo Management</title>
</head>
<body>
  <header>
    <nav>
      <ul>
        <li><a href="/">ZooManagement</a></li>
        <li><a href="/about">About</a></li>
        <li><a href="{% url 'mainapp:news' %}">News</a></li>
        <li><a href="{% url 'mainapp:codes' %}">Promocodes</a></li>
        <li><a href="/employees">Contacts</a></li>
        <li><a href="/reviews">Reviews</a></li>
      </ul>

      {% if us_gr == 'worker' %}
          <p>Вы являетесь работником.</p>
      {% elif us_gr == 'customer' %}
          <p>Вы являетесь клиентом.</p>
      {% else %}
        {% if user.is_authenticated %}
          <p>Вы суперпользователь.</p>
        {% else %}
          <p>Вы неавторизованный пользователь.</p>
        {% endif %}

      {% endif %}

      <ul>
        <li><a href="/animals">View All Animals</a></li>
        <li><a href="/rooms">View all rooms</a></li>

        <li><a href="{% url 'users:agify' %}">Agify api</a></li>
        <li><a href="{% url 'users:cat_facts' %}">Random facts api</a></li>

        {% if us_gr == 'worker' %}
          <li><a href="/employees/animals">View my animals</a></li>
        {% endif %}

        {% if user.is_superuser %}
          <li><a href="/employees">View All Employees</a></li>
          <li><a href="/animals/animal_family_population">Info by class</a></li>
          <li><a href="{% url 'users:customers' %}">All customers</a></li>
          <li><a href="{% url 'tickets:codes' %}">All promocodes</a></li>
        {% endif %}
      </ul>

      <ul>
        {% if user.is_authenticated %}
          <li>User: {{ user.get_username }}</li>

          <li><a href="/user/logout">Logout</a></li>
          {% if us_gr == 'customer' %}
<!-- <li><a href="/user/profile/{{user.pk}}">Profile</a></li> -->
            <li><a href="/user/profile">Profile</a></li>
            <li><a href="/tickets/buy-ticket">Buy ticket</a></li>
            <li><a href="/tickets/user-tickets">History</a></li>
          {% elif us_gr == 'worker' %}
            <li><a href="/user/profile">Profile</a></li>
          {% else %}

          {% endif %}
        {% else %}
          <li><a href="/user/register">Register</a></li>
          <li><a href="/user/login">Login</a></li>
          <li><a href="/tickets/">Check price</a></li>
        {% endif %}


      </ul>
    </nav>
  </header>
  <main>
    {% block content %}
    {% endblock %}
  </main>
  <footer>
    <div>2024 Zoo by Andrei Yeudakavets, 253505</div>
  </footer>
</body>
</html>
--------------------------


<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Zoo Management</title>
</head>
<body>
  <header>
    <h1>ZooManagement</h1>
    <nav>
      <div class="menu">
        <a href="/">Home</a> |
        <a href="/about">About</a> |
        <a href="{% url 'mainapp:news' %}">News</a> |
        <a href="{% url 'mainapp:codes' %}">Promocodes</a> |
        <a href="/employees">Contacts</a> |
        <a href="/reviews">Reviews</a>
        <a href="{% url 'users:agify' %}">Agify API</a> |
        <a href="{% url 'users:cat_facts' %}">Random Facts API</a>
      </div>

      <div class="user-info">
        {% if user.is_authenticated %}
          <p>Welcome, {{ user.get_username }}!</p>
          <a href="/user/logout">Logout</a>
          {% if us_gr == 'customer' %}
            <a href="/user/profile">Profile</a> |
            <a href="/tickets/buy-ticket">Buy ticket</a> |
            <a href="/tickets/user-tickets">History</a>
          {% elif us_gr == 'worker' %}
            <a href="/user/profile">Profile</a> |
            <a href="/employees/animals">View my animals</a>
          {% else %}
            <p>You are a superuser.</p>
          {% endif %}
        {% else %}
          <p>You are not logged in.</p>
          <a href="/user/register">Register</a> |
          <a href="/user/login">Login</a> |
          <a href="/tickets/">Check price</a>
        {% endif %}
      </div>
    </nav>
  </header>

  <main>
    {% block content %}
    {% endblock %}
  </main>

  <footer>
    <div>2024 Zoo by Andrei Yeudakavets, 253505</div>
  </footer>
</body>
</html>

"""