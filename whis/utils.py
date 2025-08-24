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
    GRAY = "\033[90m"
    DIM = "\033[2m"  # less visible than GRAY
    RESET = "\033[0m"


def colorize(text, color):
    return f"{color}{text}{ANSIColors.RESET}"


def get_whis_env_vars():
    return {k: v for k, v in os.environ.items() if k.startswith("WHIS_")}


def print_config():
    print(colorize(f"Python version: {sys.version}", ANSIColors.GRAY))
    print(colorize(f"ENV: {config.ENV}", ANSIColors.GRAY))
    print(colorize(f"version: {config.get_version()}", ANSIColors.GRAY))
    print(colorize(f"REPO_ROOT: {config.REPO_ROOT}", ANSIColors.GRAY))
    print(colorize(f"PACKAGE_ROOT: {config.PACKAGE_ROOT}", ANSIColors.GRAY))
    print(colorize(f"CONFIG_FILE: {config.CONFIG_FILE}", ANSIColors.GRAY))
    print(colorize(f"LOG_FILE: {config.LOG_FILE}", ANSIColors.GRAY))
    print(colorize(f"llm_provider: {config.llm_provider}", ANSIColors.GRAY))
    print(colorize(f"llm_model: {config.llm_model}", ANSIColors.GRAY))
    print(colorize(f"config_file_content: {config.config_toml}", ANSIColors.GRAY))
    env_vars_str = " ".join(f"{k}={v}" for k, v in get_whis_env_vars().items())
    print(colorize(f"ENV: {env_vars_str}", ANSIColors.GRAY))
