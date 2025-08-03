import logging
import subprocess
import time
import os
import sys

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
        ['xdotool', 'key', '--clearmodifiers', 'ctrl+shift+v'],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
