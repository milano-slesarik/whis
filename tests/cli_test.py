import importlib

import whis.cli as cli


def test_parse_user_action_basic(monkeypatch):
    monkeypatch.setenv("WHIS_LLM_PROVIDER", "dummy")
    monkeypatch.setenv("WHIS_LLM_MODEL", "dummy")

    importlib.reload(cli)

    s = cli.Session()
    assert s._parse_user_action("") == cli.UserAction.EXECUTE
    assert s._parse_user_action("r") == cli.UserAction.REGENERATE
    assert s._parse_user_action("q") == cli.UserAction.QUIT
    assert s._parse_user_action("quit") == cli.UserAction.QUIT  # todo remove "quit", "q" is more than enough
    assert s._parse_user_action("human-readable sizes") == "human-readable sizes"
