# LLM UI Demo

This is a personal demo project for experimenting with Large Language Models (LLMs) using [Streamlit](https://streamlit.io/). The app provides a simple web interface to chat with LLMs via the [Ollama](https://ollama.com/) backend.

I intend to use this project as a starter template ui for projects with local language models. I don't intend to do significant development in this demo.

## Features

- Chat with LLMs in a web UI
- Select from available models
- Save and load chat history
- Session-based logging

## Requirements

- Python 3.12
- [Ollama](https://ollama.com/) installed and running locally
- [uv](https://github.com/astral-sh/uv) for dependency management
- [Streamlit](https://streamlit.io/)

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd ui
   ```

2. **(Optional, if not using `uv`) Set up a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Linux/macOS
   ```

3. **Install dependencies using uv:**
   ```sh
   uv sync
   ```

4. **Start Ollama:**
   Make sure Ollama is running locally and you have pulled at least one model, for example:
   ```sh
   ollama pull llama3.2:latest
   ```

5. **Run the Streamlit app:**
   ```sh
   uv run streamlit run src/app.py
   ```

6. **Open your browser:**
   Visit [http://localhost:8501](http://localhost:8501) to use the app.

## Notes

- Chat logs and saved chats are stored in the `logs` and `saved-chats` directories.
- This is a personal project I intend to use as a demo template when using local language models.