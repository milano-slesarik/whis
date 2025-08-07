import logging
import os
from datetime import datetime
from importlib import metadata
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LOG_DIR = os.path.expanduser("~/.local/share/whis")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "whis.log")

LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 1024 * 1024 * 5 # 5 MB
LOG_BACKUP_COUNT = 5


def setup_logging():
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': LOG_FORMAT,
                'datefmt': LOG_DATE_FORMAT
            },
        },
        'handlers': {
            'console': {
                'level': 'ERROR',  # it's a cli tool - no logs to the console
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_FILE,
                'maxBytes': LOG_MAX_BYTES,
                'backupCount': LOG_BACKUP_COUNT,
                'encoding': 'utf-8',  # todo is it necessary?
            }
        },
        'root': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        "loggers": {
            # silence third-party loggers
            "urllib3": {"level": "WARNING", "propagate": True},
            "httpx": {"level": "WARNING", "propagate": True},
            "openai": {"level": "WARNING", "propagate": True},
            "ollama": {"level": "WARNING", "propagate": True},
            "httpcore": {"level": "WARNING", "propagate": True},
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.captureWarnings(True)

whis_provider = os.environ.get("WHIS_PROVIDER", "ollama")
whis_model = os.environ.get("WHIS_MODEL", "qwen2:7b")


SYSTEM_PROMPT = f"""
You are an expert Linux shell assistant. Your goal is to translate a user's request into a runnable bash command.

# Context:
- The ENTIRE conversation is about creating ONE command based on the user request.

# Strict Output Rules:
- Your response MUST contain ONLY the raw command.
- Do NOT include any explanations, comments, markdown, or any text that is not part of the command.
- Do NOT write "Feedback:" or simulate a user conversation. Your output must be directly executable.
- Do NOT add echo statements, progress messages, or status updates.
- Do NOT chain commands with pipes unless specifically requested or necessary.
- Do NOT add xargs unless the user explicitly needs it.
- Remember: Simplicity is key.

# Behavior Rules:
- If the user's prompt is a correction, apply it to the last command you generated.
- Never escalate a safe command (like `find`) to a destructive one (like `rm`) unless explicitly asked.
- For file searching, prefer simple direct commands.
- Be minimal and conservative - give exactly what is asked for, nothing more.
- Do not be proactive. If command has standard default params, it's not needed to redefine them unless asked.
- Basically suggest MVP that fits the users description.
- When using a specific filename or path that contains spaces, always enclose it in quotes.

# Common Feedback Patterns for Command Refinement:
- "this dir" or "current dir" or "here" → modify previous command to search only current directory (add -maxdepth 1 to find, or use ls)
- "recursive" → ensure command searches subdirectories 

# Examples:
- Initial: "list txt files" → `find . -type f -name '*.txt'`
- Feedback: "this dir" → `find . -maxdepth 1 -type f -name '*.txt'` (SAME task, refined scope)
- NOT: `pwd` (this would be a different task entirely)

# Useful Information
- Current date and time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""


def get_version() -> str:
    """Returns version. For development, we parse it from the pyproject.toml."""
    try:
        import tomllib  # Python 3.11+
        repo_root = Path(__file__).resolve().parents[1]
        pyproject = repo_root / "pyproject.toml"
        if pyproject.is_file():
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            return data.get("project", {}).get("version", "COULD_NOT_DETECT_VERSION")
    except Exception:
        pass

    try:
        return metadata.version("whis-cli")
    except metadata.PackageNotFoundError:
        pass

    return "COULD_NOT_DETECT_VERSION"
