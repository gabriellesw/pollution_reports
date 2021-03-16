import pathlib
from yaml_pyconf import FlaskConfig


class Config(FlaskConfig):
    def __new__(cls, *args, **kwargs):
        kwargs["yaml_path"] = pathlib.Path(__file__).parent.joinpath("config.yaml")
        kwargs["dotenv_path"] = pathlib.Path(__file__).parent.joinpath(".env")
        return super(Config, cls).__new__(cls, *args, **kwargs)
