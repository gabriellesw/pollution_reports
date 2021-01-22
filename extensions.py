from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore


class PortableSQLAlchemyUserDataStore(SQLAlchemyUserDatastore):
    """
    Allow datastore to be created here w/o args and finalized in create_app, so we don't
    have to import any of our model here and risk circular imports, but also can use
    this wherever we need to outside of create_app. Kinda like "init_app" pattern except
    all that's needed is to set attributes
    """
    def __init__(self, db=None, user_model=None, role_model=None):
        super(PortableSQLAlchemyUserDataStore, self).__init__(db, user_model, role_model)

    def init_models(self, db=None, user_model=None, role_model=None):
        if db is not None:
            self.db = db
        if user_model is not None:
            self.user_model = user_model
        if role_model is not None:
            self.role_model = role_model

        # Assume superclass has a good reason for requiring all attributes for __init__
        errors = []
        print(self.role_model)
        for name, value in {
            "db": self.db,
            "user_model": self.user_model,
            "role_model": self.role_model,
        }.items():
            if value is None:
                errors.append(name)
        if errors:
            errors = "', '".join(errors)
            msg = f"The following required arguments are missing: '{errors}'"
            raise NotImplementedError(msg)


db = SQLAlchemy()
migrate = Migrate()
datastore = PortableSQLAlchemyUserDataStore()
security = Security()
