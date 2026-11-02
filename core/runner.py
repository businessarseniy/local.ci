import uuid
import subprocess
import logging

from backend import BaseBackend
from config import BaseConfig
from .base import BaseRunner


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("local.ci/runner")


class Runner(BaseRunner):

    config: BaseConfig
    backend: BaseBackend
    identifier: str

    def __init__(self: "Runner", config: BaseConfig, backend: BaseBackend):
        self.config = config
        self.backend = backend
    
    def __enter__(self: "Runner"):
        self.bootstrap()
        self.setup()

    def __exit__(self: "Runner", exc_type, exc, tb):
        self.cleanup()

    # TODO: rewrite with error handling, instead of
    # some weird `with` block
    def run(self: "Runner"):
        with self:
            self.install()
            self.test()
            self.deploy()
            self.notify()

    def bootstrap(self: "Runner"):
        # Setup a VM or Docker image defined in config
        # NOTE: superuser
        config_view = self.config.view()
        identifier = f"ci_runner_{uuid.uuid4().hex}"
        image = config_view.image
        env = config_view.env
        args = self.backend.bootstrapArgs(image, env, identifier)
        r = subprocess.run(args)
        self.identifier = identifier
        log.debug(f"Starting docker container with {r.args} -> {r.returncode}")
    
    def setup(self: "Runner"):
        # Run setup scripts inside created instance
        # NOTE: superuser
        config_view = self.config.view()
        for step in config_view.setup:
            args = self.backend.execArgs(self.identifier, step, "root")
            r = subprocess.run(args)
            log.info(f"\"{step.name or step.run}\" -> {r.returncode}")

    def install(self: "Runner"):
        # Run project related requirements
        # NOTE: regular user
        config_view = self.config.view()
        for step in config_view.install:
            args = self.backend.execArgs(self.identifier, step, "user")
            r = subprocess.run(args)
            log.info(f"\"{step.name or step.run}\" -> {r.returncode}")

    def test(self: "Runner"):
        # Run test scriplets
        # NOTE: regular user
        config_view = self.config.view()
        for step in config_view.test:
            args = self.backend.execArgs(self.identifier, step, "user")
            r = subprocess.run(args)
            log.info(f"\"{step.name or step.run}\" -> {r.returncode}")

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
        args = self.backend.cleanupArgs(self.identifier)
        r = subprocess.run(args)
        log.debug(f"\"{r.args}\" -> {r.returncode}")
        self.identifier = None
