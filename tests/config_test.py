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


def test_check_is_ready(monkeypatch):
    monkeypatch.delenv("WHIS_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("WHIS_LLM_MODEL", raising=False)
    monkeypatch.setattr(config, "config_toml", {}, raising=False)

    with pytest.raises(config.NotReadyError) as e:
        config.check_is_ready()
    assert e.value.missing_vars == ["llm_provider", "llm_model"]

    monkeypatch.setenv("WHIS_LLM_PROVIDER", "dummy")
    monkeypatch.setenv("WHIS_LLM_MODEL", "dummy")

    config.check_is_ready()

    monkeypatch.delenv("WHIS_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("WHIS_LLM_MODEL", raising=False)
    monkeypatch.setattr(config, "config_toml", {"llm_provider": "dummy", "llm_model": "dummy"}, raising=False)

    config.check_is_ready()
