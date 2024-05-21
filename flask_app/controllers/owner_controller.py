from flask_app import app
from flask_app.models.owner_model import Owner
from flask import redirect, render_template, request


@app.get("/")
def index():
    """Displays the home page."""
    return render_template("index.html")


@app.get("/owners/new")
def new_owner():
    """Displays a form to create an owner."""

    return render_template("new_owner.html")


@app.post("/owners/create")
def create_owner():
    """Processes the new owner form."""

    if not Owner.owner_form_is_valid(request.form):
        return redirect("/owners/new")

    Owner.insert(request.form)
    return redirect("/owners/all")


@app.get("/owners/all")
def all_owners():
    """Displays all the owners."""

    owners = Owner.select_all()

    return render_template("all_owners.html", owners=owners)


@app.get("/owners/<int:owner_id>")
def one_owner(owner_id):
    """Displays the details of one owner."""

    owner = Owner.select_by_id_with_pets(owner_id)
    return render_template("one_owner.html", owner=owner)


@app.get("/owners/<int:owner_id>/edit")
def edit_owner(owner_id):
    """Displays the edit form for an owner."""

    owner = Owner.select_by_id(owner_id)

    return render_template("edit_owner.html", owner=owner)


@app.post("/owners/update")
def update_owner():
    """Updates an owner."""

    Owner.update(request.form)
    return redirect(f"/owners/{request.form['owner_id']}")


@app.get("/owners/<int:owner_id>/delete")
def delete_owner(owner_id):
    """Deletes an owner from the database."""

    Owner.delete_by_id(owner_id)
    return redirect("/owners/all")
