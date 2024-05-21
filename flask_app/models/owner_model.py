from flask import flash
from pprint import pprint
from flask_app.models import pet_model
from flask_app.config.mysqlconnection import connectToMySQL


class Owner:
    _db = "bonus_boops_db"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.pets = []

    @staticmethod
    def owner_form_is_valid(form_data):
        is_valid = True

        if len(form_data["first_name"].strip()) == 0:
            flash("Please enter first name.")
            is_valid = False
        elif len(form_data["first_name"].strip()) < 2:
            flash("First name must be at least two characters.")
            is_valid = False

        if len(form_data["last_name"].strip()) == 0:
            flash("Please enter last name.")
            is_valid = False
        elif len(form_data["last_name"].strip()) < 2:
            flash("Last name must be at least two characters.")
            is_valid = False

        return is_valid

    @classmethod
    def insert(cls, form_data):
        """Insert a new owner row into the database."""

        query = """
        INSERT INTO owners
        (first_name, last_name)
        VALUES
        (%(first_name)s, %(last_name)s);
        """
        owner_id = connectToMySQL(Owner._db).query_db(query, form_data)
        return owner_id

    @classmethod
    def select_all(cls):
        """Selects all of the owners in the database."""

        query = "SELECT * FROM owners;"
        list_of_dicts = connectToMySQL(Owner._db).query_db(query)
        owners = []

        for each_dict in list_of_dicts:
            owners.append(Owner(each_dict))

        return owners

    @classmethod
    def select_by_id(cls, owner_id):
        """Selects one owner by id from the database."""

        query = "SELECT * FROM owners WHERE id=%(owner_id)s;"
        data = {"owner_id": owner_id}
        list_of_dicts = connectToMySQL(Owner._db).query_db(query, data)

        owner = Owner(list_of_dicts[0])
        return owner

    @classmethod
    def select_by_id_with_pets(cls, owner_id):
        """Selects one owner by id and their pets from the database."""

        query = """
        SELECT * FROM owners
        LEFT JOIN pets
        ON owners.id = pets.owner_id
        WHERE owners.id=%(owner_id)s;
        """
        data = {"owner_id": owner_id}
        list_of_dicts = connectToMySQL(Owner._db).query_db(query, data)
        pprint(list_of_dicts)

        owner = Owner(list_of_dicts[0])
        for each_dict in list_of_dicts:
            if each_dict["pets.id"] != None:
                pet_data = {
                    "id": each_dict["pets.id"],
                    "name": each_dict["name"],
                    "type": each_dict["type"],
                    "is_derpy": each_dict["is_derpy"],
                    "created_at": each_dict["pets.created_at"],
                    "updated_at": each_dict["pets.updated_at"],
                }
                pet = pet_model.Pet(pet_data)
                owner.pets.append(pet)
        return owner

    @classmethod
    def update(cls, form_data):
        """Update an owner in the database from form data."""

        query = """
        UPDATE owners
        SET
        first_name=%(first_name)s,
        last_name=%(last_name)s
        WHERE id=%(owner_id)s;
        """
        connectToMySQL(Owner._db).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(cls, owner_id):
        """Deletes an owner by id from the database."""

        query = "DELETE FROM owners WHERE id=%(owner_id)s;"
        data = {"owner_id": owner_id}

        connectToMySQL(Owner._db).query_db(query, data)
        return
