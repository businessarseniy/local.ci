import yaml

from .base import BaseConfig
from .schema import ConfigModel


class YamlConfig(BaseConfig):

    _config: ConfigModel = None

    @staticmethod
    def load(path: str) -> "YamlConfig":
        with open(path, "r") as fd:
            file = yaml.safe_load(fd)
        config = ConfigModel.model_validate(file)
        return YamlConfig(config)

    def __init__(self: "YamlConfig", config: ConfigModel) -> None:
        self._config = config

    def view(self: "YamlConfig") -> ConfigModel:
        return self._config
