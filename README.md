# Local.CI

A tool that enables CI workflows on local host system.
You just need to define ci config and run.

## Requirements

- Make
- Python 3.12 (I think?)
- Docker

## Installation

Clone the repository, then run `make && make install`.
It will install (soft link) `main.py` to `~/bin/local.ci`.

## Usage

Using this tool is simple after installing it. Make sure that `~/bin` is
in your `$PATH`. Look at [example ci config](./example.yml) for reference.
Then you can run in working directory `local.ci <config file>`
