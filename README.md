# AI Task Planning Agent

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange)](https://www.anthropic.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent AI-powered personal task planning and scheduling assistant that learns your habits and preferences over time.

## Overview

This agent helps you manage your tasks by:
- **Planning**: Generates optimal schedules using AI (Claude)
- **Learning**: Adapts to your working patterns and preferences
- **Monitoring**: Tracks your progress in real-time
- **Replanning**: Dynamically adjusts when life happens

## Key Features

### 🤖 AI-Powered Planning
- Analyzes tasks, deadlines, priorities, and calendar
- Generates optimal schedules based on your preferences
- Proposes plans for your review and iterative refinement
- Learns from every interaction

### 📅 Calendar Integration
- Syncs with Google Calendar and Outlook
- Reads existing meetings and events
- Schedules tasks in available time slots
- Maintains real-time synchronization

### 🧠 Adaptive Learning
- Tracks actual vs estimated task duration
- Learns your productive hours
- Identifies working patterns
- Adjusts recommendations over time

### 🔄 Dynamic Replanning
- Monitors schedule adherence
- Detects deviations automatically
- Triggers replanning when needed
- Adapts to changes in real-time

### 📊 Insights & Analytics
- Productivity patterns
- Schedule adherence metrics
- Personalized recommendations
- Continuous improvement tracking

## Quick Start

**Get started in 5 minutes!** See [QUICKSTART.md](QUICKSTART.md)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure (add your Anthropic API key)
cp .env.example .env

# 3. Setup
python main.py setup

# 4. Add tasks
python main.py add-task "Your task" --priority high --duration 2

# 5. Generate plan
python main.py plan
```

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- **[Usage Guide](USAGE_GUIDE.md)** - Comprehensive documentation
- **[Example Usage](example_usage.py)** - Code examples

## Installation

### Prerequisites
- Python 3.9+
- Anthropic API key ([Get one here](https://console.anthropic.com/))
- Google Calendar API credentials (optional, for calendar sync)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Edit `.env`:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_CALENDAR_CREDENTIALS=credentials.json
```

3. (Optional) Set up Google Calendar:
   - Follow [Google Calendar API setup](https://developers.google.com/calendar/api/quickstart/python)
   - Download credentials.json to project root

## Project Structure

```
ai_agent/
├── main.py                 # Entry point
├── models/                 # Data models
│   ├── task.py
│   ├── calendar_event.py
│   └── user_profile.py
├── services/
│   ├── calendar_service.py
│   ├── ai_planner.py
│   └── preference_learner.py
├── database/
│   └── db_manager.py
├── config/
│   └── settings.py
└── utils/
    └── helpers.py
```

## Usage

### Command Line Interface

```bash
# Add a task
python main.py add-task "Complete project report" \
  --priority high \
  --duration 3.5 \
  --deadline 2025-12-20 \
  --deep-focus

# List tasks
python main.py list-tasks

# Generate AI plan
python main.py plan --days 14

# Mark task complete
python main.py complete <task_id>

# Monitor schedule
python main.py monitor

# View insights
python main.py insights

# Interactive mode
python main.py interactive
```

### Python API

```python
from agent import AITaskPlanningAgent
from datetime import datetime, timedelta

# Initialize agent
agent = AITaskPlanningAgent()

# Add tasks
agent.add_task(
    title="Complete project report",
    description="Finish Q4 analysis",
    priority="high",
    estimated_duration=3.5,
    deadline=datetime(2025, 12, 20),
    requires_deep_focus=True
)

# Generate plan
plan = agent.generate_plan(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14)
)

# Refine with feedback
refined_plan = agent.refine_plan(
    "Move deep work tasks to morning",
    plan
)

# Execute plan
agent.execute_plan(refined_plan)

# Monitor progress
agent.start_monitoring(interval_minutes=15)

# Complete tasks
agent.mark_task_completed(task_id)

# Get insights
insights = agent.get_insights()
```

## How It Works

### 1. You Define Tasks
Provide tasks with descriptions, priorities, deadlines, and time estimates.

### 2. Agent Reads Your Calendar
Fetches existing meetings and events from Google Calendar or Outlook.

### 3. AI Generates Optimal Plan
Claude analyzes everything and creates a realistic, optimized schedule considering:
- Task priorities and deadlines
- Your calendar availability
- Working hours and preferences
- Learned productivity patterns
- Task dependencies

### 4. Interactive Refinement
Review the plan and provide feedback. The agent refines it based on your input and learns your preferences.

### 5. Plan Execution
Tasks are scheduled on your calendar with proper time blocks.

### 6. Real-Time Monitoring
The agent tracks your progress, comparing actual vs planned completion times.

### 7. Adaptive Learning
- Learns your productive hours
- Adjusts time estimates
- Improves future plans
- Adapts to your working style

### 8. Dynamic Replanning
When you deviate from schedule (we all do!), the agent automatically replans remaining tasks.

## Architecture

### Components

```
┌─────────────────────────────────────────────────────┐
│                    User Interface                   │
│            (CLI / Interactive / Python API)         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              AI Planning Agent                      │
│  ┌──────────────────────────────────────────────┐  │
│  │         AI Planner (Claude)                  │  │
│  │  • Generate plans                            │  │
│  │  • Refine with feedback                      │  │
│  │  • Analyze deviations                        │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │       Preference Learner                     │  │
│  │  • Learn from completions                    │  │
│  │  • Track patterns                            │  │
│  │  • Update profile                            │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │       Calendar Service                       │  │
│  │  • Google Calendar                           │  │
│  │  • Outlook Calendar                          │  │
│  │  • Event management                          │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              Database (SQLite)                      │
│  • Tasks  • Events  • User Profile  • History      │
└─────────────────────────────────────────────────────┘
```

### Tech Stack

- **AI**: Claude 4 Sonnet (Anthropic API)
- **Language**: Python 3.9+
- **Calendar APIs**: Google Calendar API, Microsoft Graph API
- **Database**: SQLite (easy upgrade to PostgreSQL)
- **CLI**: Typer + Rich
- **Data Models**: Pydantic

## Advanced Features

### Task Dependencies
```python
task1 = agent.add_task("Design API", ...)
task2 = agent.add_task("Implement API", dependencies=[task1.id])
```

### Split Tasks
```python
agent.add_task(
    "Long project",
    estimated_duration=6.0,
    can_split=True,
    min_session_duration=2.0
)
# Agent will split into 2-3 hour sessions
```

### Custom Preferences
```python
profile = agent.user_profile
profile.prefer_morning_deep_work = True
profile.max_daily_work_hours = 6.0
profile.productivity_pattern.peak_hours = [9, 10, 11, 14]
agent.db.save_profile(profile)
```

### Monitoring Hooks
```python
agent.start_monitoring(interval_minutes=10)
# Automatically detects and adapts to schedule changes
```

## Examples

### Daily Workflow
```bash
# Morning
python main.py list-tasks --status scheduled

# During work
python main.py start <task_id>
# ... do work ...
python main.py complete <task_id>

# Evening
python main.py insights
```

### Weekly Planning
```bash
# Add week's tasks
python main.py add-task "Task 1" ...
python main.py add-task "Task 2" ...

# Generate plan
python main.py plan --days 7

# Start monitoring
python main.py monitor &
```

See [example_usage.py](example_usage.py) for complete examples.

## Learning & Adaptation

The agent learns from:

**Task Completion**
- Actual vs estimated duration
- Time of day completed
- Task type patterns

**User Feedback**
- Plan refinement requests
- Preference changes
- Schedule adjustments

**Schedule Adherence**
- On-time completion rate
- Typical delays
- Productivity patterns

**Metrics Tracked**
- Peak productive hours
- Average focus duration
- Adherence rate
- Task estimation accuracy

## Roadmap

- [ ] Web UI interface
- [ ] Mobile notifications
- [ ] Team collaboration features
- [ ] Integration with project management tools (Jira, Asana)
- [ ] Voice interface
- [ ] Slack/Discord bot
- [ ] Advanced analytics dashboard
- [ ] Multi-user support

## Contributing

Contributions welcome! Areas for improvement:

- Additional calendar providers (Apple Calendar, etc.)
- UI enhancements
- Additional learning algorithms
- Performance optimizations
- Documentation improvements

## License

MIT License - see LICENSE file for details

## Support

- **Documentation**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Examples**: [example_usage.py](example_usage.py)
- **Issues**: GitHub Issues

## Acknowledgments

This project was built with:
- **AI Planning**: Powered by [Anthropic Claude](https://www.anthropic.com/) for intelligent task scheduling
- **Calendar Integration**: Google Calendar API and Microsoft Graph API
- **Development**: Python with modern libraries (Pydantic, SQLAlchemy, Typer, Rich)

### Built with Claude Code

This entire project was developed with the assistance of [Claude Code](https://claude.ai/claude-code), Anthropic's AI-powered coding assistant. Claude Code helped with:
- Architecture design and implementation
- Writing clean, well-documented code
- Creating comprehensive documentation
- Implementing best practices and patterns
- Building a production-ready system from concept to completion

Special thanks to the Anthropic team for creating such powerful AI tools that enable rapid development of sophisticated applications.

---

## Project Stats

- **~3,000 lines** of Python code
- **17 modules** with clean separation of concerns
- **5 comprehensive guides** and documentation files
- **Production-ready** with error handling and validation
- **Extensible architecture** for easy feature additions

---

**Start planning smarter today!** 🚀

```bash
python main.py setup
```

## Star History

If you find this project helpful, please consider giving it a ⭐ on GitHub!

---

**Made with ❤️ and AI**
