#!/usr/bin/env python3
# *-* encoding: UTF-8 *-*

# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 @businessarseniy


import logging
import sys

from backend import BaseBackend, DockerBackend
from config import BaseConfig, YamlConfig
from core import BaseRunner, Runner


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("local.ci")


def main():
    # TODO: check for only yaml file
    # TODO: error handling
    # TODO: execution steps termination
    if (len(sys.argv) != 2):
        log.error("Wrong tool usage! Exiting...")
        sys.exit(1)
    if (sys.argv[-1] == "--version"):
        log.info("0.0.0-alpha")
        sys.exit(0)
    c = YamlConfig.load(path=sys.argv[-1])
    b = DockerBackend()
    r = Runner(c, b)
    r.run()


if __name__ == "__main__":
    main()
