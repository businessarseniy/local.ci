from abc import ABC, abstractmethod
from typing import Literal

from config.schema import EnvModel, StepModel
from share.types import Result


class BaseBackend(ABC):

    @abstractmethod
    def bootstrap(self: "BaseBackend", image: str, env: EnvModel) -> Result:
        """Manages creation of isolated environment for proper backend"""
        pass

    @abstractmethod
    def exec(self: "BaseBackend", step: StepModel, role: Literal["user", "root"]) -> Result:
        """Manages execution of step inside isolated environment under some user role"""
        pass

    @abstractmethod
    def cleanup(self: "BaseBackend") -> Result:
        """Manages cleanup resources of isolated environment"""
        pass
