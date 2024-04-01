from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import pet_model
from flask import flash

class Post:
    db = "pettopia"
    def __init__(self,data):
        self.id = data['id']
        self.comment= data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pet_id = data['pet_id']
        self.pet = None

    # Save Comment Method
    @classmethod
    def save(cls,pet_comment):
        query = """INSERT INTO posts (comment, pet_id) VALUES (%(comment)s, %(pet_id)s);"""
        return connectToMySQL(cls.db).query_db(query,pet_comment)

    # Delete Comment Method
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    # Get Methods
    @classmethod
    def get_one_with_pet(cls,id):
        query = "SELECT * FROM posts JOIN pets ON posts.pet_id = pets.id WHERE pets.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,id)

        all_posts = []

        for row in results:
            post = cls(row)
            data = {
                "id": row["pets.id"],
                "pet_name": row["pet_name"],
                "age": row["age"],
                "type": row["type"],
                "breed": row["breed"],
                "description": row["description"],
                "created_at": row["pets.created_at"],
                "updated_at": row["pets.updated_at"],
                "user_id": row["user_id"]
            }
            post.pet = pet_model.Pet(data)
            all_posts.append(post)
        return all_posts

    @classmethod
    def get_all_with_pets(cls):
        query = "SELECT * FROM posts JOIN pets ON posts.pet_id = pets.id;"
        results =  connectToMySQL(cls.db).query_db(query)

        all_posts = []


        for row in results:
            post = cls(row)
            data = {
                "id": row["pets.id"],
                "pet_name": row["pet_name"],
                "age": row["age"],
                "type": row["type"],
                "breed": row["breed"],
                "description": row["description"],
                "created_at": row["pets.created_at"],
                "updated_at": row["pets.updated_at"],
                "user_id": row["user_id"]
            }
            post.pet = pet_model.Pet(data)
            all_posts.append(post)
        return all_posts

    # Validation Method
    @staticmethod
    def val_comment(pet_comment):
        is_valid = True
        if len(pet_comment["comment"]) < 10:
            flash("post must be at least 10 characters or more!!", "comment")
            is_valid = False
        if len(pet_comment["comment"]) >= 10:
            flash("Success! Make another comment!", "comment")
            is_valid = True
        return is_valid