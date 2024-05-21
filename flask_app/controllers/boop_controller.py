from flask_app import app
from flask import redirect, request
from flask_app.models.boop_model import Boop


@app.post("/boops/create")
def create_boop():
    """Creates a new boop."""

    Boop.insert(request.form)
    pet_id = request.form["pet_id"]
    return redirect(f"/pets/{pet_id}")
