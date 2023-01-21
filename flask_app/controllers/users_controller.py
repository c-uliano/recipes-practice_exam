from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models import user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ? --------------------------------------
# Homepage
@app.route('/') 
def index():
    return render_template("index.html")  
# ? --------------------------------------



# ? --------------------------------------
# CREATE, validate, hash, redirect to recipes page
@app.route('/register', methods=['POST']) 
def register():

    if not user_model.User.registration(request.form):
        return redirect("/")

    data = {
        "password": bcrypt.generate_password_hash(request.form['password']),
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
    }

    user_model.User.save(data)

    # need this to redirect to /recipes or else it just reloads the homepage because of the if statement in the /recipes route, and because there was no session saved. Can't save session without pulling the user. Can't pull user info when user is just being created, have to create then call.
    user = user_model.User.get_by_email({"email": request.form['email']})
    session['user_id'] = user.id
    # to show user's name on the recipe page after they register
    session['first_name'] = user.first_name

    return redirect('/recipes') 
# ? --------------------------------------



# ? --------------------------------------
# READ user by email, redirect to success page
@app.route('/login', methods=['POST']) 
def login():
    data = { 
        "email" : request.form["email"] 
    }

    user = user_model.User.get_by_email(data)

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']): 
        flash("Invalid Credentials", "login")
        return redirect('/')

    # to determine if someone is logged in. No idea where the 'user_id' in session['user_id'] is coming from, guess it's just whatever you want to call it?
    session['user_id'] = user.id
    # to show user's name on the recipe page after they log in
    session['first_name'] = user.first_name


    return redirect("/recipes") 
# ? --------------------------------------



# ? --------------------------------------
# redirect successful registration to success page
@app.route('/recipes') 
def to_recipes_page():

    # this is working just fine now, at http://127.0.0.1:5000/ on Firefox. No clue what was going on with previous assignment
    if 'user_id' not in session:
        return redirect('/')

    # never tested, but does this work like the above code?
    # if not session['user_id']:
    #     return redirect('/')

    return render_template("recipes.html", users = user_model.User.get_all()) 
# ? --------------------------------------



# ? --------------------------------------
# logout, redirect to homepage
@app.route('/logout') 
def logout():
    session.clear()
    return redirect("/")
# ? --------------------------------------
