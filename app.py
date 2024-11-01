from flask import Flask
from application.config import LocalDevelopmentConfig
from application.models import db, User, Role
from application.resources import api
from flask_security import Security, SQLAlchemyUserDatastore, auth_required

def createApp():
    app = Flask(__name__)

    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    api.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    app.security = Security(app, datastore=datastore, register_blueprint=False)
    app.app_context().push()

    return app

app = createApp()

import application.initial_data

import application.controllers


        
if (__name__ == '__main__'):
    app.run(debug=True)