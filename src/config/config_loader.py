import yaml

from environment import Environment

from .config import Config


class ConfigLoader:
    config: Config | None = None

    @classmethod
    def get_config(cls) -> Config:
        if cls.config is not None:
            return cls.config

        config_path = Environment.get_variable("CONFIG_PATH")
        with open(config_path, "r") as f:
            cls.config = Config.model_validate(yaml.safe_load(f))
            return cls.config
