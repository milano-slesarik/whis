import logging
import subprocess
import time
import os
import sys
from . import config
import pyperclip

logger = logging.getLogger(__name__)


def paste_to_bash(text):
    """
    Forks a child process that pastes the given suggestion to the clipboard.
    Needs xclip and xdotool installed.
    """
    try:
        pid = os.fork()
        if pid > 0:
            return
    except OSError as e:
        print(f"Error: Fork failed: {e}", file=sys.stderr)
        return

    # give the shell some time
    time.sleep(0.1)
    pyperclip.copy(text)
    # simulate ctrl+shift+v (linux terminal pasting)
    subprocess.run(
        ["xdotool", "key", "--clearmodifiers", "ctrl+shift+v"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


class ANSIColors:
    BOLD_CYAN = "\033[1;36m"
    BOLD_ORANGE = "\033[1;33m"
    RESET = "\033[0m"


def colorize(text, color):
    return f"{color}{text}{ANSIColors.RESET}"


def print_config():
    print("ENV:", config.ENV)
    print("version:", config.get_version())
    print("REPO_ROOT:", config.REPO_ROOT)
    print("PACKAGE_ROOT:", config.PACKAGE_ROOT)
    print("CONFIG_FILE:", config.CONFIG_FILE)
    print("LOG_FILE:", config.LOG_FILE)
    print("llm_provider:", config.llm_provider)
    print("llm_model:", config.llm_model)
    print("config_file_content:", config.config_toml)
    print("env vars:", {k: v for k, v in os.environ.items() if k.startswith("WHIS_")})
