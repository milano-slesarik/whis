# A tiny Linux command whisperer (WHIS)


A tiny Linux command whisperer/generator based on LLM, written in Python.

The main goals are:
- minimal interruption of the workflow
- fast
- free and unlimited suggestions (with local LLM)
- privacy (with local LLM)
- minimalistic interface


## Usage

# ![Showcase](_showcase.gif)

# Todo (business logic)

- one-shot mode: `whis "list mp3 files"` without the interactive session
- get configuration variables from a config file
- `explain` command that sends request for a brief explanation of the command
  - should use a new conversation without a previous context
- `continue` - loads old session and continues refining
- API support
  - Gemini
  - Anthropic
  - OpenAI-compatible API (LM Studio, LocalAI...)
- dangerous commands red warning (e.g. `rm` stuff)
- `whis` inner history - arrow up should get the latest input even after session restart
- `whis config` - change settings - provider, model, whether to paste or just copy (maybe execute later)
- other modes (current "quit then paste" feels unreliable)
  - copy to clipboard
  - execute directly (dangerous)
- more dynamic context in system prompt (OS, pwd, git branch, etc.) - some might need user permission
- command syntax check before suggestion
- use one specific color for all responses and another for user inputs

# Todo (technical)

- tests
- consider [click](https://github.com/pallets/click/) for CLI
- checks - precommit
  - flake8
  - black
  - isort
  - mypy
- better command pasting (now it uses xdotool and xclip with process forking) using bash functions
- there seems to be a conflict between `black` and `ruff`
