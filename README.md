## Project 1 - Books
### Enda McCarthy
#### Web Programming with Python and JavaScript

I set this project up using blueprints.
The 3 blueprints I used are main, users and errors.
- In the main directory are the routes for the home page, book page, contact page and the API request page. The forms for searching books and reviewing books are also here.
- In the users directory are the routes for registering, logging in and logging out. The forms for registration and logging in are also here.
- The error directory contains a route for a 404 error handling function.

The app is created in the init.py file using a function.

The books table is created in import.py. The users and reviews tables are created within the create_app function.

The reviews table references the books table for isbn numbers and the users table for usernames.