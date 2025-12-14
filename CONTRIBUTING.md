# Contributing to AI Task Planning Agent

Thank you for considering contributing to this project!

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature has already been requested
- Clearly describe the feature and its use case
- Explain how it would benefit users

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation
4. **Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **Push to your branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AI_Agent.git
cd AI_Agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API keys to .env

# Run tests (if available)
python -m pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write clear, descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

## Areas for Contribution

We'd especially welcome contributions in:

- **Additional calendar providers** (Apple Calendar, CalDAV, etc.)
- **Web UI** (React/Vue frontend)
- **Testing** (unit tests, integration tests)
- **Mobile app** (React Native, Flutter)
- **Integrations** (Jira, Asana, Trello, Notion)
- **Advanced analytics** (visualization, reporting)
- **Performance optimizations**
- **Documentation improvements**
- **Bug fixes**

## Questions?

Feel free to open an issue for questions or join the discussions!

---

Thank you for helping make this project better! 🙏
