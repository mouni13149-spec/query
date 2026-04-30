# Contributing

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Tests

```powershell
pytest
```

## Guidelines

- Keep generated SQL read-only by default.
- Add tests for new natural-language patterns and validation rules.
- Do not commit production databases or credentials.

