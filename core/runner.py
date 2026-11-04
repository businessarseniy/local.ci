import logging
from abc import ABC, abstractmethod

from backend import BaseBackend
from config import BaseConfig
from share.types import Result, Ok, Err


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("local.ci/runner")


class BaseRunner(ABC):
    pass


class Runner(BaseRunner):

    config: BaseConfig
    backend: BaseBackend

    def __init__(self: "Runner", config: BaseConfig, backend: BaseBackend):
        self.config = config
        self.backend = backend

    # TODO: rewrite with error handling, instead of
    # some weird `with` block
    def run(self: "Runner"):
        try:
            match self.bootstrap():
                case Err(e): raise e
            match self.setup():
                case Err(e): raise e
            match self.install():
                case Err(e): raise e
            match self.test():
                case Err(e): raise e
            match self.deploy():
                case Err(e): raise e
            match self.notify():
                case Err(e): raise e
        except Exception as e:
            log.error("Error during runner execution: %s", e)
        finally:
            _ = self.cleanup()


    def bootstrap(self: "Runner") -> Result:
        # Setup a VM or Docker image defined in config
        # NOTE: superuser
        config_view = self.config.view()
        image = config_view.image
        env = config_view.env
        result = self.backend.bootstrap(image, env)
        match result:
            case Ok(r): log.debug(f"Starting docker container with {r.args} -> {r.returncode}")
            case Err(e):
                log.error("Error during bootstrap: %s", e)
                return result
        return Ok(())
    
    def setup(self: "Runner") -> Result:
        # Run setup scripts inside created instance
        # NOTE: superuser
        config_view = self.config.view()
        if config_view.setup is None:
            log.info("Nothing to do for setup")
            return Ok(())
        for step in config_view.setup:
            result = self.backend.exec(step, "root")
            match result:
                case Ok(r): log.info(f"\"{step.name or step.run}\" -> {r.returncode}")
                case Err(e):
                    log.error("Error during setup: %s", e)
                    return result
        return Ok(())

    def install(self: "Runner") -> Result:
        # Run project related requirements
        # NOTE: regular user
        config_view = self.config.view()
        if config_view.install is None:
            log.info("Nothing to do for install")
            return Ok(())
        for step in config_view.install:
            result = self.backend.exec(step, "user")
            match result:
                case Ok(r): log.info(f"\"{step.name or step.run}\" -> {r.returncode}")
                case Err(e):
                    log.error("Error during setup: %s", e)
                    return result
        return Ok(())

    def test(self: "Runner") -> Result:
        # Run test scriplets
        # NOTE: regular user
        config_view = self.config.view()
        if config_view.test is None:
            log.error("Error during test: no tests!")
            return Err("No tests")
        for step in config_view.test:
            result = self.backend.exec(step, "user")
            match result:
                case Ok(r): log.info(f"\"{step.name or step.run}\" -> {r.returncode}")
                case Err(e):
                    log.error("Error during test: %s", e)
                    return result
        return Ok(())

    def deploy(self: "Runner") -> Result:
        # TODO
        # Run deploy scripts
        # NOTE: regular user
        return Ok(())

    def notify(self: "Runner") -> Result:
        # TODO
        # Run notifications
        # NOTE: regular user
        return Ok(())

    def cleanup(self: "Runner") -> Result:
        # Clean resources allocated to runner
        result = self.backend.cleanup()
        match result:
            case Ok(r): log.debug(f"\"{r.args}\" -> {r.returncode}")
            case Err(e):
                log.error("Error during cleanup: %s", e)
                return result
        return Ok(())
