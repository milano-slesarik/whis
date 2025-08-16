from .providers import registry
from .utils import ANSIColors, colorize


def run_smoke():
    print("Running smoke test...")
    provider = registry.create_by_env()
    if provider.is_available():
        print("Provider is available.", end=" ")
        print(provider)
    print("Asking for suggestion...", end=" ")
    print(colorize("list mp3 files", ANSIColors.BOLD_ORANGE))
    sug = provider.say("list mp3 files")
    print(f"Suggestion received: {colorize(sug, ANSIColors.BOLD_CYAN)}")
    print("OK. No errors found.")
    return
