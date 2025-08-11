from .providers import registry
from .utils import ANSIColors, colorize


def run_smoke():
    print("Checking provider and model...", end=" ")
    provider = registry.create_by_env()
    if provider.is_available():
        print(f"{provider.label} ({provider.model})")  # todo create method on provider
    print("Asking for suggestion...", end=" ")
    print(colorize("list mp3 files", ANSIColors.BOLD_ORANGE))
    sug = provider.say("list mp3 files")
    print(f"whis: {colorize(sug, ANSIColors.BOLD_CYAN)}")
    print("OK. No errors found.")
    return
