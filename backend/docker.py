import os
import subprocess
import uuid
from typing import Literal

from config.schema import EnvModel, StepModel
from share.types import Result, Ok, Err
from .base import BaseBackend


BASE_IDENTIFIER = "local-ci_"


# TODO: capture output, check, timeout
class DockerBackend(BaseBackend):

    # state: current isolated environment identifier
    identifier: str

    @staticmethod
    def generate_identifier() -> str:
        """Makes unique identifier for container to create and name"""
        return BASE_IDENTIFIER + uuid.uuid4().hex[:6]

    def bootstrap(self: "DockerBackend", image: str, env: EnvModel) -> Result:
        """Creates container, assigning it identifier, entrypoint and global env vars"""
        try:
            identifier = DockerBackend.generate_identifier()
            arguments = self.bootstrapArgs(image, env, identifier)
            r = subprocess.run(arguments)
            self.identifier = identifier
            return Ok(r)
        except Exception as e:
            return Err(e)

    def exec(self: "DockerBackend", step: StepModel, role: Literal["user", "root"]) -> Result:
        """Handles execution inside container under user roles (user for regular,
        root for privilleged). Uses step run command."""
        try:
            identifier = self.identifier
            arguments = self.execArgs(identifier, step, role)
            r = subprocess.run(arguments)
            return Ok(r)
        except Exception as e:
            return Err(e)

    def cleanup(self: "DockerBackend") -> Result:
        """Clears identified container"""
        try:
            identifier = self.identifier
            arguments = self.cleanupArgs(identifier)
            r = subprocess.run(arguments)
            return Ok(r)
        except Exception as e:
            return Err(e)
        finally:
            self.identifier = None

    def bootstrapArgs(self: "DockerBackend", image: str, env: EnvModel, identifier: str) -> list[str]:
        """Builds list of arguments to start container"""
        args = []
        pwd = os.getcwd()
        args = ["docker", "run", "-d", "-v", f"{pwd}:/workspace", "-w", "/workspace", "--name", identifier]
        if (env and env.view()):
            for key, val in env.view().items():
                args.append("-e")
                args.append("{}={}".format(key, val))
        args.extend(["--entrypoint", "tail"])
        args.append(image)
        args.extend(["-f", "/dev/null"])
        return args

    def execArgs(self: "DockerBackend", identifier: str, step: StepModel, role: Literal["user", "root"] = "user") -> list[str]:
        """Builds arguments to execute step inside identified container"""
        args = ["docker", "exec"]
        if (role == "user"):
            args.extend(["-u", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp"])
        args.append(identifier)
        args.extend(step.view())
        return args

    def cleanupArgs(self: "DockerBackend", identifier: str) -> list[str]:
        """Builds arguments for clearing and removing identified container"""
        return ["docker", "rm", "-f", identifier]
