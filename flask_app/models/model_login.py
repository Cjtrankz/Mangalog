from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.acc_name = data['acc_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    #C
    @classmethod # query, call database, return
    def create(cls, data:dict) -> int:
        query = "INSERT INTO users (acc_name, email, password) VALUES (%(acc_name)s, %(email)s, %(password)s)"
        return connectToMySQL(DATABASE).query_db(query, data)


    #R
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        friends = []

        for friend in results:
            friends.append( cls(friend) )
        return friends

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return []
    
    @classmethod
    def get_one_email(cls, data:dict):
        query = "SELECT * FROM users WHERE email = %(email_login)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return User(results[0])
        return []

    #U
    @classmethod
    def update_one(cls, data:dict):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    #D
    @classmethod
    def delete_one(cls, data:dict):
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validator_registration(data:dict):
        is_valid = True

        if(len(data['acc_name'])<3):
            flash("Account name needs to be longer than 3 letters", 'err_acc_name')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'err_email')
            is_valid = False
        if(len(data['password'])<8):
            flash("Password needs to be at least 8 characters", 'err_password')
            is_valid = False
        elif(data['password'] != data['confirm_password']):
            flash("Passwords do not match", 'err_confirm_pw')
            
        return is_valid

    @staticmethod
    def validate_login(data:dict):
        is_valid = True

        if not EMAIL_REGEX.match(data['email_login']): 
            flash("Invalid email address!", 'err_email_login')
            is_valid = False
        elif(len(data['password'])<8):
            flash("Password needs to be longer than 8 letters", 'err_password_login')
            is_valid = False
        else:
            user = User.get_one_email(data)
            if user:
                if not bcrypt.check_password_hash(user.password, data['password']):
                    flash("Wrong password", 'err_wrong_pass')
                    is_valid = False
                else:
                    session['uuid']=user.id
            else:
                flash("Email does not exist", 'err_no_email')
                is_valid = False

        return is_valid