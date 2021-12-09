# CS166-final
## General Overview
Final project for CS166

This is meant to be a little website for a business. You start with a screen prompting you to either sign in or sign up.

Signing up won't let you choose an insecure password so watch out for that. It needs a lower-case letter, upper-case 
letter, special character, and a number. It also gives everyone the lowest access level, by default.
The only login credentials without the lowest level or access are: 

admin, admin (access level 3)

Jamie, password (access level 3)

Harry, dragon (access level 2)

Everyone else is access level 1. This is for security. You can't just have people choosing their own access levels whenever.

## Security measures
This is not vulnerable to XSS or SQL injection. Obviously I'm not a master hacker, but I was unable to see any place
where the app was vulnerable. I also attempted both attacks in the username fields and couldn't get it to work.

The passwords are also hashed and salted in the database, just in case there is any data leak.