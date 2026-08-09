# Project

We are building an educative workshop teaching people how to build AI systems by implementing a hybrid AI system containing a Deep Research Agent and a Writing Workflow, both served as MCP servers and connected to a harness such as Claude Code or Cursor.

# Project Structure

```
project-root/
├── src/
│   ├── research/              # Deep Research Agent MCP server
│   │   ├── server.py          # FastMCP entry point
│   │   ├── config/            # Settings, constants, prompt templates
│   │   ├── models/            # Pydantic schemas for structured LLM output
│   │   ├── app/               # Business logic handlers
│   │   ├── tools/             # MCP tool implementations
│   │   ├── routers/           # MCP tool, resource, and prompt registration
│   │   └── utils/             # Gemini client, file I/O, markdown helpers
│   └── writing/               # LinkedIn Writer MCP server
│       ├── server.py          # FastMCP entry point
│       ├── profiles/          # Shipped markdown profiles (structure, terminology, character)
│       ├── config/            # Settings, constants, prompt templates
│       ├── models/            # Pydantic schemas (Post, Review, Profiles)
│       ├── app/               # Business logic handlers (writer, reviewer, image, profile loader)
│       ├── tools/             # MCP tool implementations
│       ├── routers/           # MCP tool, resource, and prompt registration
│       └── utils/             # Gemini client helpers (text + Imagen)
├── inputs/                    # Seed and guideline files
├── scripts/                   # Entrypoints and test scripts
└── .env.example               # All supported env vars
```

# Tech Stack

- Data validation and structuring: Pydantic
- Settings: Pydantic Settings
- MCP Server Framework: FastMCP
- CLI: Click
- Logging: Native Python logger (never prints!)
- LLM API: Gemini
- Observability and evals: Opik

## Access Documentation
Use the context7 MCP server to find out more about the tech stack usage and good practices.

# Doing Research

This project is built around a Deep Research Agent. For ANY research or investigation task, use this project's own tooling — the `deep_research` MCP server (or the `research` / `deep-research` skill) — not generic `WebSearch`/`WebFetch`. Reserve raw `WebSearch`/`WebFetch` for quick, single-fact lookups that don't warrant a research run, and even then prefer the project tooling when in doubt.

More broadly: **before choosing tools for a task, check whether a project skill or MCP server already covers it.** A simple-looking request is not a reason to skip this check — that is exactly when the generic default wrongly wins.

# Running QA

We use ruff as our formatter and linter.

First always fix the formatting and linting errors with the fix commands:
```
make format-fix
make lint-fix
```
Then, check if there are any errors that couldn't be fixed automatically and fix them:
```
make format-check
make lint-check
```

# Running Code

We manage all the core commands through GNU Make as our command center. File available at @Makefile. Run all the commands with `make ...`

We use uv to manage our Python project such as the virtual environment(s), dependencies, and overall package the project.

Thus, use uv to run any custom command that is not present in the @Makefile, but uses Python: `uv run python ...`

## Fallback when `make` is not installed

Some environments (fresh WSL, minimal containers, corporate dev images) ship without GNU Make. **Do not block on a missing `make`** — every target in the Makefile is a thin wrapper around a one-line `uv run ...` invocation. When `make <target>` fails with `command not found: make`, open the `Makefile`, find the target's recipe, and run the underlying command directly. Example: `make test-research-workflow` becomes `uv run python scripts/test_research_workflow.py --working-dir test_logic --iterations 2` (after the two `mkdir -p` / `cp` setup lines also shown in the recipe). The Makefile's `export PYTHONPATH=./src/` and `include .env` are already handled by `uv run` reading the project's environment + `.env`, so no extra shell setup is needed.
