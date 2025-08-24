import logging.config
from enum import Enum

from . import config
from .providers import registry
from .utils import paste_to_bash, ANSIColors, colorize

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

        self.provider = registry.create_by_env()
        logger.info(self.provider)

    def oneshot(self, message: str):
        return paste_to_bash(self.provider.say(message))

    def run(self):
        logger.info("run")
        print(colorize(f"Whisperer: {self.provider}", ANSIColors.DIM))

        message = input("> ")

        while True:
            suggestion = self.provider.say(message)
            print(f"{colorize('? ' + suggestion, ANSIColors.BOLD_CYAN)}", end=" ")

            action = self._get_user_action()

            if action == UserAction.EXECUTE:
                logger.info("Pasting to bash: %s", suggestion)
                # pyperclip.copy(suggestion)
                paste_to_bash(suggestion)
                return

            elif action == UserAction.QUIT:
                print("Cancelled.")
                return
            elif action == UserAction.RETRY:
                message = "Try again, user wants something different."
            elif isinstance(action, str):  # custom feedback like "ok, but display human-readable file sizes"
                message = action

    def _get_user_action(self):
        print(colorize("[enter], [r]etry, feedback", f"{ANSIColors.DIM}{ANSIColors.GRAY}"))
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


def run_cli(oneshot=None):
    config.check_is_ready()
    session = Session()
    if not oneshot:
        session.run()
    else:
        session.oneshot(oneshot)
