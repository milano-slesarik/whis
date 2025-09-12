import logging.config
from enum import Enum

from prompt_toolkit import HTML, prompt
from prompt_toolkit.styles import Style

from . import config
from .providers import registry
from .utils import ANSIColors, colorize, paste_to_bash

config.setup_logging()

logger = logging.getLogger(__name__)


class UserAction(Enum):
    EXECUTE = "_execute"
    QUIT = "_quit"
    REGENERATE = "_regenerate"
    FEEDBACK = "feedback"


class Session:
    def __init__(self):
        logger.info("WHIS %s", config.get_version())

        self.provider = registry.create_by_env()
        logger.info(self.provider)

    def oneshot(self, message: str):
        return paste_to_bash(self.provider.say(message))

    def run(self):
        logger.info("run")
        print(colorize(f"Whisperer: {self.provider}", ANSIColors.DIM), end="\n")

        message = self._input("")

        while True:
            suggestion = self.provider.say(message)
            print("\nSuggestion: ")
            print(f"    {colorize(suggestion, ANSIColors.BOLD_CYAN)}", end="\n\n")

            action = self._get_user_action()

            if action == UserAction.EXECUTE:
                logger.info("Pasting to bash: %s", suggestion)
                # pyperclip.copy(suggestion)
                paste_to_bash(suggestion)
                return

            elif action == UserAction.QUIT:
                print("Cancelled.")
                return
            elif action == UserAction.REGENERATE:
                message = "Try again, user wants something different."
            elif isinstance(action, str):  # custom feedback like "ok, but display human-readable file sizes"
                message = action

    def _get_user_action(self):
        raw_input = self._input(placeholder="[Enter] Accept | Type to Refine | [Q]uit")
        logger.debug("User input: %s", raw_input)
        return self._parse_user_action(raw_input)

    def _input(self, placeholder: str = ""):
        style = Style.from_dict({"placeholder": "fg:#808080"})
        return prompt(
            ">>> ",
            placeholder=HTML(f"<placeholder>{placeholder}</placeholder>"),
            style=style,
        )

    def _parse_user_action(self, user_response):
        response_lower = user_response.lower()

        if response_lower in ("", "y", "yes", "ok"):
            _return = UserAction.EXECUTE
        elif response_lower in ("q", "quit"):
            _return = UserAction.QUIT
        elif response_lower in ("r", "regenerate"):
            _return = UserAction.REGENERATE
        else:
            _return = user_response  # custom feedback

        logger.debug("Parsed user action: %s", _return)
        return _return


def run_cli(oneshot=None):
    config.check_is_ready()
    session = Session()
    if not oneshot:
        session.run()
    else:
        session.oneshot(oneshot)
