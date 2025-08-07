import logging.config
from enum import Enum

from .utils import paste_to_bash
from . import config
from .providers import get_provider

config.setup_logging()

logger = logging.getLogger(__name__)


class UserAction(Enum):
    EXECUTE = "_execute"
    QUIT = "_quit"
    RETRY = "_retry"
    FEEDBACK = "feedback"


class ANSIColors:
    BOLD_CYAN = "\033[1;36m"
    RESET = "\033[0m"


class Session:
    def __init__(self):
        logger.info("WHIS %s", config.get_version())


        self.provider = get_provider()
        logger.info(self.provider)

    def robot_label(self):
        return f"{self.provider.label} ({self.provider.model})"

    def run(self):
        logger.info("run")
        print(f"WHIS: {self.robot_label()}")

        message = input("> ")

        while True:
            # try/except with repeat?
            suggestion = self.provider.say(message)
            print(f"? {self._colorize(suggestion, ANSIColors.BOLD_CYAN)}")

            action = self._get_user_action()

            if action == UserAction.EXECUTE:
                print(suggestion)
                logger.info("Pasting to bash: %s", suggestion)
                # pyperclip.copy(suggestion)
                paste_to_bash(suggestion)
                exit(0)

            elif action == UserAction.QUIT:
                print("Cancelled.")
                exit(0)
            elif action == UserAction.RETRY:
                message = "Try again, user wants something different."
            elif isinstance(
                action, str
            ):  # custom feedback like "ok, but display human-readable file sizes"
                message = action

    def _get_user_action(self):
        print("[enter] use, [r]etry, [q]uit, or refine:")
        raw_input = input("> ").strip()
        logger.debug("User input: %s", raw_input)
        return self._parse_user_action(raw_input)

    def _parse_user_action(self, user_response):
        response_lower = user_response.lower()

        if response_lower in ("", "y", "yes", "ok"):
            _return = UserAction.EXECUTE
        elif response_lower in ("q", "quit"):
            _return = UserAction.QUIT
        elif response_lower in ("r", "retry"):
            _return = UserAction.RETRY
        else:
            _return = user_response  # custom feedback

        logger.debug("Parsed user action: %s", _return)
        return _return

    def _colorize(self, text, color):
        return f"{color}{text}{ANSIColors.RESET}"


def run_cli():
    session = Session()
    session.run()


if __name__ == "__main__":
    run_cli()
