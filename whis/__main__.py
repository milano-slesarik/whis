import argparse
from . import config, utils
from .cli import run_cli
from .smoke import run_smoke


def main():
    parser = argparse.ArgumentParser(
        prog="whis",
        description="Suggest a shell command from a natural-language prompt.",
        epilog=(
            "Usage:\n"
            "  1. Write your request in natural language\n"
            "  2. After a suggestion appears, choose:\n"
            "     • [enter] quit+paste the command into your terminal\n"
            "     • [r] retry\n"
            "     • refine the command by writing a feedback message\n"
            "\n"
            "Note: After [enter], the command is automatically pasted into your terminal."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("--version", action="store_true", help="Show version.")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("run", help="Start interactive session")
    # subparsers.add_parser("setup", help="Run interactive configuration")
    subparsers.add_parser("smoke", help="Run a quick smoke test")

    args = parser.parse_args()

    if args.version:
        print(config.get_version())
        return

    cmd = args.command or "run"
    if cmd == "run":
        run_cli()
    elif cmd == "smoke":
        run_smoke()


if __name__ == "__main__":
    if config.is_dev:
        utils.print_config()
    main()
