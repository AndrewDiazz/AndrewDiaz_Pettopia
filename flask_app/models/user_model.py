from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'pettopia'
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Save Method
    @classmethod
    def save(cls,form_data):
        query = """INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        return connectToMySQL(db).query_db(query,form_data)

    # Get Methods
    # Get Email
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results  = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Get User id
    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    # Update Method
    @classmethod
    def update(cls,data):
        query = """UPDATE users
                SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at=NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query,data)

    # Validation Methods
    # Validation Sign in
    @staticmethod
    def val_sign_in(form_data):
        if not EMAIL_REGEX.match(form_data['email']):
            flash('Invalid email/password', 'sign_in')
            return False
        user = User.get_by_email(form_data)
        if not user:
            flash('Invalid email/password','sign_in')
            return False
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash('Invalid email/password', 'sign_in')
            return False
        return user

    # Validation Register
    @staticmethod
    def val_account(user):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!","register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirmp']:
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid

    # Updating Profile Validation
    @staticmethod
    def is_valid(user_dict):
        is_valid = True
       
        if len(user_dict['email']) < 1:
            flash("Email cannot be blank.","register")
            is_valid = False
        if not EMAIL_REGEX.match(user_dict['email']):
            flash("Invalid Email!!","register")
            is_valid = False
        if len(user_dict["first_name"]) < 2:
            flash("First Name must be at least 2 characters")
            is_valid = False
        elif len(user_dict["last_name"]) < 2:
            flash("Last Name must be at least 2 characters")
            is_valid = False
        return is_valid 
    

