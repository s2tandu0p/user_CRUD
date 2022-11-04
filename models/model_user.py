# import the function that will return an instance of the connection class
from config.mysqlconnection import connectToMySQL
from flask import flash
from __init__ import app
from flask_bcrypt import Bcrypt
# creating an object called bcrypt
# which is made by invoking the function Bcrypt with our app as an argument
bcrypt = Bcrypt(app)


class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # now we use a class method to query our database
    # when get_all, put them in a list
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        result = connectToMySQL('user_cr').query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users

    # class method to save input from the website to the database
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, username, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(username)s,%(password)s);'
        # connect to the database and pass the data in
        # notice how i have data in query_db() but only query in query_db()
        # because the one above is only getting the data
        return connectToMySQL('user_cr').query_db(query, data)

    # class method to get one user from the database
    @classmethod
    def get_user_info(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL('user_cr').query_db(query, data)
        return cls(result[0])

    # class method to update a user
    @classmethod
    def update_user(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;'

        return connectToMySQL('user_cr').query_db(query, data)

    # a class method to destroy a user
    @classmethod
    def destroy_user(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL('user_cr').query_db(query, data)

    # a static method for validation
    @staticmethod
    def validate_user(user):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL('user_cr').query_db(query)
        db_email = []
        for row in users_from_db:
            db_email.append(row['email'])
        print("================================================================")
        print(db_email)
        is_valid = True  # we assume this is true that the code after can run
        if (len(user['first_name'])) == 0:
            flash("First Name is required")
            is_valid = False
        if (len(user['last_name'])) == 0:
            flash("Last Name is required")
            is_valid = False
        if len(user['email']) == 0:
            flash("email is required.")
            is_valid = False
        if user['email'] in db_email:
            flash("Pick a different email")
            is_valid = False
        return is_valid

    # a static method for validation
    @staticmethod
    def validate_user_edit(user):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL('user_cr').query_db(query)
        db_email = []
        for row in users_from_db:
            db_email.append(row['email'])
        print("================================================================")
        print(db_email)
        is_valid = True  # we assume this is true that the code after can run
        if (len(user.first_name)) == 0:
            flash("First Name is required")
            is_valid = False
        if (len(user.last_name)) == 0:
            flash("Last Name is required")
            is_valid = False
        if len(user.email) == 0:
            flash("email is required.")
            is_valid = False
        if user.email in db_email:
            flash("Pick a different email")
            is_valid = False
        return is_valid
