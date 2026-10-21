#!/usr/bin/env python3
# *-* encoding: UTF-8 *-*


import yaml
import subprocess
import uuid
import os
import logging
import sys


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("local.ci")


class Config:

    class _Deploy:
        provider: str
        secret: dict[str, str]
        branch: str

    class _Image(str):...
    class _Env(dict[str, str]):...
    class _Script(str):...
    class _Stage(list[_Script]):...
    class _Notify(dict):...

    image: _Image
    env: _Env
    setup: _Stage
    install: _Stage
    test: _Stage
    deploy: _Deploy
    notify: _Notify

    def load(path: str) -> "Config":
        with open(path, "r") as file:
            data: dict = yaml.load(file, Loader=yaml.CLoader)
        result = Config()
        result.image = data.get("image")
        result.env = data.get("env")
        result.setup = data.get("setup")
        result.install = data.get("install")
        result.test = data.get("test")
        result.deploy = data.get("deploy")
        result.notify = data.get("notify")
        return result

    def __repr__(self: "Config"):
        return "<CI Config>: {}".format(str(self.__dict__))


class Runner:

    class _Result():...
    class _Id(str):...

    config: Config
    identifier: _Id

    def __init__(self: "Runner", config: Config):
        self.config = config
    
    def __enter__(self: "Runner"):
        self.bootstrap()
        self.setup()

    def __exit__(self: "Runner", exc_type, exc, tb):
        self.cleanup()

    def run(self: "Runner"):
        with self:
            self.install()
            self.test()
            self.deploy()
            self.notify()

    def bootstrap(self: "Runner"):
        # Setup a VM or Docker image defined in config
        # NOTE: superuser
        self.identifier = f"ci_runner_{uuid.uuid4().hex}"
        image = self.config.image
        pwd = os.getcwd()
        args = ["docker", "run", "-dit", "-v", f"{pwd}:/workspace", "-w", "/workspace", "--name", self.identifier]
        for key in self.config.env:
            args.append("-e")
            args.append("{}={}".format(key, self.config.env.get(key)))
        args.append(image)
        r = subprocess.run(args)
        log.debug(f"Starting docker container with {r.args} -> {r.returncode}")
    
    def setup(self: "Runner"):
        # Run setup scripts inside created instance
        # NOTE: superuser
        for cmd in self.config.setup:
            r = subprocess.run(["docker", "exec", self.identifier, *cmd.split(" ")])
            log.info(f"\"{cmd}\" -> {r.returncode}")

    def install(self: "Runner"):
        # Run project related requirements
        # NOTE: regular user
        for cmd in self.config.install:
            r = subprocess.run(["docker", "exec", self.identifier, *cmd.split(" ")])
            log.info(f"\"{cmd}\" -> {r.returncode}")

    def test(self: "Runner"):
        # Run test scriplets
        # NOTE: regular user
        for cmd in self.config.test:
            r = subprocess.run(["docker", "exec", self.identifier, *cmd.split(" ")])
            log.info(f"\"{cmd}\" -> {r.returncode}")

    def deploy(self: "Runner"):
        # TODO
        # Run deploy scripts
        # NOTE: regular user
        pass

    def notify(self: "Runner"):
        # TODO
        # Run notifications
        # NOTE: regular user
        pass

    def cleanup(self: "Runner"):
        # Clean resources allocated to runner
        r = subprocess.run(["docker", "rm", "-f", self.identifier])
        log.debug(f"\"{r.args}\" -> {r.returncode}")
        self.identifier = None


def main():
    # TODO: check for only yaml file
    # TODO: error handling
    # TODO: execution steps termination
    if (len(sys.argv) != 2):
        log.error("Wrong tool usage! Exiting...")
        sys.exit(-1)
    c = Config.load(path=sys.argv[-1])
    r = Runner(c)
    r.run()


if __name__ == "__main__":
    main()
