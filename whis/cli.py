import argparse
import logging.config
from enum import Enum

from .utils import paste_to_bash, ANSIColors, colorize
from . import config
from .providers import get_provider

config.setup_logging()

logger = logging.getLogger(__name__)


class UserAction(Enum):
    EXECUTE = "_execute"
    QUIT = "_quit"
    RETRY = "_retry"
    FEEDBACK = "feedback"


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
            print(f"? {colorize(suggestion, ANSIColors.BOLD_CYAN)}")

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
            elif isinstance(action, str):  # custom feedback like "ok, but display human-readable file sizes"
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


def run_cli():
    parser = argparse.ArgumentParser(
        prog="whis",
        description="Suggest a shell command from a natural-language prompt.",
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit.")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Quick smoke test: tries connection with simple command and exits.",
    )

    args = parser.parse_args()
    if args.version:
        print(config.get_version())
        exit(0)

    if args.smoke:
        print("Checking provider and model...", end=" ")
        provider = get_provider()
        if provider.is_available():
            print(f"{provider.label} ({provider.model})")  # todo create method on provider
        print("Asking for suggestion...", end=" ")
        print(colorize("list mp3 files", ANSIColors.BOLD_ORANGE))
        sug = provider.say("list mp3 files")
        print(f"whis: {colorize(sug, ANSIColors.BOLD_CYAN)}")
        print("OK. No errors found.")
        exit(0)

    session = Session()
    session.run()


if __name__ == "__main__":
    run_cli()
