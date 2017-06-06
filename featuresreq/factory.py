"""
Factory used to create a Flask app instance.
"""

from flask import Flask
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine, func

from featuresreq.models import session_factory, Base, Client
from featuresreq.routes import bp


def create_app(db_uri: str="sqlite://"):
    """
    Create a Flask application instance.

    Initializes the database, app routes, and extensions.

    :param db_uri: Database uri
    """
    app = Flask('featuresreq')

    # Intialize the datbase
    engine = create_engine(db_uri)
    session_factory.configure(bind=engine)
    session = flask_scoped_session(session_factory, app)
    app.session = session

    # Register blueprints
    app.register_blueprint(bp)

    # Bootstrap the database models and Clients
    @app.before_first_request
    def bootstrap_client_models():
        Base.metadata.create_all(engine)

        for c in ("a", "b", "c"):
            name = "Client {}".format(c.upper())
            client = session.query(Client).filter(func.lower(Client.name) == name.lower()).first()
            if client is None:
                client = Client(name=name)
                session.add(client)
                session.commit()

    return app
