from flask_app import app
from flask_app.models.pet_model import Pet
from flask_app.models.owner_model import Owner
from flask import redirect, render_template, request


@app.get("/pets/new")
def new_pet():
    """Displays a form to create an pet."""

    owners = Owner.select_all()

    return render_template("new_pet.html", owners=owners)


@app.post("/pets/create")
def create_pet():
    """Processes the new pet form."""

    if not Pet.pet_form_is_valid(request.form):
        return redirect("/pets/new")

    Pet.insert(request.form)
    return redirect("/pets/all")


@app.get("/pets/all")
def all_pets():
    """Displays all the pets."""

    pets = Pet.select_all()

    return render_template("all_pets.html", pets=pets)


@app.get("/pets/<int:pet_id>")
def one_pet(pet_id):
    """Displays one pet's details."""

    pet = Pet.select_by_id_with_owner_and_boops(pet_id)
    owners = Owner.select_all()
    return render_template("one_pet.html", pet=pet, owners=owners)


@app.get("/pets/<int:pet_id>/edit")
def edit_pet(pet_id):
    """Displays the edit pet form."""

    pet = Pet.select_by_id(pet_id)
    return render_template("edit_pet.html", pet=pet)


@app.post("/pets/update")
def update_pet():
    """Processes the edit pet form."""

    pet_id = request.form["pet_id"]
    if not Pet.pet_form_is_valid(request.form):
        return redirect(f"/pets/{pet_id}/edit")

    Pet.update(request.form)
    return redirect(f"/pets/{pet_id}")


@app.get("/pets/<int:pet_id>/delete")
def delete_pet(pet_id):
    """Deletes a pet."""

    Pet.delete_by_id(pet_id)
    return redirect("/pets/all")
