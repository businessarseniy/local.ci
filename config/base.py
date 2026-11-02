from abc import ABC, abstractmethod

from .schema import ConfigModel


class BaseConfig(ABC):

    @staticmethod
    @abstractmethod
    def load(path: str) -> "BaseConfig":
        pass

    @abstractmethod
    def view(self: "BaseConfig") -> ConfigModel:
        pass
