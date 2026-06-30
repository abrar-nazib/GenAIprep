# uv Cheatsheet

## Projects

- Create a project: `uv init`
- Create with a Python requirement: `uv init --python <version>`
- Create an app/library: `uv init --app` / `uv init --lib`
- Create in a new directory: `uv init <name>`

Recommended setup order:

```bash
mkdir <project>
cd <project>
uv python pin <version>
uv init
uv add <packages>
```

`uv python pin` can run before `uv init`; it creates `.python-version`, which
`uv init` uses for the project's `requires-python` value.

## Dependencies

- Add a package: `uv add <package>`
- Add a specific version: `uv add '<package>==1.2.3'`
- Add a development dependency: `uv add --dev <package>`
- Add from requirements: `uv add -r requirements.txt`
- Remove a package: `uv remove <package>`
- Upgrade one package: `uv lock --upgrade-package <package>`
- Upgrade all packages: `uv lock --upgrade`
- Show the dependency tree: `uv tree`

## Lock and Sync

- Update the lockfile: `uv lock`
- Create/update `.venv` from `uv.lock`: `uv sync`
- Verify the lockfile is current: `uv lock --check`
- Sync without changing the lockfile: `uv sync --locked`
- Export requirements: `uv export --format requirements.txt -o requirements.txt`

`uv sync` requires an initialized project and removes undeclared packages by
default. `uv add` updates the lockfile and syncs automatically.

## Run

- Run a script: `uv run path/to/script.py`
- Run a module: `uv run python -m module.name`
- Run a project command: `uv run <command>`
- Run with a temporary dependency: `uv run --with <package> <command>`

`uv run` automatically locks and syncs the project environment.

## Python Versions

- Install Python: `uv python install <version>`
- List available/installed versions: `uv python list`
- Pin the project version: `uv python pin <version>`
- Create `.venv`: `uv venv`
- Create at a specific path: `uv venv <path>`
- Create with a specific Python version: `uv venv --python <version>`

## Tools

- Run a tool temporarily: `uvx <tool>`
- Install a tool globally: `uv tool install <tool>`
- Upgrade installed tools: `uv tool upgrade --all`
- List installed tools: `uv tool list`
- Uninstall a tool: `uv tool uninstall <tool>`

## pip-Compatible Workflows

- Install from requirements: `uv pip install -r requirements.txt`
- Sync exactly from requirements: `uv pip sync requirements.txt`
- Compile requirements: `uv pip compile requirements.in -o requirements.txt`
- List installed packages: `uv pip list`
- Show package details: `uv pip show <package>`
- Check dependency conflicts: `uv pip check`
