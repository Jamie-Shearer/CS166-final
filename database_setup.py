# This program just creates the database and populates it with some initial values

from helpers import create_db, query_db, add_user

create_db()

users = []

users = query_db(users)

add_user("Jamie", "password", 3)
add_user("admin", "admin", 3)
add_user("Harry", "dragon", 2)
add_user("James", "bbkat2", 1)
add_user("Sam", "Tovah68", 1)
add_user("Liviya", "bbkat3", 1)
