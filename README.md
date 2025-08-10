# A tiny Linux command whisperer (WHIS)

Blah blah...
A tiny Linux command whisperer/generator.

The main goals:
- lightweight
- simple
- fast
- free and unlimited (LLM requests)
- 
I'm building it to use it with local (free and fast) LLMs (Ollama) but works with common external APIs too. 

## Usage

# ![Showcase](_showcase.gif)

# Todo

- get configuration variables from a config file
- `explain` command that sends request for a brief explanation of the command
  - should use a new conversation without a previous context
- `continue` - loads old session and continues refining
- API support
  - Gemini
  - Anthropic
- dangerous commands red warning (e.g. `rm` stuff)
- `whis` inner history - arrow up should get the latest input even after session restart
- `whis config` - change settings - provider, model, whether to paste or just copy (maybe execute later)
- other modes (current "quit then paste" feels unreliable)
  - copy to clipboard
  - execute directly
- tests
- checks - precommit
  - flake8
  - black
  - isort
  - mypy
- more info in system prompt (OS, pwd...)
- command syntax check before suggestion
