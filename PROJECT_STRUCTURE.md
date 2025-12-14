# Project Structure

Complete file tree and organization of the AI Task Planning Agent.

```
AI-Task-Planning-Agent/
│
├── 📄 Core Application Files
│   ├── main.py                      # CLI entry point with all commands
│   ├── agent.py                     # Main agent orchestrator (400+ lines)
│   ├── example_usage.py             # Working examples demonstrating features
│   └── setup.py                     # Python package setup configuration
│
├── 📚 Documentation (9 files)
│   ├── README.md                    # Main documentation with badges
│   ├── QUICKSTART.md               # 5-minute getting started guide
│   ├── USAGE_GUIDE.md              # Comprehensive user manual
│   ├── PROJECT_SUMMARY.md          # Technical overview & capabilities
│   ├── WORKFLOW.md                 # Visual diagrams & data flows
│   ├── PROJECT_STRUCTURE.md        # This file - project organization
│   ├── GITHUB_SETUP.md             # Guide to push to GitHub
│   ├── CHANGELOG.md                # Version history and changes
│   └── CONTRIBUTING.md             # Contribution guidelines
│
├── 📋 Data Models (models/)
│   ├── __init__.py                 # Package initialization & exports
│   ├── task.py                     # Task model (priorities, deadlines, deps)
│   ├── calendar_event.py           # Calendar event model
│   └── user_profile.py             # User preferences & learned patterns
│
├── ⚙️ Services (services/)
│   ├── __init__.py                 # Package initialization & exports
│   ├── ai_planner.py               # Claude-powered planning engine
│   ├── calendar_service.py         # Google/Outlook calendar integration
│   └── preference_learner.py       # Adaptive learning system
│
├── 💾 Database (database/)
│   ├── __init__.py                 # Package initialization & exports
│   └── db_manager.py               # SQLAlchemy ORM with CRUD operations
│
├── 🔧 Configuration (config/)
│   ├── __init__.py                 # Package initialization & exports
│   └── settings.py                 # Pydantic settings from environment
│
├── 🛠️ Utilities (utils/)
│   ├── __init__.py                 # Package initialization & exports
│   └── helpers.py                  # Time/date utilities, scheduling helpers
│
├── 🐙 GitHub Configuration (.github/)
│   ├── workflows/
│   │   └── python-app.yml          # CI/CD workflow for testing
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md           # Bug report template
│   │   └── feature_request.md      # Feature request template
│   └── PULL_REQUEST_TEMPLATE.md    # PR template
│
├── 📦 Package & Installation
│   ├── requirements.txt            # Python dependencies
│   ├── setup.py                    # Package setup configuration
│   ├── MANIFEST.in                 # Package manifest
│   ├── install.sh                  # Linux/Mac installation script
│   └── install.bat                 # Windows installation script
│
├── 🔒 Security & License
│   ├── LICENSE                     # MIT License
│   ├── SECURITY.md                 # Security policy
│   └── CODE_OF_CONDUCT.md          # Community guidelines
│
└── ⚙️ Configuration Files
    ├── .env.example                # Environment template (API keys)
    ├── .gitignore                  # Git ignore rules
    └── .gitattributes              # Git attributes for text handling
```

## File Count Summary

- **Python Files**: 17 modules (~3,000 lines of code)
- **Documentation**: 9 comprehensive guides
- **Configuration**: 10+ config files
- **GitHub Templates**: 4 templates
- **Total Files**: 40+ files

## Module Dependencies

```
main.py
  └── agent.py
        ├── models/
        │     ├── task.py
        │     ├── calendar_event.py
        │     └── user_profile.py
        ├── services/
        │     ├── ai_planner.py
        │     ├── calendar_service.py
        │     └── preference_learner.py
        ├── database/
        │     └── db_manager.py
        ├── config/
        │     └── settings.py
        └── utils/
              └── helpers.py
```

## Key Files Explained

### Core Application

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | CLI interface with Typer, all user commands | ~450 |
| `agent.py` | Main orchestrator, coordinates all components | ~400 |
| `example_usage.py` | Demonstrates all features with working code | ~150 |

### Models

| File | Purpose | Lines |
|------|---------|-------|
| `task.py` | Task data model with validation | ~100 |
| `calendar_event.py` | Calendar event model | ~80 |
| `user_profile.py` | User preferences & learning data | ~120 |

