# AI Assistant Project (THIS PROJECT IS IN PROGRESS: ADDING DOCKER AND FLASK FOR BETTER EXPERIENCE)

A local AI assistant for the terminal with web search and persistent memory, powered by [Ollama](https://ollama.com).

## Features

- **Conversational AI** — chat with a locally-running LLM via Ollama (default: `llama3.2`)
- **Web Search** — prefix any message with `search:` to pull live results from DuckDuckGo, with automatic page scraping for richer context
- **Persistent Memory** — conversation history is saved to `memory.json` and reloaded on startup, so context carries across sessions
- **Streaming responses** — output streams token-by-token for a responsive feel

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running locally with a model pulled (e.g. `ollama pull llama3.2`)

## Installation

```bash
git clone https://github.com/yourusername/ai-assistant-project.git
cd ai-assistant-project
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

### Commands

| Input | Action |
|---|---|
| Any text | Chat with the assistant |
| `search: your query` | Search the web and answer using live results |
| `clear memory` | Wipe conversation history |
| `quit` | Exit |

## Project Structure

```
ai-assistant-project/
├── main.py          # Entry point — main chat loop
├── memory.py        # Load, save, and clear conversation history
├── memory.json      # Auto-generated — persisted conversation history
├── requirements.txt
└── README.md
```

## Dependencies

```
openai
duckduckgo-search
requests
beautifulsoup4
```

Install with:

```bash
pip install openai duckduckgo-search requests beautifulsoup4
```

## How It Works

**Search** — when a `search:` query is detected, the assistant fetches the top 5 DuckDuckGo results, scrapes up to 1000 characters of text from each page, and injects that content into the prompt before generating a response.

**Memory** — every user message and assistant reply is appended to a list and written to `memory.json`. On startup, this file is read back in and passed as the full message history to Ollama, giving the model persistent context across sessions.

**Model** — the assistant uses Ollama's OpenAI-compatible API endpoint (`http://localhost:11434/v1`), so swapping models is as simple as changing the model string in `main.py`.

## Configuration

To use a different model, change the `model` field in `main.py`:

```python
response = client.chat.completions.create(
    model="llama3.2",  # swap for any model you have pulled in Ollama
    ...
)
```

## License

MIT
