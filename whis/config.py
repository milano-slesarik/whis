import logging
import os
import tomllib
from datetime import datetime
from enum import Enum
from importlib import metadata
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    pass  # ok if dotenv is not installed
else:
    load_dotenv()


class Env(str, Enum):
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


ENV = os.environ.get("WHIS_ENV", Env.PROD)

is_dev = ENV == Env.DEV

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "whis"

if ENV == "dev":
    CONFIG_FILE = REPO_ROOT / "config.dev.toml"
    LOG_FILE = REPO_ROOT / "whis.dev.log"
else:
    XDG_CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")).expanduser()
    XDG_STATE_HOME = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")).expanduser()

    CONFIG_FILE = XDG_CONFIG_HOME / "whis" / "config.toml"

    LOG_DIR = XDG_STATE_HOME / "whis"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = str(LOG_DIR / "whis.log")

    # ~/.config/whis/config.toml might not exist yet, so we create it here with default values
    # from config.template.toml
    if not CONFIG_FILE.exists():
        template_text = (PACKAGE_ROOT / "config.template.toml").read_text()
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(template_text)

config_toml = tomllib.loads(CONFIG_FILE.read_text())

llm_provider = os.environ.get("WHIS_PROVIDER", config_toml.get("llm_provider"))  # ollama, openai...
llm_model = os.environ.get("WHIS_MODEL", config_toml.get("llm_model"))  # gpt-3.5-turbo, gpt-4, qwen2:7b...

LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 1024 * 1024 * 5  # 5 MB
LOG_BACKUP_COUNT = 5


def setup_logging():
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": LOG_FORMAT, "datefmt": LOG_DATE_FORMAT},
        },
        "handlers": {
            "console": {
                "level": "ERROR",  # it's a cli tool - no logs to the console
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_FILE,
                "maxBytes": LOG_MAX_BYTES,
                "backupCount": LOG_BACKUP_COUNT,
                "encoding": "utf-8",  # todo is it necessary?
            },
        },
        "root": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
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
