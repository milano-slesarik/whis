import logging
from abc import ABC, abstractmethod
from enum import Enum

from . import config

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import ollama

    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

logger = logging.getLogger(__name__)


class ProviderType(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    # ANTHROPIC = "anthropic"  # todo
    # GEMINI = "gemini"  # todo


class ProviderRegistry:
    def __init__(self):
        self._providers = {}

    class UnavailableProviderError(Exception):
        pass

    def register(self, cls):
        logger.debug("Registering provider: %s", cls)
        self._providers[cls.name] = cls
        return cls

    def _get_provider_class(self, provider_name):
        try:
            return self._providers[provider_name]
        except KeyError:
            raise self.UnavailableProviderError(f"Provider {provider_name} is not available.")

    def create(self, provider_name, model):
        # todo manage errors
        return self._get_provider_class(provider_name)(model)

    def create_by_env(self):
        return self.create(config.llm_provider, config.llm_model)

    def list(self) -> list[str]:
        return sorted(self._providers.keys())


registry = ProviderRegistry()


class LLMProvider(ABC):
    name = None
    label = None
    temp = None

    def __init__(self, model):
        self.history = []
        self.model = model
        self._set_system_prompt()

    def _set_system_prompt(self) -> None:
        self._add_message("system", config.SYSTEM_PROMPT)

    def _add_message(self, role: str, content: str):
        logger.debug("Adding message to history: role=%s, content=%s", role, content)
        self.history.append({"role": role, "content": content})

    def _log_recent_history(self, max_messages: int = 5) -> None:
        if len(self.history) <= 1:
            return

        user_messages = self.history[1:]  # skip system prompt
        recent = user_messages[-max_messages:] if len(user_messages) >= max_messages else user_messages

        logger.debug("Last messages in history:")
        for msg in recent:
            logger.debug("  Role=%s, Content=%s", msg["role"], msg["content"])

    def submit(self) -> str:
        logger.debug("Submitting request to LLM")
        self._log_recent_history()
        response = self._submit()
        self._add_message("assistant", response)
        logger.debug("Response: %s", response)
        return response

    @abstractmethod
    def _submit(self):
        pass

    def say(self, message) -> str:
        self._add_message("user", message)
        response = self.submit()
        command = self.parse_command(response)
        return command

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @staticmethod
    def parse_command(command: str) -> str:
        if command.startswith("```") and command.endswith("```"):
            lines = command.splitlines()
            command_lines = lines[1:-1]
            command = "\n".join(command_lines)
        else:
            command = command.strip("`")
        return command.strip()

    def __str__(self):
        return f"{self.label} ({self.model})"


@registry.register
class OpenAIProvider(LLMProvider):
    name = "openai"
    label = "OpenAI"
    temp = 0.2

    def __init__(self, model: str):
        if not OPENAI_AVAILABLE:
            raise ImportError("Missing package `openai`.")

        super().__init__(model)

        self.model = model
        self.provider = OpenAI()

    def is_available(self) -> bool:
        return OPENAI_AVAILABLE

    def _submit(self) -> str:
        response = self.provider.chat.completions.create(
            model=self.model,
            messages=self.history,
            temperature=self.temp,
        )
        return response.choices[0].message.content.strip()


@registry.register
class OllamaProvider(LLMProvider):
    name = "ollama"
    label = "Ollama"
    temp = 0.2

    def __init__(self, model: str):
        if not OLLAMA_AVAILABLE:
            raise ImportError("Missing package `ollama`.")
        super().__init__(model)

        self.model = model
        self.provider = ollama.Client()

    def is_available(self) -> bool:
        return OLLAMA_AVAILABLE

    def _submit(self) -> str:
        response = self.provider.chat(
            model=self.model,
            messages=self.history,
            options={"temperature": self.temp},
        )
        return response.message.content.strip()


class DummyProvider(LLMProvider):
    """Dummy provider for testing etc..."""

    name = "dummy"
    label = "Dummy"
    temp = 0.0

    def __init__(self, model: str = "dummy"):
        super().__init__(model)

    def is_available(self) -> bool:
        return True

    def _submit(self) -> str:
        return "a dummy response"


if config.is_dev or config.is_test or config.llm_provider == "dummy":
    registry.register(DummyProvider)
