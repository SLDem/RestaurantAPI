<h1>Test task for "RestaurantAPI"</h1>

To run the application:
1. Clone the repository to your local machine.
2. Run `pip install -r requirements.txt` to install requirements.
3. Run a PostgreSQL instance on port 5432 and create a database named **restaurantapidb** with user **postgres** and password **postgres**.
4. Run `python manage.py makemigrations` > `python manage.py migrate` to migrate your **db**.
5. Run `python manage.py runserver` to run the application.
6. Run `python manage.py createsuperuser` or go to `http://127.0.0.1:8000/signup` to create a user.
7. Login at `http://127.0.0.1:8000/login`.
8. Run test with `pytest` command.

<h3>List of available api's:</h3>

`employees/` > get list of all employees/users and add a new employee/user.

`restaurants/` > get list of all restaurants and add a new restaurant.

`restaurant/<int:pk>/` > get info about a specific restaurant, its menu and its items.

`menus/<int:pk>/` > get info about all menus that belong to a specific restaurant.

`menu_items/<int:pk>/` > get info about all menu items in a specific menu.

`create_menu/<int:pk>/` > create a menu for a restaurant with items.

`current_day_menu/<int:pk>/` > get a current day menu for a restaurant.
