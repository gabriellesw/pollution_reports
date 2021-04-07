import pathlib
from yaml_pyconf import FlaskConfig


class Config(FlaskConfig):
    def __new__(
            cls,
            db_path=pathlib.Path(__file__).parent,
            *args, **kwargs
    ):
        kwargs["yaml_path"] = pathlib.Path(__file__).parent.joinpath("config.yaml")
        kwargs["dotenv_path"] = pathlib.Path(__file__).parent.joinpath(".env")
        new_config = super(Config, cls).__new__(cls, *args, **kwargs)
        if db_path is not None:
            new_config.__setattr__("SQLITE_PROJECT_DIRECTORY", db_path)
        return new_config

    @property
    def RECAPTCHA_PUBLIC_KEY(self):
        if self.FLASK_ENV == "development" or self.FLASK_ENV == "testing":
            return self.DEV_RECAPTCHA_PUBLIC_KEY
        elif self.FLASK_ENV == "deployment":
            return self.PROD_RECAPTCHA_PUBLIC_KEY
        else:
            raise NotImplementedError(
                "Environment should be one of 'development', 'testing', or 'deployment'"
            )

    @property
    def RECAPTCHA_SECRET_KEY(self):
        if self.TESTING:
            return self.DEV_RECAPTCHA_SECRET_KEY
        return self.PROD_RECAPTCHA_SECRET_KEY

    @property
    def GSHEET(self):
        if self.TESTING:
            return self.GSHEET_TEST
        return self.GSHEET_PROD
