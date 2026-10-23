# ⚡ NVIDIA Nemotron 3 Ultra - LangChain Chat Agent

A production-ready conversational AI agent built with **LangChain**, **LangGraph**, and **NVIDIA Nemotron 3 Ultra** (`nvidia/nemotron-3-ultra-550b-a55b`).

Nemotron 3 Ultra is NVIDIA's flagship 550B-parameter Mixture-of-Experts (MoE) reasoning model engineered specifically for autonomous agent orchestration, complex multi-step reasoning, and precision tool calling.

---

## 🌟 Features

- **NVIDIA NIM Integration**: Native integration with NVIDIA Foundation Models via `ChatNVIDIA` (or OpenAI-compatible NIM endpoint).
- **Tool-Augmented Reasoning**:
  - 🌐 **Live Web Search** (`DuckDuckGo`) for current events and documentation.
  - 🧮 **Safe Calculator** for complex mathematical computations.
  - 🕒 **DateTime & Timezone** queries.
- **Persistent Memory**: Stateful multi-turn conversation memory with thread-level persistence via LangGraph `MemorySaver`.
- **Dual Interfaces**:
  - 💻 **Interactive CLI**: Colored terminal chat with real-time tool execution logs.
  - 🌐 **Modern Web UI**: Streamlit web chat with session management.

---

## 📁 Project Structure

```text
LangchainAgent/
├── config.py          # Configuration and environment validation
├── tools.py           # Agent tools (Web search, Calculator, DateTime)
├── agent.py           # LangGraph ReAct agent & ChatNVIDIA setup
├── main.py            # Terminal / CLI interactive chat application
├── app.py             # Streamlit web chat interface
├── requirements.txt   # Python package dependencies
├── .env.example       # Example configuration file
└── README.md          # Project documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.11)
- An NVIDIA API Key.

### 2. Get an NVIDIA NIM API Key
1. Visit the [NVIDIA API Catalog](https://build.nvidia.com/).
2. Select any model (e.g., [Nemotron](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b)).
3. Click **Get API Key** and generate your key (starts with `nvapi-...`). Free credits are provided.

### 3. Setup Virtual Environment & Install Dependencies
Open your terminal in the project directory:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.venv\Scripts\activate.bat
# Linux / macOS:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your API key:
```env
NVIDIA_API_KEY=nvapi-your-key-here
NVIDIA_MODEL=nvidia/nemotron-3-ultra-550b-a55b
```

---

## 💬 Running the Chat Agent

### Option A: Interactive Terminal Interface (CLI)
Run:
```bash
python main.py
```
**In-Chat Commands:**
- `/help` — Display command guide.
- `/tools` — Show list of available tools.
- `/clear` — Start a fresh conversation thread.
- `/exit` — Quit the application.

### Option B: Web UI (Streamlit)
Run:
```bash
streamlit run app.py
```
This opens an interactive chat UI in your default web browser (`http://localhost:8501`).

---

## 🛠️ Adding Custom Tools

You can easily register new tools in [`tools.py`](file:///d:/VS%20Code%202/LangchainAgent/tools.py) using LangChain's `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def get_stock_price(ticker: str) -> str:
    """Fetch the latest stock price for a given ticker symbol."""
    # Your logic here
    return f"{ticker}: $150.00"

# Add it to the agent_tools list:
agent_tools = [get_current_datetime, calculate, search_web, get_stock_price]
```

---

## 🔄 Supported Models

You can change `NVIDIA_MODEL` in `.env` to any model in the NVIDIA NIM catalog:
- `nvidia/nemotron-3-ultra-550b-a55b` *(Default - Nemotron 3 Ultra Flagship MoE)*
- `nvidia/llama-3.1-nemotron-70b-instruct`
- `nvidia/nemotron-4-340b-instruct`
- `nvidia/nemotron-mini-4b-instruct`
