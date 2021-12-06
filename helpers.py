# This file just has the functions I'll need for the project. They were getting in my way
import csv
import sys
import hashlib
from random import choice
import sqlite3
import os
from base64 import b64encode
from datetime import datetime

MAX_PASSWORD_LENGTH = 25
MIN_PASSWORD_LENGTH = 8
SALT_LENGTH = 40


def generate_secure(length=MAX_PASSWORD_LENGTH):
    """ "strong password generator" feature """
    secure = ""
    while len(secure) < length:
        character = choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890<>?=+-!@#$%^&*")
        secure += character
    return secure


def validate(password):
    """ password validation -
       8-25 characters
       At least one:
        number
        special character
        upper-case letter
        lower-case letter"""
    valid = False
    upper = False
    lower = False
    num = False
    spec = False

    for i in password:
        if not valid:
            if i.isupper():
                upper = True
            elif i.islower():
                lower = True
            elif i.isdigit():
                num = True
            else:
                spec = True

            if upper and lower and spec and num and len(password) >= MIN_PASSWORD_LENGTH and len(password) <= MAX_PASSWORD_LENGTH:
                # Stop this early if everything has been satisfied
                valid = True

    return valid


def add_user(users, filename):
    """ Function to add a user to the CSV file """
    # Make a list of usernames to compare against
    usernames = []
    for user in users:
        usernames.append(user[0])

    name = ""
    while name not in usernames:
        name = input("Choose a username: ")
        if name in usernames:
            print("Sorry! That name is taken. Choose a different one!")

        else:
            usernames.append(name)

    choose_default = ""
    while choose_default != "0" and choose_default != "1":
        choose_default = input("Enter 1 to choose your own password or 0 to use the default generator")

        if choose_default == "0":
            password = generate_secure()
        elif choose_default == "1":
            valid = False

            while not valid:
                password = input("Choose a password. It must have an upper-case letter, lower-case letter, special char"
                                 "acter, and a number. Minimum password length = 8, max length = 25: ")

                # validate the password
                valid = validate(password)
                if len(password) < MIN_PASSWORD_LENGTH:
                    print("Password is too short! Please choose a longer password\n")
                elif len(password) > MAX_PASSWORD_LENGTH:
                    print("Password is too long! Go easy on yourself!\n")

    access_level = 1        # Set to the lowest access level by default

    # New user is all set to be added to the file
    # TODO: hash password and add the hash to the file instead of the plaintext password

    new_user = [name, password, access_level]
    with open(filename, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Add the new user to the file
        csv_writer.writerow(new_user)



def sign_in(users):
    """ sign_in() won't let you past it until you provide a username and password that are in users
        Returns access level of active user """
    # A flag to indicate whether the user has logged in successfully
    verified = False
    attempts = 0

    while not verified and attempts < 3:
        attempts += 1
        # Initially ask for username and passwords
        username = input("Username: ")
        password = input("Password: ")
        # TODO: Hash inputted password, check that against hashed password in users.csv

        for user in users:
            # Determine if this user is in the users file
            if username == user[0]:
                if password == user[1]:
                    verified = True
                    print("You're in!")
                    return int(user[2])
                else:
                    print("Access Denied!")

    # Only gets here if all attempts are used
    print("Too many log in attempts!")
    sys.exit(0)


def show_menu():
    """ Simply show the menu """
    print("1: Accounting")
    print("2: Receiving")
    print("3: Location of the last unicorn")
    print("4: Grocery list")
    print("5: Log out")
    choice = input("Input the number of the option you want to see: ")
    return choice


def create_db():
    """ Create table 'users' in 'user' database """
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users
                    (
                    name text,
                    password text,
                    access_level text,
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def hash_pw(plain_text, salt='') -> str:
    """
    Generate hash of plain text. Here we allow for passing in a salt
    explicitly. This is so you can tinker and see the results.

    Python's Hashlib provides all we need here. Documentation is at
    https://docs.python.org/3/library/hashlib.html.

    Here we use SHA-1. (Weak!) For stronger encryption, see: bcrypt,
    scrypt, or Argon2. Nevertheless, this code should suffice for an
    introduction to some important concepts and practices.

    A few things to note.

    If we supply a fixed salt (or don't use a salt at all), then the
    output of the hash function becomes predictable -- for a given
    algorithm, the same password will always produce the same result.

    If we allow our algorithm to generate a salt from a pseudorandom
    input (e.g., using os.urandom(60)) then the same password will
    produce different results. All we know is the length of the combined
    salt and password.

    If we wish to be able to authenticate, then we must store the salt
    with the hash. We facilitate this by prepending the salt to the hash.

    :param plain_text: str (user-supplied password)
    :param salt: str
    :return: str (ASCII-encoded salt + hash)
    """
    if salt == '':
        salt_bytes = os.urandom(SALT_LENGTH)
        salt = b64encode(salt_bytes).decode('utf-8')

    hashable = salt + plain_text  # concatenate salt and plain_text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash w/ SHA-1 and hexdigest
    return salt + this_hash  # prepend hash and return
