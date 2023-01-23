from flask_app.config.mysqlconnection import connectToMySQL
from flask import request, flash
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
            # * iterate & make each recipe object
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
    # READ one recipe and it's user
    @classmethod
    # maybe rename this to just get_by_email? On the other hand, I like the descritiveness
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
    # UPDATE user with form data
    @classmethod
    def update(cls, data):
        query  = """
        UPDATE recipes 
        SET 
        name = %(name)s, 
        description = %(description)s, 
        instructions = %(instructions)s, 
        date = %(date)s, 
        under_thirty = %(under_thirty)s  
        WHERE id = %(id)s;
        """

        return connectToMySQL('recipes_schema').query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
    # DELETE user
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL('recipes_schema').query_db(query, data)
# ? --------------------------------------



# ? --------------------------------------
    # user validation
    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['name']) < 2:
            flash("Name must be at least 2 characters.", "recipe")
            is_valid = False

        if len(data['description']) < 2:
            flash("Description must be at least 2 characters.", "recipe")
            is_valid = False

        if len(data['instructions']) < 2:
            flash("Instructions must be at least 2 characters.", "recipe")
            is_valid = False

        if data['date'] == '':
            flash("Date must be added", "recipe")
            is_valid = False

        if 'under_thirty' not in data:
            flash("Is it under 30 minutes? Pick yes or no", "recipe")
            is_valid = False

        return is_valid
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