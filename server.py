from flask_app import app

from flask_app.controllers import owner_controller, pet_controller, boop_controller

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5150)
