import logging
import os

try:
    import tomllib
except ImportError:  # py <= 3.10
    import tomli as tomllib
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


ENV = os.environ.get("WHIS_ENV", Env.PROD).lower()

is_dev = ENV == Env.DEV
is_prod = ENV == Env.PROD
is_test = ENV == Env.TEST

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "whis"
SYSTEM_PROMPT_FILE = PACKAGE_ROOT / "system_prompt.txt"
CONFIG_FILE = None

if is_dev:
    LOG_FILE = REPO_ROOT / "whis.dev.log"
    config_toml = {}
elif is_test:
    LOG_FILE = Path("/tmp/whis.test.log")
    config_toml = {}
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


def get_cfg_var(key: str, default=None):
    """
    First try env var named as WHIS_<UPPER_SNAKE_KEY> then config.toml.
    """
    val = os.environ.get(f"WHIS_{key.upper()}")
    if val is not None:
        return val
    return config_toml.get(key, default)


llm_provider = get_cfg_var("llm_provider")  # ollama, openai...
llm_model = get_cfg_var("llm_model")  # gpt-3.5-turbo, gpt-4, qwen2:7b...
llm_temp = get_cfg_var("llm_temp")  # 0.2

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


def load_system_prompt():
    prompt = SYSTEM_PROMPT_FILE.read_text()
    context = {
        "current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return prompt.format(**context)


def get_version() -> str:
    """Returns version. For development, we parse it from the pyproject.toml."""
    try:
        repo_root = Path(__file__).resolve().parents[1]
        pyproject = repo_root / "pyproject.toml"
        if pyproject.is_file():
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            return data.get("project", {}).get("version", "COULD_NOT_DETECT_VERSION")
    except Exception:
        pass

    try:
        return metadata.version("whis")
    except metadata.PackageNotFoundError:
        pass

    return "COULD_NOT_DETECT_VERSION"


class NotReadyError(Exception):
    """Raised when required config vars are not set"""

    missing_vars = []

    def __init__(self, message, missing_vars):
        super().__init__(message)
        self.missing_vars = missing_vars


REQUIRED_CONFIG_KEYS = ["llm_provider", "llm_model"]


def check_is_ready():
    missing_vars = []
    for var in REQUIRED_CONFIG_KEYS:
        if not get_cfg_var(var):
            missing_vars.append(var)
    if missing_vars:
        raise NotReadyError(f"Required config vars not set: {missing_vars}", missing_vars)


SYSTEM_PROMPT = load_system_prompt()
