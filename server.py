from flask_app import app
from flask_app.controllers import controller_login, controller_manga

if __name__=="__main__":
    app.run(debug=True)