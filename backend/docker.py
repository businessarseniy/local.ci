import os

from .base import BaseBackend


# TODO: implement docker backend
class DockerBackend(BaseBackend):
    def bootstrapArgs(self: "DockerBackend", image: str, env: dict, identifier: str) -> list[str]:
        args = []
        pwd = os.getcwd()
        args = ["docker", "run", "-d", "-v", f"{pwd}:/workspace", "-w", "/workspace", "--name", identifier]
        for key in env:
            args.append("-e")
            args.append("{}={}".format(key, env.get(key)))
        args.extend(["--entrypoint", "tail"])
        args.append(image)
        args.extend(["-f", "/dev/null"])
        return args

    def execArgs(self: "DockerBackend", identifier: str, cmd: list[str], is_user: bool = True) -> list[str]:
        args = ["docker", "exec"]
        if (is_user):
            # Use host system uid:gid map?
            args.extend(["-u", "1000:1000", "-e", "HOME=/tmp"])
        args.append(identifier)
        args.extend(cmd)
        return args

    def cleanupArgs(self: "DockerBackend", identifier: str) -> list[str]:
        return ["docker", "rm", "-f", identifier]
