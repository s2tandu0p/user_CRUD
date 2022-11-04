from pprint import pprint
from flask import render_template, request, redirect, session
from models.model_user import User
from __init__ import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# a route for user registration


@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "username": request.form['username'],
        "password": pw_hash,
    }
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(f"password hash {data.password}")
    # call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/")


# a route to display all users
@app.route('/')
def index():
    users = User.get_all()
    # for user in users:
    #     pprint(user.created_at)
    session.clear()
    return render_template('index.html', users=users)


@app.route('/addd_user')
def add_user():
    if not session:
        session['first_name'] = ""
        session['last_name'] = ""
    return render_template('addd_user.html', first_name=session['first_name'], last_name=session['last_name'])


# a route when a user is created ont the webpage


@ app.route('/create', methods=['POST'])
def create():
    print(request.form)

    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    # first we make a data dictionary from our request.form coming from the webpage
    # the keys in "data" - the data dictionary that we are going to pass to model
    # to run the query - needs to be exactly the same as the variables in our
    # query prepared statement.
    data = {
        'first_name': session['first_name'],
        'last_name': session['last_name'],
        'email': request.form['email'],
    }
    print(f"session {session}")
    print(f"data {data}")
    # if there are errors:
    # we call the staticmethod on User model to validate
    if not User.validate_user(request.form):
        # redirect to the route where the error message is rendered
        return redirect('/addd_user')
    # now we call the "save" class method from the model
    User.save(data)
    # session.clear()
    # and don't forget to redirect - POST no render_template
    # need to display what's been saved on '/'
    return redirect('/')

# a rout to a page when add user button is clicked


# a route to edit a user


@ app.route('/edit_user/<int:id>')
def edit_user(id):
    data = {
        'id': id,
    }
    user = User.get_user_info(data)
    print(user.first_name)

    # now we call the "save" class method from the model
    return render_template('edit_user.html', user=user)


# a route to show details of a user


@ app.route('/show_user/<int:id>')
def show_user(id):
    data = {
        'id': id,
    }
    user = User.get_user_info(data)
    return render_template('user_detail.html', user=user)


# a route to delete a user


@ app.route('/destroy_user/<int:id>')
def destroy_user(id):
    data = {
        'id': id,
    }
    user = User.destroy_user(data)
    return redirect('/')

# a route to update the user after the edit and redirect back to home page


@ app.route('/update_user', methods=['POST'])
def update_user():
    print(request.form)
    # if there are errors:
    # we call the staticmethod on User model to validate
    # if not User.validate_user(request.form):
    #     # redirect to the route where the error message is rendered
    #     return redirect(request.referrer)
    User.update_user(request.form)
    return redirect('/')
