# Contributing to ImageGhost

First off, thank you for considering contributing to ImageGhost! It's people like you that make ImageGhost such a great tool for the security community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
- Check the [documentation](README.md) to see if you can resolve the issue yourself
- Search [existing issues](https://github.com/yourusername/imageghost/issues) to see if the problem has already been reported
- Collect relevant information (OS, Python version, error messages, logs)

**How to submit a good bug report:**

Create an issue with the following template:

```markdown
## Bug Description
A clear and concise description of what the bug is.

## To Reproduce
Steps to reproduce the behavior:
1. Run command '...'
2. With input files '...'
3. See error

## Expected Behavior
A clear description of what you expected to happen.

## Environment
- OS: [e.g., Kali Linux 2024.1]
- Python Version: [e.g., 3.11.2]
- ImageGhost Version: [e.g., 3.0]
- Installation Method: [pip/git clone]

## Logs/Error Messages
```
Paste error messages or logs here
```

## Additional Context
Any other context about the problem.
```

### Suggesting Enhancements

**Before submitting an enhancement:**
- Check if the enhancement already exists in the latest version
- Search [existing issues](https://github.com/yourusername/imageghost/issues) for similar suggestions
- Consider if your idea fits the project scope

**How to submit a good enhancement:**

Create an issue with the following template:

```markdown
## Enhancement Description
A clear description of the feature or improvement.

## Motivation
Why is this enhancement needed? What problem does it solve?

## Proposed Solution
How should this be implemented?

## Alternatives Considered
What other approaches have you considered?

## Additional Context
Any mockups, examples, or references.
```

### Pull Requests

**Before submitting a PR:**
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

**PR Guidelines:**
- Follow the [coding standards](#coding-standards)
- Include tests for new features
- Update documentation
- Keep PRs focused on a single feature/fix
- Reference any related issues

**PR Template:**

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] I have tested these changes locally
- [ ] I have added/updated tests
- [ ] All tests pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Changelog updated (if applicable)

## Related Issues
Fixes #(issue number)
```

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/imageghost.git
cd imageghost
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
# Production dependencies
pip3 install -r requirements.txt

# Development dependencies
pip3 install pytest pytest-cov black flake8 mypy bandit
```

### 4. Install System Dependencies

```bash
# Debian/Ubuntu/Kali
sudo apt install exiftool dcraw

# Arch Linux
sudo pacman -S perl-image-exiftool dcraw
```

### 5. Run Tests

```bash
# Run all tests
./run_tests.sh

# Or manually
pytest tests/ -v --cov=core --cov-report=html
```

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line Length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Single quotes for strings (unless double quotes avoid escaping)
- **Docstrings**: Google-style docstrings

### Code Formatting

Use **Black** for automatic formatting:

```bash
black .
```

### Linting

Use **Flake8** for linting:

```bash
flake8 . --max-line-length=100 --ignore=E203,W503
```

### Type Hints

Use type hints where appropriate:

```python
def scrub_image(self, input_path: str, output_path: str) -> Tuple[bool, dict]:
    """
    Scrub metadata from an image.

    Args:
        input_path: Path to input image
        output_path: Path to save cleaned image

    Returns:
        Tuple of (success, metadata_dict)
    """
    pass
```

### Security

Run **Bandit** for security checks:

```bash
bandit -r core/ cli/ gui/ web/ -ll
```

### Docstring Format

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief one-line description.

    More detailed description if needed.
    Can span multiple lines.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input
        IOError: When file operations fail

    Examples:
        >>> function_name("test", 42)
        True
    """
    pass
```

## Testing

### Test Structure

```
tests/
├── test_scrubber.py    # Scrubber module tests
├── test_crypto.py      # Cryptography tests
├── test_secure_delete.py   # Secure deletion tests
├── test_formats.py     # Format handling tests
└── fixtures/           # Test data
    └── sample_images/
```

### Writing Tests

```python
import pytest
from core.scrubber import ImageScrubber

class TestImageScrubber:
    @pytest.fixture
    def scrubber(self):
        return ImageScrubber(verbose=False)

    def test_scrub_jpeg(self, scrubber, tmp_path):
        """Test JPEG metadata removal"""
        input_file = "tests/fixtures/sample.jpg"
        output_file = tmp_path / "output.jpg"

        success, info = scrubber.scrub_image(str(input_file), str(output_file))

        assert success is True
        assert output_file.exists()
        assert info['bytes_removed'] > 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov-report=term-missing

# Run specific test
pytest tests/test_scrubber.py::TestImageScrubber::test_scrub_jpeg

# Run with verbose output
pytest -v
```

## Documentation

### Code Comments

- Write self-documenting code with clear variable names
- Add comments for complex logic
- Avoid obvious comments
- Use TODO/FIXME for future improvements

```python
# Good
metadata = self._extract_metadata(file_path)

# Bad
# Extract metadata from file
metadata = self._extract_metadata(file_path)  # Extract metadata
```

### README Updates

When adding features:
1. Update feature list in README.md
2. Add usage examples
3. Update supported formats if applicable
4. Add to changelog

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**

```bash
feat(scrubber): add support for WebP format
fix(crypto): handle empty password edge case
docs(readme): update installation instructions
test(crypto): add Argon2id parameter tests
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions

### Getting Help

- Read the [documentation](README.md)
- Search [existing issues](https://github.com/yourusername/imageghost/issues)
- Ask in [GitHub Discussions](https://github.com/yourusername/imageghost/discussions)

### Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project credits

## License

By contributing to ImageGhost, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to ImageGhost! 🎉**

Your efforts help make operational security tools better for the entire community.
