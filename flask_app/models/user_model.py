from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



# ? --------------------------------------
    # READ all users, display on frontend
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("recipes_schema").query_db(query)

        users = []

        for user in results:
            users.append(cls(user))
        
        return users
# ? --------------------------------------



# ? --------------------------------------
    # CREATE new user, add form data to database
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        return connectToMySQL("recipes_schema").query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
# READ one user by email address
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes_schema").query_db(query, data)

        return cls(result[0]) if result else None
# ? --------------------------------------



# ? --------------------------------------
    # user validation & regex
    @staticmethod
    def registration(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False

        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False

        # to check if an email address is already registered. Requires another classmethod, added above.
        # * need to pass in a full dictionary, not just data['email'], that won't work
        if User.get_by_email({ "email" : request.form["email"] }):
            flash("Email already taken", "register")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False

        # * for a password input and confirm password input
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Passwords need to match", "register")
            is_valid = False


        return is_valid
# ? --------------------------------------



# ? --------------------------------------
# ! can probably delete, don't need to get and display just one user for this assignment
    # READ one user by id, show on frontend
    # @classmethod
    # def get_one(cls, data):
    #     query  = "SELECT * FROM users WHERE id = %(id)s;" 
    #     result = connectToMySQL('recipes_schema').query_db(query, data)

    #     return cls(result[0]) 
# ? --------------------------------------



# ? --------------------------------------
# ! can probably delete, don't need to update user info for this assignment
    # UPDATE user with form data
    # @classmethod
    # def update_one(cls, data):
    #     query  = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;" 

    #     return connectToMySQL('recipes_schema').query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
# ! can probably delete, don't need to delete a user for this assignment
    # DELETE user
    # @classmethod
    # def remove_one(cls, data):
    #     query = "DELETE FROM users WHERE id = %(id)s;"

    #     return connectToMySQL('recipes_schema').query_db(query, data)
# ? --------------------------------------

