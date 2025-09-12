import importlib


def test_quit_flow(monkeypatch, capsys):
    monkeypatch.setenv("WHIS_LLM_PROVIDER", "dummy")
    monkeypatch.setenv("WHIS_LLM_MODEL", "dummy")

    import whis.cli as cli

    importlib.reload(cli)

    inputs = iter(["list mp3", "q"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))

    session = cli.Session()
    session.run()

    out = capsys.readouterr().out
    assert "Whisperer:" in out
    assert "Cancelled." in out


def test_parse_user_action_basic(monkeypatch):
    monkeypatch.setenv("WHIS_LLM_PROVIDER", "dummy")
    monkeypatch.setenv("WHIS_LLM_MODEL", "dummy")

    import whis.cli as cli

    importlib.reload(cli)

    s = cli.Session()
    assert s._parse_user_action("") == cli.UserAction.EXECUTE
    assert s._parse_user_action("r") == cli.UserAction.REGENERATE
    assert s._parse_user_action("q") == cli.UserAction.QUIT
    assert s._parse_user_action("quit") == cli.UserAction.QUIT  # todo remove "quit", "q" is more than enough
    assert s._parse_user_action("human-readable sizes") == "human-readable sizes"
