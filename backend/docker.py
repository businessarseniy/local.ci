import os

from .base import BaseBackend


# TODO: implement docker backend
class DockerBackend(BaseBackend):
    def bootstrapArgs(self: "DockerBackend", image: str, env: dict, identifier: str) -> list[str]:
        args = []
        pwd = os.getcwd()
        args = ["docker", "run", "-dit", "-v", f"{pwd}:/workspace", "-w", "/workspace", "--name", identifier]
        for key in env:
            args.append("-e")
            args.append("{}={}".format(key, env.get(key)))
        args.append(image)
        return args

    def execArgs(self: "DockerBackend", identifier: str, cmd: list[str]) -> list[str]:
        args = ["docker", "exec", identifier]
        args.extend(cmd)
        return args

    def cleanupArgs(self: "DockerBackend", identifier: str) -> list[str]:
        return ["docker", "rm", "-f", identifier]
