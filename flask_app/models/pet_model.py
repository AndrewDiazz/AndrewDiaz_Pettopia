from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask_app.models import post_model
from flask import flash




class Pet:
    db = "pettopia"
    def __init__(self,data):
        self.id = data['id']
        self.pet_name= data['pet_name']
        self.age= data['age']
        self.type= data['type']
        self.breed= data['breed']
        self.description= data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    # Get Methods
    @classmethod
    def get_all_with_user(cls):
        query = "SELECT * FROM pets JOIN users ON pets.user_id = users.id;"
        results =  connectToMySQL(cls.db).query_db(query)

        all_pets = []


        for row in results:
            pet = cls(row)
            data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            pet.user = user_model.User(data)
            all_pets.append(pet)
        return all_pets

    @classmethod
    def get_one_with_user(cls,pet_id):
        query = "SELECT * FROM pets JOIN users ON pets.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,pet_id)

        all_pets = []

        for row in results:
            pet = cls(row)
            data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            pet.user = user_model.User(data)
            all_pets.append(pet)
        return all_pets

    @classmethod
    def get_pet_id(cls,pet_id):
        query = "SELECT * FROM pets WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,pet_id)
        return results[0]

    # Save Pet
    @classmethod
    def save(cls,form_data):
        query = """INSERT INTO pets (pet_name, age, type, breed, description, user_id) VALUES (%(pet_name)s, %(age)s, %(type)s, %(breed)s, %(description)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query,form_data)

    # Update Pet
    @classmethod
    def pet_update(cls,pet_data):
        query = "UPDATE pets SET pet_name=%(pet_name)s,age=%(age)s,type=%(type)s,breed=%(breed)s,description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, pet_data)

    # Delete Pet
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pets WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)

    # Form Validation
    @staticmethod
    def val_pet(form_data):
        is_valid = True
        if len(form_data["pet_name"]) < 2:
            flash("pet_name must be at least 2 characters!!", "pet")
            is_valid = False
        if len(form_data["age"]) == 0:
            flash("your pet must have an age!!", "pet")
            is_valid = False
        if len(form_data["type"]) == 0:
            flash("please enter TYPE of pet!!", "pet")
            is_valid = False
        if len(form_data["breed"]) < 1:
            flash("please enter pet BREED!!", "pet")
            is_valid = False
        if len(form_data["description"]) < 20:
            flash("description must be at least 20 characters or more!!", "pet")
            is_valid = False
        return is_valid
