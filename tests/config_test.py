import pytest
from whis import config


@pytest.mark.parametrize(
    "env_val,file_val,default,expected",
    [
        ("from_env", "from_config", None, "from_env"),  # config wins
        ("from_env", None, None, "from_env"),  # fallback to env
        (None, None, "def", "def"),  # fallback to default
    ],
)
def test_get_cfg_var(monkeypatch, env_val, file_val, default, expected):
    key = "foo"

    if env_val is None:
        monkeypatch.delenv("WHIS_FOO", raising=False)
    else:
        monkeypatch.setenv("WHIS_FOO", env_val)

    if file_val is None:
        monkeypatch.setattr(config, "config_toml", {}, raising=False)
    else:
        monkeypatch.setattr(config, "config_toml", {key: file_val}, raising=False)

    assert config.get_cfg_var(key, default=default) == expected
