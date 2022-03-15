from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import model_login
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Manga:
    def __init__( self , data ):
        self.id = data['id']
        self.dex_id = data['dex_id']
        self.chapters_read = data['chapters_read']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []

    #C
    @classmethod # query, call database, return
    def follow(cls, data:dict) -> int:
        query = "INSERT INTO mangas (dex_id, chapters_read, user_id) VALUES (%(dex_id)s, 0, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)


    #R
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM mangas;"
        results = connectToMySQL(DATABASE).query_db(query)
        friends = []

        for friend in results:
            friends.append( cls(friend) )
        return friends


    @classmethod
    def get_mag_users(cls):
        query = "SELECT * FROM mangas m LEFT JOIN users u ON u.id = m.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if not results:
            return []
        all_mangas = []
        for row in results:
            manga = cls(row)
            data = {
                    'id':row['u.id'],
                    'acc_name':row['acc_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'updated_at':row['u.updated_at'],
                    'created_at':row['u.created_at']
            }
            manga.users.append(model_login.User(data))
            all_mangas.append(manga)
        return all_mangas

    @classmethod
    def mag_name(cls, data:dict):
        query = "SELECT acc_name FROM users u JOIN mangas m ON u.id = m.user_id WHERE m.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return results[0]
        return []

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM mangas WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return []

    @classmethod
    def get_all_mangas(cls, data:dict):
        query = "SELECT * FROM mangas WHERE user_id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        friends = []
        if not results:
            return []
        for friend in results:
            friends.append(cls(friend))
        return friends
    
    #U
    @classmethod
    def update_one(cls, data:dict):
        query = "UPDATE mangas SET title=%(title)s, description=%(description)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update_num_ch_read(cls, data:dict):
        query = "UPDATE mangas SET chapters_read=%(chapters_read)s WHERE id=%(id)s && user_id=%(user_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    #D
    @classmethod
    def unfollow(cls, data:dict):
        query = "DELETE FROM mangas WHERE id = %(id)s && user_id=%(user_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    # @staticmethod
    # def validator_mag(data:dict):
    #     is_valid = True
    #     if(len(data['title'])<=2):
    #         flash("Title must be at least 2 characters", 'err_title')
    #         is_valid = False
    #     if(len(data['description'])<=10):
    #         flash("Description must be at least 10 characters", 'err_description')
    #         is_valid = False
    #     return is_valid

    @staticmethod
    def validate_follow(data:dict):
        is_valid = True
        query = "SELECT * FROM mangas WHERE dex_id = %(dex_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if(results):
            is_valid = False
            flash("Already following this manga. Pick something new!", 'err_follow_val')
        else:
            flash("Added to follows", 'err_follow_val')
        return is_valid

    @staticmethod
    def validator_user_update(data:dict):
        is_valid = True
        if(len(data['acc_name'])<3):
            flash("Account name needs to be longer than 3 letters", 'err__acc_name')
            is_valid = False
        # if(len(data['email'])<2):
        #     flash("Email needs to be longer than 2 letters", 'err_email')
        #     is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'err_email')
            is_valid = False
        return is_valid