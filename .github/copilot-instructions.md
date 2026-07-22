# Copilot instructions for `cli-url-shortener`

## Build, test, and lint commands

This repository uses **uv** (`pyproject.toml` + `uv.lock`).

- Install dependencies: `uv sync`
- Run API server: `uv run python run_api.py`
- Run CLI app: `uv run python run_cli.py`
- Run all tests: `uv run pytest -q`
- Run a single test: `uv run pytest tests/test_shorten.py::test_shorten_url -q`

No dedicated lint or formatter command is configured in the repository at the moment.

## High-level architecture

This project has two entrypoints over one URL-shortener domain:

1. **HTTP API (FastAPI)**  
   `run_api.py` starts `src.api.server.server:app`.  
   Routers are split into:
   - `src/api/routes/shortener_routes.py`: create short URLs, list links, stats
   - `src/api/routes/redirect_routes.py`: resolve `/{short_id}` and record access events

2. **CLI client (Typer + Rich)**  
   `run_cli.py` starts `src.cli.app`.  
   Commands in `src/cli/commands/url_commands.py` call HTTP endpoints via `src/cli/client/api_client.py` and render output with `src/cli/ui/display.py`.

Data is persisted with **SQLModel** (`src/api/models/shortener_models.py`) using two tables:
- `URL` (original URL)
- `URLAccess` (each redirect access, with timestamp/user-agent/referrer/IP)

`short_id` is derived from the numeric DB id using base62 helpers in `src/api/core/base62.py`.

## Key conventions in this codebase

- **Error response contract is standardized** in `src/api/server/server.py` as:
  ```json
  {"error": {"code": "...", "message": "...", "details": ...}}
  ```
  Keep this structure and use existing exception handlers when adding new API errors.

- **Validation messages are domain-specific and in Portuguese**. URL validation lives in `URLrequest` validators (`src/api/schemas/shortener_schemas.py`) and rejects local/private network targets.

- **URL normalization is done on both sides**:
  - API schema validators normalize incoming URL before persistence
  - CLI client normalizes user input before API requests
  Preserve both paths when adjusting URL handling.

- **Configuration comes from `.env` via `pydantic-settings`**:
  - API expects: `database_url`, `base_url`, `app_host`, `app_port`
  - CLI expects: `base_url`
  Keep new settings in these typed settings modules instead of reading env vars ad hoc.

- **Tests override DB dependency via FastAPI dependency injection** (`tests/conftest.py`) using in-memory SQLite + `StaticPool`; follow this pattern for API tests that need persistence.
