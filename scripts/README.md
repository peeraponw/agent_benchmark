# Scripts Directory

This directory contains utility scripts for the AI Agent Frameworks Comparison Project, running in an isolated UV environment.

## Environment Setup

The scripts use their own UV-managed environment with dedicated dependencies:

```bash
cd scripts/
uv sync  # Install dependencies
```

## Available Scripts

### `validate_structure.py`
Validates the project structure against specifications with enhanced rich formatting.

**Usage:**
```bash
uv run python validate_structure.py
```

**Features:**
- Validates framework directories and structure
- Checks Docker template syntax and configuration
- Validates environment template completeness
- Verifies JSON file structure and syntax
- Enhanced output with Rich formatting and tables
- 77 comprehensive validation checks

## Dependencies

- **PyYAML**: For Docker template validation
- **Pydantic**: For data validation and modeling
- **Rich**: For enhanced terminal output formatting

## Development

To add new scripts:

1. Create the script in this directory
2. Add any new dependencies with `uv add <package>`
3. Update this README with usage instructions
4. Ensure scripts follow the project's Python standards

## Execution

Always use `uv run` to execute scripts to ensure they run in the correct isolated environment:

```bash
# Correct
uv run python script_name.py

# Incorrect (may use wrong environment)
python script_name.py
```
