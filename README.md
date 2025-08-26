# A tiny Linux command whisperer (Alpha version)


WHIS is a tiny Linux command whisperer/generator based on LLM, written in Python.

The main goals are:
- minimal interruption of the workflow
- fast
- free and unlimited suggestions (with local LLM)
- privacy (with local LLM)
- minimalistic interface

## Alpha version
Please note that this is an Alpha version and is not ready for production use.<br/>
So far it's only tested on **Ubuntu 24.04** and **Python 3.12**.

## Usage

# ![Showcase](_showcase.gif)

## Install

1. Install pipx
   - Follow the official guide: https://github.com/pipxproject/pipx
2. Install WHIS with pipx
   - `pipx install whis`
3. Configure your provider and model by either
   - a) Config file: `~/.config/whis/config.toml` (or `XDG_CONFIG_HOME/whis/config.toml` if you use a different location)
     - create/edit the file with:
       ```toml
       llm_provider = "ollama"   # e.g. ollama, openai
       llm_model = "qwen2:7b"    # e.g. qwen2:7b, gpt-4o-mini
       ```
   - b) Environment variables (have priority over config file)
     - `WHIS_LLM_PROVIDER`
     - `WHIS_LLM_MODEL`
4. Run `whis` interactive session by running `whis` in terminal

---
## Todo (business logic)

- one-shot mode: `whis "list mp3 files"` without the interactive session
- `explain` command that sends request for a brief explanation of the command
  - should use a new conversation without a previous context
- `continue` - loads old session and continues refining
- API support
  - Gemini
  - Anthropic
  - OpenAI-compatible API (LM Studio, LocalAI...)
- dangerous commands red warning (e.g. `rm` stuff)
- `whis` inner history - arrow up should get the latest input even after session restart
- #### interactive configuration
  - `whis config`
    - **provider, model**
    - **action** - copy+paste, copy, maybe execute?
- other modes (current "quit then paste" feels unreliable)
  - copy to clipboard
  - execute directly (dangerous)
- more dynamic context in system prompt (OS, pwd, git branch, etc.) - some might need user permission
- command syntax check before suggestion
- use one specific color for all responses and another for user inputs

## Todo (technical)
- Python versions support (3.10+)
- tests
- consider [click](https://github.com/pallets/click/) for CLI
- checks
  - flake8
  - black
  - isort
  - mypy
- better command pasting (now it uses xdotool and xclip with process forking) using bash functions
- there seems to be a conflict between `black` and `ruff`
