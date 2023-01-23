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

    return render_template("home.html", recipes = recipe_model.Recipe.get_all()) 
# ? --------------------------------------



# ? --------------------------------------
# To form page
@app.route('/add') 
def create_form():
    # to stop someone from typing /add if they are not logged in
    if 'user_id' not in session:
        return redirect('/')

    return render_template("add.html")
# ? --------------------------------------



# ? --------------------------------------
# CREATE recipe, POST data
@app.route('/add', methods=['POST']) 
def create():
    if not recipe_model.Recipe.validate(request.form):
        return redirect("/add")

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



# ? --------------------------------------
# READ one recipe, show on frontend in filled-out form
@app.route('/update/<int:id>') 
def uppdate_form(id):
    data = { 
        "id": id 
    }

    # to stop someone from typing /edit/2 if they are not logged in
    if 'user_id' not in session:
        return redirect('/')

    return render_template("update.html", recipe = recipe_model.Recipe.recipe_by_id_with_user(data))  
# ? --------------------------------------



# ? --------------------------------------
# UPDATE one recipe
@app.route('/update/<int:id>', methods=['POST']) 
def update(id):
    if not recipe_model.Recipe.validate(request.form):
        return redirect(f"/update/{id}")

    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'under_thirty': request.form['under_thirty'],
    }

    recipe_model.Recipe.update(data)

    return redirect(f"/view/{id}")  
# ? --------------------------------------



# ? --------------------------------------
# DELETE recipe
@app.route('/delete/<int:id>') 
def delete(id):

    data ={ 
        "id": id
    }

    recipe_model.Recipe.delete(data)

    return redirect("/recipes")  
# ? --------------------------------------