from flask_app.config.mysqlconnection import connectToMySQL


class Boop:
    _db = "bonus_boops_db"

    @classmethod
    def insert(cls, form_data):
        """Creates a boop in the database."""

        query = """
        INSERT INTO boops
        (owner_id, pet_id)
        VALUES
        (%(owner_id)s, %(pet_id)s);
        """
        boop_id = connectToMySQL(Boop._db).query_db(query, form_data)
        return boop_id
