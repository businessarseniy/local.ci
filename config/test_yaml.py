import os

import pytest

from config.yaml import YamlConfig


def test_yaml_config_minimal(tmp_path):
    content = """\
image: "alpine:latest"

test:
    - run: exit 0
"""
    path = os.path.join(tmp_path, "minimal.yml")
    with open(path, "w") as f: f.write(content)
    config = YamlConfig.load(path)
    assert config.is_ok()
    view = config.value.view()
    assert view.image == "alpine:latest"
    assert len(view.test) == 1
    assert view.test[0].run == "exit 0"


@pytest.mark.parametrize(
    ["content"],
    [
        [""],
        ["imeag: bleh"],
        ["eenv:"],
        ["env:\n  vlies:\n    KEY: VALUE"],
        ["env:\n  filee: .env"],
        ["sutup:"],
        ["ienstall:"],
        ["test:\n  - rin: exit 0"],
        ["test:\n  - naem: bleh"],
        ["teast:"],
        ["diepliy:"],
        ["notifyy:"],
    ]
)
def test_yaml_config_wrong(tmp_path, content):
    path = os.path.join(tmp_path, "wrong.yml")
    with open(path, "w") as f: f.write(content)
    config = YamlConfig.load(path)
    assert config.is_err()


def test_yaml_config_image(tmp_path):
    content = """\
image: "docker:dind"
test: []
"""
    path = os.path.join(tmp_path, "image.yml")
    with open(path, "w") as f: f.write(content)
    config = YamlConfig.load(path)
    assert config.is_ok()
    view = config.value.view()
    assert view.image == "docker:dind"


def test_yaml_config_env(tmp_path):
    content = """\
image: ""
env:
    file: .env
    values:
        KEY: VALUE
test: []
"""
    path = os.path.join(tmp_path, "env.yml")
    with open(path, "w") as f: f.write(content)
    config = YamlConfig.load(path)
    assert config.is_ok()
    view = config.value.view()
    assert view.env.file == ".env"
    assert "KEY" in view.env.values.keys()
    assert view.env.values.get("KEY") == "VALUE"


def test_yaml_config_steps(tmp_path):
    content = """\
image: ""
setup:
    - name: Setup
      run: exit 0
    - name: Setup 2
      run: exit 1
install:
    - name: Install
      run: exit 2
test:
    - name: Test123
      run: exit 4
    - run: exit 5
"""
    path = os.path.join(tmp_path, "steps.yml")
    with open(path, "w") as f: f.write(content)
    config = YamlConfig.load(path)
    assert config.is_ok()
    view = config.value.view()
    assert len(view.setup) == 2
    assert len(view.install) == 1
    assert len(view.test) == 2

    assert view.setup[0].name == "Setup"
    assert view.setup[0].run == "exit 0"
    assert view.setup[1].name == "Setup 2"
    assert view.setup[1].run == "exit 1"

    assert view.install[0].name == "Install"
    assert view.install[0].run == "exit 2"

    assert view.test[0].name == "Test123"
    assert view.test[0].run == "exit 4"
    assert view.test[1].name is None
    assert view.test[1].run == "exit 5"
