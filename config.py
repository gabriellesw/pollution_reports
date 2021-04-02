import pathlib
from yaml_pyconf import FlaskConfig


class Config(FlaskConfig):
    def __new__(cls, *args, **kwargs):
        kwargs["yaml_path"] = pathlib.Path(__file__).parent.joinpath("config.yaml")
        kwargs["dotenv_path"] = pathlib.Path(__file__).parent.joinpath(".env")
        return super(Config, cls).__new__(cls, *args, **kwargs)

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
        if self.FLASK_ENV == "development" or self.FLASK_ENV == "testing":
            return self.DEV_RECAPTCHA_SECRET_KEY
        elif self.FLASK_ENV == "deployment":
            return self.PROD_RECAPTCHA_SECRET_KEY
        else:
            raise NotImplementedError(
                "Environment should be one of 'development', 'testing', or 'deployment'"
            )

