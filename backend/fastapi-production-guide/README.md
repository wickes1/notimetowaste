# FastAPI Production Guide

## Setup

```bash
poetry config --list
# setup to create .venv in project directory
poetry config virtualenvs.in-project true

poetry add fastapi 'uvicorn[standard]'
poetry add -G dev ruff black mypy
poetry add python-dotenv pydantic-settings

# Async MongoDB driver
poetry add motor
# Motor stub
poetry add -G dev motor-types
```

Extra config for dev tools:

```toml
[tool.black]
line-length = 88

[tool.ruff]
select = ["E", "F", "I"]
fixable = ["ALL"]
exclude = [".git", ".mypy_cache", ".ruff_cache"]
line-length = 88

[tool.mypy]
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_return_any = true
strict_equality = true
disallow_untyped_decorators = false
ignore_missing_imports = true
implicit_reexport = true
plugins = "pydantic.mypy"

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true
warn_untyped_fields = true
```

## Reference

[FastAPI Production Setup Guide 🏁⚡️🚀](https://dev.to/dpills/fastapi-production-setup-guide-1hhh)
[GitHub - dpills/fastapi-prod-guide: FastAPI Production Setup Guide ⚡️🚀🏁](https://github.com/dpills/fastapi-prod-guide)
