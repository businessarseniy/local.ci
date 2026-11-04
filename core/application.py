import os
import sys
import logging
from argparse import ArgumentParser
from importlib.metadata import version

from backend import BaseBackend, DockerBackend
from config import BaseConfig, YamlConfig
from share.types import Result, Ok, Err
from .runner import Runner


APP_NAME = "local-ci"


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(APP_NAME)


class Application:
    argument_parser: ArgumentParser

    def __init__(self: "Application") -> None:
        # Argument parser for proper usage by users
        ap = ArgumentParser(APP_NAME)
        # Version flag
        ap.add_argument("--version", action="version", version=version(APP_NAME))
        # Verbose flag
        ap.add_argument("-v", "--verbose", action="store_true")
        # Configuration file type (only YAML for now, JSON TODO)
        ap.add_argument("--type", default="yaml", choices=["yaml", "json"])
        # Backend providers (only docker for now, podman TODO)
        ap.add_argument("--backend", default="docker", choices=["docker", "podman"])

        # CI configuration file
        ap.add_argument("FILE", type=str, default=None, help="CI configuration file path")
        # Apply parsed arguments
        args = ap.parse_args()

        self.is_verbose = args.verbose
        self.config_type = args.type
        self.backend_type = args.backend
        self.config_path = args.FILE

    def validate(self: "Application") -> Result:
        # No file provided
        if self.config_path is None:
            return Err("Wrong tool usage")
        # File not exists
        if not os.path.exists(self.config_path):
            return Err("File not exists")
        return Ok(())

    def run(self: "Application") -> Result:
        # Validate application usage
        validation = self.validate()
        if validation.is_err():
            log.error(validation.error)
            sys.exit(1)

        # Create types of usage
        configT: type[BaseConfig] = None
        backendT: type[BaseBackend] = None
        runnerT = Runner

        match self.config_type:
            case "yaml": configT = YamlConfig

        match self.backend_type:
            case "docker": backendT = DockerBackend
        
        config: BaseConfig = None
        backend: BaseBackend = None

        match configT.load(self.config_path):
            case Err(e):
                log.error(e)
                sys.exit(1)
            case Ok(val):
                config = val

        backend = backendT()
        runner = runnerT(config, backend)
        runner.run()
