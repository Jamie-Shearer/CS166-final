# This program just creates the database and populates it with some initial values

# WARNING: Enable admin override in helpers.add_user() before running

from helpers import create_db, add_user

create_db()

# users = query_db()

add_user("Jamie", "password", 3)
add_user("admin", "admin", 3)
add_user("Harry", "dragon", 2)
add_user("James", "bbkat2", 1)
add_user("Sam", "Tovah68", 1)
add_user("Liviya", "bbkat3", 1)