### Services

| File | Purpose | Lines |
|------|---------|-------|
| `ai_planner.py` | Claude API integration for planning | ~400 |
| `calendar_service.py` | Google/Outlook calendar sync | ~350 |
| `preference_learner.py` | Learning and adaptation logic | ~300 |

### Infrastructure

| File | Purpose | Lines |
|------|---------|-------|
| `db_manager.py` | Database operations with SQLAlchemy | ~400 |
| `settings.py` | Configuration management | ~50 |
| `helpers.py` | Utility functions | ~250 |

## Documentation Files

| File | Purpose | Size |
|------|---------|------|
| `README.md` | Main project documentation | 13 KB |
| `QUICKSTART.md` | 5-minute setup guide | 5.5 KB |
| `USAGE_GUIDE.md` | Comprehensive manual | 10.4 KB |
| `PROJECT_SUMMARY.md` | Technical deep dive | 13.2 KB |
| `WORKFLOW.md` | Visual diagrams | 33 KB |
| `GITHUB_SETUP.md` | GitHub deployment guide | 5 KB |
| `CHANGELOG.md` | Version history | 2.4 KB |
| `CONTRIBUTING.md` | Contribution guidelines | 2.2 KB |
| `SECURITY.md` | Security policy | 1.9 KB |

## Generated Files (Not in Git)

These files are created during runtime or setup:

```
AI-Task-Planning-Agent/
├── .env                       # Your API keys (gitignored)
├── credentials.json           # Google OAuth credentials (gitignored)
├── token.json                # Google OAuth token (gitignored)
├── ai_agent.db               # SQLite database (gitignored)
├── venv/                     # Virtual environment (gitignored)
└── __pycache__/              # Python cache (gitignored)
```

## Import Paths

When using the agent programmatically:

```python
# Main agent
from agent import AITaskPlanningAgent

# Models
from models import Task, CalendarEvent, UserProfile
from models import Priority, TaskStatus, EventType

# Services
from services import AIPlannerService, CalendarService, PreferenceLearner

# Database
from database import DatabaseManager

# Config
from config import settings

# Utils
from utils import parse_date_string, format_duration
```

## Development Workflow

```
1. Edit code in respective modules
2. Test with: python example_usage.py
3. Run CLI: python main.py [command]
4. Commit changes: git add . && git commit -m "..."
5. Push to GitHub: git push
```

## Adding New Features

### New Service
1. Create `services/new_service.py`
2. Add to `services/__init__.py`
3. Import in `agent.py`
4. Update documentation

### New Model
1. Create `models/new_model.py` with Pydantic
2. Add to `models/__init__.py`
3. Add database table in `db_manager.py`
4. Update migrations (if using Alembic)

### New CLI Command
1. Add command function in `main.py` with `@app.command()`
2. Use existing agent methods or create new ones
3. Update `--help` documentation

## Testing Structure (Future)

```
tests/
├── __init__.py
├── test_models.py
├── test_services.py
├── test_database.py
├── test_agent.py
├── test_cli.py
└── fixtures/
```

## Deployment Structure (Future)

```
docker/
├── Dockerfile
├── docker-compose.yml
└── .dockerignore

kubernetes/
├── deployment.yaml
├── service.yaml
└── configmap.yaml
```

## Project Metrics

- **Total Lines of Code**: ~3,000
- **Documentation**: ~100 KB
- **Test Coverage**: TBD (future)
- **Dependencies**: 15 packages
- **Python Version**: 3.9+
- **Platforms**: Windows, macOS, Linux

## Code Organization Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Type Safety**: Pydantic models for validation
3. **DRY**: Reusable utilities in `utils/`
4. **Modularity**: Independent services can be tested separately
5. **Documentation**: Every file has docstrings and comments

## Architecture Layers

```
┌─────────────────────────────┐
│   Presentation Layer        │  main.py, CLI
├─────────────────────────────┤
│   Application Layer         │  agent.py
├─────────────────────────────┤
│   Business Logic Layer      │  services/
├─────────────────────────────┤
│   Data Access Layer         │  database/
├─────────────────────────────┤
│   Data Model Layer          │  models/
└─────────────────────────────┘
```

---

**Well-organized, maintainable, and ready for collaboration!** 🚀
