from abc import ABC, abstractmethod

from share.types import Result
from .schema import ConfigModel


class BaseConfig(ABC):

    @staticmethod
    @abstractmethod
    def load(path: str) -> Result["BaseConfig"]:
        """Handles staticmethod loading of config, returning config class instance"""
        pass

    @abstractmethod
    def view(self: "BaseConfig") -> ConfigModel:
        """Returns view on config model"""
        pass
