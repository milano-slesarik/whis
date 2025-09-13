# A tiny Linux command whisperer


**WHIS** is a tiny Linux command whisperer/generator based on **LLM**, written in **Python**.

## ! An Important Note on Usage and Safety !

Think of **whis** as a "whisperer" for the commands you already know but can't quite remember.  It is a tool for
experienced users who can recognize dangerous commands.
```
Never execute a suggested command without fully understanding its function and potential consequences or at least
without knowing it's not dangerous.
Blindly trusting AI-generated commands is dangerous and can lead to data loss. That's why **whis** doesn't execute
commands but only prepares them for you to the terminal.
```

## The main goals are:
- minimal interruption of the workflow
- speed
- free and unlimited suggestions (with local LLM)
- privacy (with local LLM)
- minimalistic interface

## Alpha version
Please note that this is an Alpha version and might not work as expected.
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
   - b) Environment variables (have priority over the config file)
     - `WHIS_LLM_PROVIDER`
     - `WHIS_LLM_MODEL`
4. Run `whis` interactive session by running `whis` in terminal


## Todo

Todo was moved to [Issues](https://github.com/milano-slesarik/whis/issues)
