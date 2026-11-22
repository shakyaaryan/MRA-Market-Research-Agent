# Multi-Agent Market Research App

A basic Streamlit application that generates a short market research brief using a sequential multi-agent workflow.

## Workflow

1. **Orchestrator** initializes the research state and controls the workflow.
2. **Researcher** searches the web using Tavily and returns source-backed findings.
3. **Analyst** creates a Markdown research brief using the findings.
4. **Critic** reviews the draft. If it is not approved, the analyst gets one opportunity to revise it.
5. The final brief and collected evidence are displayed in Streamlit.

The agents share information through a LangGraph state. Pydantic models validate individual research findings and critic reviews.

## Technology stack

- Python 3.13 or newer
- uv
- Streamlit
- LangGraph
- LangChain Openrouter
- Openrouter API
- Tavily Search API
- Pydantic
- python-dotenv

## Requirements

You need API keys for:
- openrouter: https://openrouter.ai/
- Tavily: https://app.tavily.com/

## Setup on Windows PowerShell

Install `uv` if it is not already installed. Then:

```powershell
git clone https://github.com/shakyaaryan/MRA-Market-Research-Agent.git
cd MRA-Market-Research-Agent

uv sync
Copy-Item .env.example .env
```

Open `.env` and add your real API keys:

```env
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
OPENROUTER_MODEL=deepseek/deepseek-v4.1-flash
```

The model name is configurable. If that model is unavailable, set `OPENROUTER_MODEL` to a currently supported model from https://openrouter.ai/models.

Run the application:

```powershell
uv run streamlit run src/app.py
```

Streamlit will print a local URL, usually http://localhost:8501.

## Setup on macOS / Linux

```bash
git clone https://github.com/shakyaaryan/MRA-Market-Research-Agent.git
cd MRA-Market-Research-Agent

uv sync
cp .env.example .env
```

Add your API keys to `.env`, then run:

```bash
uv run streamlit run src/app.py
```

## Example query

```text
Analyze the food delivery market in Nepal.
```

## Sample output

See [sample output](sample_outputs/sample_report.md).