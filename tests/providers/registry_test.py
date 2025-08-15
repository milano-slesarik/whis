import pytest

from whis.providers import ProviderRegistry


class DummyProviderA:
    name = "dummy_a"
    label = "Dummy A"

    def __init__(self, model):
        self.model = model


class DummyProviderB:
    name = "dummy_b"
    label = "Dummy B"

    def __init__(self, model):
        self.model = model


def test_register_and_list_sorted():
    reg = ProviderRegistry()
    reg.register(DummyProviderB)
    reg.register(DummyProviderA)
    assert reg.list() == ["dummy_a", "dummy_b"]


def test_create_returns_instance_with_model():
    reg = ProviderRegistry()
    reg.register(DummyProviderA)

    inst = reg.create("dummy_a", model="supermodel")
    assert isinstance(inst, DummyProviderA)
    assert inst.model == "supermodel"


def test_create_unknown_provider_raises_unavailable_provider_error():
    reg = ProviderRegistry()
    with pytest.raises(ProviderRegistry.UnavailableProviderError):
        reg.create("unknown", model="doesntmatter")
