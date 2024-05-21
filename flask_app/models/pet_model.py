from flask import flash
from pprint import pprint
from flask_app.models import owner_model
from flask_app.config.mysqlconnection import connectToMySQL


class Pet:
    _db = "bonus_boops_db"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.type = data["type"]
        self.is_derpy = data["is_derpy"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.owner = None
        self.boops = []

    @staticmethod
    def pet_form_is_valid(form_data):
        is_valid = True

        if len(form_data["name"].strip()) == 0:
            flash("Please enter pet name.")
            is_valid = False
        elif len(form_data["name"].strip()) < 2:
            flash("Pet name must be at least two characters.")
            is_valid = False

        if len(form_data["type"].strip()) == 0:
            flash("Please enter pet type.")
            is_valid = False
        elif len(form_data["type"].strip()) < 2:
            flash("Pet type must be at least two characters.")
            is_valid = False

        if "is_derpy" not in form_data:
            flash("Please choose pet derpiness.")
            is_valid = False
        elif form_data["is_derpy"] not in ["0", "1"]:
            flash("Invalid derpiness data.")
            is_valid = False

        return is_valid

    @classmethod
    def insert(cls, form_data):
        """Insert a new pet row into the database."""

        query = """
        INSERT INTO pets
        (name, type, is_derpy, owner_id)
        VALUES
        (%(name)s, %(type)s, %(is_derpy)s, %(owner_id)s);
        """
        pet_id = connectToMySQL(Pet._db).query_db(query, form_data)
        return pet_id

    @classmethod
    def select_all(cls):
        """Selects all of the pets in the database."""

        query = "SELECT * FROM pets;"
        list_of_dicts = connectToMySQL(Pet._db).query_db(query)
        pets = []

        for each_dict in list_of_dicts:
            pets.append(Pet(each_dict))

        return pets

    @classmethod
    def select_by_id(cls, pet_id):
        """Selects a pet in the database by its id."""

        query = "SELECT * FROM pets WHERE id = %(pet_id)s;"
        data = {"pet_id": pet_id}
        list_of_dicts = connectToMySQL(Pet._db).query_db(query, data)

        return Pet(list_of_dicts[0])

    @classmethod
    def select_by_id_with_owner(cls, pet_id):
        """Selects a pet and its owner in the database by the pet id."""

        query = """
        SELECT * FROM pets
        JOIN owners
        ON owners.id = pets.owner_id
        WHERE pets.id = %(pet_id)s;
        """
        data = {"pet_id": pet_id}
        list_of_dicts = connectToMySQL(Pet._db).query_db(query, data)
        one_dict = list_of_dicts[0]
        pprint(list_of_dicts)

        pet = Pet(one_dict)
        owner_data = {
            "id": one_dict["owners.id"],
            "first_name": one_dict["first_name"],
            "last_name": one_dict["last_name"],
            "created_at": one_dict["owners.created_at"],
            "updated_at": one_dict["owners.updated_at"],
        }
        owner = owner_model.Owner(owner_data)
        pet.owner = owner

        return pet

    @classmethod
    def select_by_id_with_owner_and_boops(cls, pet_id):
        """Selects a pet and its owner and all pet's boops in the database by the pet id."""

        query = """
        SELECT * FROM pets
        JOIN owners
        ON owners.id = pets.owner_id
        LEFT JOIN boops
        ON boops.pet_id = pets.id
        WHERE pets.id = %(pet_id)s;
        """
        data = {"pet_id": pet_id}
        list_of_dicts = connectToMySQL(Pet._db).query_db(query, data)
        one_dict = list_of_dicts[0]
        pprint(list_of_dicts)

        pet = Pet(one_dict)
        owner_data = {
            "id": one_dict["owners.id"],
            "first_name": one_dict["first_name"],
            "last_name": one_dict["last_name"],
            "created_at": one_dict["owners.created_at"],
            "updated_at": one_dict["owners.updated_at"],
        }
        owner = owner_model.Owner(owner_data)
        pet.owner = owner

        for each_dict in list_of_dicts:
            if each_dict["boops.id"] != None:
                pet.boops.append(each_dict["boops.owner_id"])

        return pet

    @classmethod
    def update(cls, form_data):
        """Updates a pet by id in the database."""

        query = """
        UPDATE pets
        SET
        name=%(name)s,
        type=%(type)s,
        is_derpy=%(is_derpy)s
        WHERE id=%(pet_id)s;
        """
        connectToMySQL(Pet._db).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(cls, pet_id):
        """Deletes a pet from the database by id."""

        query = "DELETE FROM pets WHERE id=%(pet_id)s;"
        data = {"pet_id": pet_id}

        connectToMySQL(Pet._db).query_db(query, data)
        return
