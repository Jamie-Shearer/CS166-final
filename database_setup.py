# This program just creates the database and populates it with some initial values

from helpers import create_db, query_db
import sqlite3

users = []

users = query_db(users)

conn = sqlite3.connect('user.db')
c = conn.cursor()
