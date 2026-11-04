from abc import ABC, abstractmethod

from share.types import Result
from .schema import ConfigModel


class BaseConfig(ABC):

    @staticmethod
    @abstractmethod
    def load(path: str) -> Result["BaseConfig"]:
        pass

    @abstractmethod
    def view(self: "BaseConfig") -> ConfigModel:
        pass
