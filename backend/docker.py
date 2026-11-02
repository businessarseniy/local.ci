import os
from typing import Literal

from config.schema import EnvModel, StepModel
from .base import BaseBackend


# TODO: implement docker backend
class DockerBackend(BaseBackend):
    def bootstrapArgs(self: "DockerBackend", image: str, env: EnvModel, identifier: str) -> list[str]:
        args = []
        pwd = os.getcwd()
        args = ["docker", "run", "-d", "-v", f"{pwd}:/workspace", "-w", "/workspace", "--name", identifier]
        for key, val in env.view().items():
            args.append("-e")
            args.append("{}={}".format(key, val))
        args.extend(["--entrypoint", "tail"])
        args.append(image)
        args.extend(["-f", "/dev/null"])
        return args

    def execArgs(self: "DockerBackend", identifier: str, step: StepModel, role: Literal["user", "root"] = "user") -> list[str]:
        args = ["docker", "exec"]
        if (role == "user"):
            args.extend(["-u", f"{os.getuid()}:{os.getgid()}", "-e", "HOME=/tmp"])
        args.append(identifier)
        args.extend(step.view())
        return args

    def cleanupArgs(self: "DockerBackend", identifier: str) -> list[str]:
        return ["docker", "rm", "-f", identifier]
