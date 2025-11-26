# GitHub Copilot Instructions

## Project Overview
This repository contains Python course assignments covering fundamental Python concepts, data science basics, and bioinformatics tools.

## Project Structure
- `day01/` - Introduction to Python programming
- `day02/` - Calculator logic, geometry calculations, growth rate analysis (CLI and GUI versions)
- `day03/` - Calculator with unit tests
- `day04/` - NCBI client and GUI programs
- `day05/` - Advanced topics
- Root level: Miscellaneous Python scripts and utilities

## Coding Standards

### Python Style
- Follow PEP 8 conventions
- Use descriptive variable names (prefer full words over abbreviations)
- Include docstrings for all functions explaining parameters and return values
- Add comments for complex logic, especially in scientific calculations

### File Naming
- Use lowercase with underscores for Python files (e.g., `growth_rate_calculator.py`)
- Suffix files with descriptive names:
  - `_cli.py` or `_cmdline.py` for command-line interfaces
  - `_gui.py` for GUI versions
  - `_logic.py` for core calculation/business logic
  - `test_*.py` for unit test files

### Code Organization
- Separate business logic from UI (CLI/GUI)
- Core calculation functions should be in `*_logic.py` files
- CLI and GUI versions should import and use the logic modules
- Include input validation and error handling with clear error messages

### Scientific Computing
- Use appropriate libraries: `math`, `matplotlib`, `numpy` (when needed)
- Include units in variable names or comments (e.g., `time_hours`, `density_cells_per_ml`)
- Validate numeric inputs (check for positive values where required, handle division by zero)
- Use meaningful formulas with clear variable names matching scientific notation

### GUI Development
- Use `tkinter` for simple GUI applications
- Provide clear labels and instructions for user inputs
- Include error dialogs for invalid inputs
- Separate GUI code from calculation logic

### Command-Line Interfaces
- Use `sys.argv` for simple CLI tools or `argparse` for more complex interfaces
- Provide usage instructions when incorrect arguments are given
- Exit with appropriate error codes (0 for success, 1 for errors)
- Include example usage in help text

### Testing
- Write unit tests for core logic functions
- Test edge cases (zero, negative values, boundary conditions)
- Use descriptive test function names (e.g., `test_growth_rate_with_valid_input`)

### Documentation
- Include README.md files in subdirectories explaining the purpose of each assignment
- Document formulas and scientific concepts in comments
- Provide examples of expected input/output

### Common Patterns in This Repository
- Growth rate calculations using logarithmic formulas
- Geometry calculations (circle area, triangle properties)
- Calculator implementations with basic operations
- NCBI/bioinformatics API clients
- Mixed Hebrew and English comments/documentation (both are acceptable)

## Preferences
- Prefer explicit error messages over silent failures
- Use `float()` for scientific calculations requiring precision
- Include `if __name__ == "__main__":` guards for executable scripts
- Keep functions focused on single responsibilities
- Provide both interactive (input-based) and CLI (argument-based) versions where appropriate

## Bioinformatics Specifics
- When working with biological data, validate input formats
- Use appropriate scientific libraries when available
- Include references to formulas or methods used
- Handle API rate limits and connection errors gracefully
