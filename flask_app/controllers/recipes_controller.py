from flask_app import app
from flask import render_template, redirect, request, flash, session
# from flask_app.controllers import users_controller
from flask_app.models import user_model, recipe_model

# ? --------------------------------------
# recipes page
@app.route('/recipes') 
def to_recipes_page():

    # this is working just fine now, at http://127.0.0.1:5000/ on Firefox. No clue what was going on with previous assignment
    # to stop someone from typing /recipes if they are not logged in
    if 'user_id' not in session:
        return redirect('/')

    # never tested, but does this work like the above code?
    # if not session['user_id']:
    #     return redirect('/')

    return render_template("recipes.html", recipes = recipe_model.Recipe.get_all()) 
# ? --------------------------------------



# ? --------------------------------------
# To form page
@app.route('/add') 
def add_form():
    # to stop someone from typing /add if they are not logged in
    if 'user_id' not in session:
        return redirect('/')

    return render_template("add.html")
# ? --------------------------------------



# ? --------------------------------------
# CREATE recipe, POST data
@app.route('/add', methods=['POST']) 
def create():
    recipe_model.Recipe.save(request.form)

    return redirect("/recipes")
# ? --------------------------------------



# ? --------------------------------------
# READ one recipe, show on frontend
@app.route('/view/<int:id>') 
def view(id):
    data = { 
        "id": id 
    }

    # to stop someone from typing /view/2 if they are not logged in
    if 'user_id' not in session:
        return redirect('/')

    return render_template("view.html", recipe = recipe_model.Recipe.recipe_by_id_with_user(data))  
# ? --------------------------------------
