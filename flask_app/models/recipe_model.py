from flask_app.config.mysqlconnection import connectToMySQL
from flask import request
from flask_app.models import user_model

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # * you don't need a list to iterate through, just one user object per recipe
        self.user = None



# ? --------------------------------------
    # READ all users, display on frontend
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL("recipes_schema").query_db(query)

        recipes = []

        for row in results:
            # * make each recipe object
            recipe = cls(row)
            # * user object
            data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": '',
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # * add user object to recipe.user attribute
            # * can now access user attributes i.e. recipe.user.first_name
            recipe.user = user_model.User(data)
            # * add completed recipe object to list
            recipes.append(recipe)
        
        return recipes
# ? --------------------------------------



# ? --------------------------------------
    # CREATE new user, add form data to database
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes (user_id, name, description, instructions, date, under_thirty) 
        VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(date)s, %(under_thirty)s);
        """

        return connectToMySQL("recipes_schema").query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
# ! probably don't need this here
# READ one user by email address
    # @classmethod
    # def get_by_email(cls, data):
    #     query = "SELECT * FROM recipes WHERE email = %(email)s;"
    #     result = connectToMySQL("recipes_schema").query_db(query, data)

    #     return cls(result[0]) if result else None
# ? --------------------------------------



# ? --------------------------------------
    # READ one user by id, show on frontend
    # ! replacing this with below method
    # @classmethod
    # def get_one(cls, data):
    #     query  = "SELECT * FROM recipes WHERE id = %(id)s;" 
    #     result = connectToMySQL('recipes_schema').query_db(query, data)

    #     return cls(result[0]) 
# ? --------------------------------------



# ? --------------------------------------
    # READ one recipe and it's user
    @classmethod
    def recipe_by_id_with_user(cls, data):
        query = """
            SELECT * FROM recipes 
            LEFT JOIN users ON users.id = recipes.user_id 
            WHERE recipes.id = %(id)s;
        """

        result = connectToMySQL("recipes_schema").query_db(query, data)

        recipe = cls(result[0])

        for row in result:
            # * user object
            data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": '',
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            recipe.user = user_model.User(data)
        
        print(recipe)
        return(recipe)
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

