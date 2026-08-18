# Contributing to Application Bot

Thank you for your interest in contributing to Application Bot! 🎉

## 📋 Table of Contents

- [How to Contribute](#how-to-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Reporting Issues](#reporting-issues)
- [Code of Conduct](#code-of-conduct)

## 🤝 How to Contribute

We welcome contributions in many forms:

- **Bug Reports**: Report bugs you encounter
- **Feature Requests**: Suggest new features
- **Code Contributions**: Submit pull requests with fixes or improvements
- **Documentation**: Improve documentation
- **Translations**: Add or improve translations
- **Code Review**: Review pull requests from other contributors

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Docker (optional, for containerized development)
- Telegram account (for testing the bot)

### Fork the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/application-bot.git
   cd application-bot
   ```

3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/original-owner/application-bot.git
   ```

## 🛠️ Development Setup

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your configuration:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=your_telegram_user_id
   DB_TYPE=sqlite  # or postgresql
   ```

5. Run the bot:
   ```bash
   python -m bot.main
   ```

### Docker Development

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. View logs:
   ```bash
   docker-compose logs -f bot
   ```

## 🎨 Code Style

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) guidelines
- Use 4 spaces for indentation
- Maximum line length: 120 characters
- Use descriptive variable and function names
- Include docstrings for public functions and classes

### Formatting

Use the following tools for code formatting:

```bash
# Format code with black
black bot/ tests/

# Check formatting with flake8
flake8 bot/ tests/ --max-line-length=120 --extend-ignore=E203

# Sort imports with isort
isort bot/ tests/
```

### Naming Conventions

- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=bot --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_translations.py -v

# Run specific test
python -m pytest tests/test_validators.py::TestEmailValidator -v
```

### Writing Tests

- Add new tests in the appropriate test file
- Follow the existing test patterns
- Use descriptive test names
- Test both happy paths and edge cases
- Mock external dependencies

### Test Requirements

- All new functionality must have corresponding tests
- All existing tests must pass before merging
- Tests should run quickly and independently

## 📝 Pull Request Guidelines

### Before Submitting

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the code style guidelines
3. **Add tests** for new functionality
4. **Run all tests** to ensure nothing is broken
5. **Update documentation** if applicable

### Pull Request Template

Use the provided pull request template and include:

- Clear description of changes
- Related issues (use `Fixes #123` or `Closes #456`)
- Type of change (bug fix, feature, documentation, etc.)
- Testing information
- Screenshots (if applicable)

### Commit Messages

- Use clear, descriptive commit messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/) format
- Include the issue number if applicable

Examples:
```
feat: add user registration validation
fix: resolve email validation bug
docs: update README with setup instructions
chore: update dependencies
```

## 🐛 Reporting Issues

### Bug Reports

When reporting a bug, please include:

- Clear description of the issue
- Steps to reproduce
- Expected vs. actual behavior
- Environment information (Python version, OS, etc.)
- Screenshots (if applicable)

### Feature Requests

When requesting a feature, please include:

- Clear description of the feature
- Use case or problem it solves
- Any alternatives you've considered
- Priority level

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We expect all contributors to:

- Be respectful and inclusive
- Focus on constructive feedback
- Follow the project's guidelines
- Maintain a positive and collaborative environment

## 📚 Additional Resources

- [GitHub Issues](https://github.com/your-repo/application-bot/issues)
- [GitHub Discussions](https://github.com/your-repo/application-bot/discussions)
- [Documentation](README.md)

## 🙏 Thank You!

Your contributions help make Application Bot better for everyone. Thank you for your time and effort!

---

*Last updated: August 2026*
