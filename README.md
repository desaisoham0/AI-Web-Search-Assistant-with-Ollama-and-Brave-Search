# AI Web Search Assistant

Small terminal app that answers questions with local LLM reasoning plus fresh web snippets. It uses Ollama to run Gemma 3 locally, Brave Search for context, and Rich to render Markdown in the console.


## Features
- Local LLM via Ollama
- Web context from Brave Search
- Clean Markdown output in the terminal
- Simple test and CI setup

## How it works
1. Takes your question from stdin.
2. Fetches 5 recent web snippets with Brave Search.
3. Builds a prompt that includes the snippets and your question.
4. Calls the local model `gemma3:4b` through LangChain Ollama.
5. Prints a Markdown answer with citations the model includes in text.

## Requirements
- Python 3.11
- [Ollama](https://ollama.ai/) installed and running
- The model `gemma3:4b` available in Ollama
- A Brave Search API key

### Install Ollama and pull the model:
```bash
# Install Ollama from https://ollama.com
# Then pull the model
ollama pull gemma3:4b
```

## Setup
### Clone and create a virtual environment:
```bash
git clone <your-repo-url>
cd <your-repo-folder>

python -m venv .venv
source ./.venv/bin/activate   # Windows: .\.venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Set your environment variable. Create a file named `.env` in the project root:
```env
BRAVE_SEARCH_API_KEY=your_key_here
```

### Optional local git hooks:
```bash
pip install pre-commit
pre-commit install
```

## Run
```bash
python main.py
```

### Example:
```pgsql
------------------------------------
Ask your question (q to quit): What is the Rust borrow checker?

# model prints a Markdown answer here, with any URLs it chose to cite
```

Quit with `q.`

## Tests

### Run tests locally:

```bash
pytest -q
```

## Configuration

### Tweak defaults in `main.py`:
- **Model**: `OllamaLLM(model="gemma3:4b")`
- **Web result count**: `search_kwargs={"count": 5}`
- **Snippet length cap**: 300 chars

### You can swap models if they are available in Ollama:
```python
model = OllamaLLM(model="llama3.1:8b")
```
