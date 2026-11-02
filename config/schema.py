import shlex

from pydantic import BaseModel, Field


class EnvModel(BaseModel):
    file:       str | None              = None          # Path to env file (e.g. `.env`)
    values:     dict[str, str] | None   = None          # Key-value pairs of variables

    # TODO: resolve env file with values into single view
    def view(self: "EnvModel") -> dict[str, str]:
        return self.values


class StepModel(BaseModel):
    name:       str                     = None          # Name of step for UX
    run:        str                     = Field(...)    # Required shell command for step

    def view(self: "StepModel") -> list[str]:
        return shlex.split(self.run) # preserve quoted


class DeployModel(BaseModel):
    pass


class NotifyModel(BaseModel):
    pass


class ConfigModel(BaseModel):
    image:      str                     = Field(...)    # Image identifier (e.g. `alpine:latest`)
    env:        EnvModel | None         = None          # EnvModel
    setup:      list[StepModel] | None  = None          # Ran after container creation
    install:    list[StepModel] | None  = None          # After setup, under regular user
    test:       list[StepModel]         = Field(...)    # Actual required test steps
    deploy:     DeployModel | None      = None          # Deploy
    notify:     NotifyModel | None      = None          # Notify
