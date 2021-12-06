"""
main.py
Jamie Shearer
CS 166 / Fall 2021

A program that takes a username and password and then allows the user to
access different things based on their credentials. Usernames and passwords are
stored in plaintext in a .csv file
"""

from helpers import *

# Name of file we'll be reading from and writing to
filename = "users.csv"

# Initializing list for users
users = []

# I felt it was important to initialize this in case there's some sort of glitch then the user won't have any access
access_level = -1

# Put all the users into a users[] list
with open(filename, 'r') as csv_file:
    # Creating a csv reader object
    csv_reader = csv.reader(csv_file)

    # Extracting data
    for line in csv_reader:
        users.append(line)


# First we want to know if we should add a user or sign in.
signed_in = False

while not signed_in:
    # Keeps looping until the user signs in

    initial_choice = input("Enter 0 to create a new user or 1 to sign in: ")

    if initial_choice == "0":
        # Add a user to the CSV file and bring them back to the home screen
        add_user(users, filename)

    elif initial_choice == "1":
        # Sign in and return the access level of the user signing in
        access_level = sign_in(users)
        signed_in = True

    else:
        # Sass them for choosing the wrong option
        print("Was that a 0 or a 1?")

# They're in! Show them the menu

while True:
    print("\n======================================================================\n")
    choice = show_menu()

    if choice == "1":
        if access_level < 2:
            print("\n======================================================================\n")
            print("Sorry! You don't have access to that!")
        else:
            print("\n======================================================================\n")
            print("You have accessed accounting!")

    elif choice == "2":
        # Everyone can see this I think
        print("\n======================================================================\n")
        print("You have accessed the receiving department!")

    elif choice == "3":
        # Obviously only admins have access to this
        if access_level < 3:
            print("\n======================================================================\n")
            print("Sorry! You don't have access to this!")
        else:
            print("\n======================================================================\n")
            print("WHoooooooooooie this is a secret! Come see me later and I'll tell you where the last unicorn is.")

    elif choice == "4":
        # Everyone can see my grocery list
        print("\n======================================================================\n")
        print("Just have to buy ice cream. I always need ice cream.")

    elif choice == "5":
        exit(0)

    else:
        print("Choose a valid option please!")
