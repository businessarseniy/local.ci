import yaml
from pydantic import ValidationError

from share.types import Result, Ok, Err
from .base import BaseConfig
from .schema import ConfigModel


class YamlConfig(BaseConfig):

    _config: ConfigModel = None

    @staticmethod
    def load(path: str) -> Result["YamlConfig"]:
        try:
            with open(path, "r") as fd:
                file = yaml.safe_load(fd)
            config = ConfigModel.model_validate(file)
            return Ok(YamlConfig(config))
        except ValidationError as e:
            return Err(e)

    def __init__(self: "YamlConfig", config: ConfigModel) -> None:
        self._config = config

    def view(self: "YamlConfig") -> ConfigModel:
        return self._config
