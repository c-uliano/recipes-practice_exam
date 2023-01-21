from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models import user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ? --------------------------------------
# Homepage
@app.route('/add') 
def add_form():
    return redirect("/")
# ? --------------------------------------

