# AI Task Planning Agent

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Multi-Provider AI](https://img.shields.io/badge/AI-Claude%20%7C%20ChatGPT%20%7C%20Gemini-orange)](https://www.anthropic.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)](https://streamlit.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An intelligent AI-powered personal task planning and scheduling assistant that learns your habits and preferences through natural conversation. Works with Claude, ChatGPT, or Gemini - no calendar API integration required!

## Overview

This agent helps you manage your tasks through **natural conversation**:
- **💬 Conversational Interface**: Share your schedule and tasks through simple text
- **🤖 AI Planning**: Generates optimal schedules using Claude, ChatGPT, or Gemini
- **🧠 Adaptive Learning**: Learns from your weekly feedback to improve future plans
- **📊 Visual Interface**: Beautiful Streamlit UI for easy interaction
- **🔒 Privacy-First**: No calendar API access needed - you control what you share

## ✨ Key Features

### 🎨 Streamlit Web Interface
- **Easy Setup**: Paste your API key and start planning in seconds
- **Multiple Pages**: Chat, Tasks, Schedule, Planning, Insights
- **Visual Dashboard**: See your schedule and plans clearly
- **Provider Selection**: Switch between Claude, ChatGPT, and Gemini anytime
- **Responsive Design**: Works on desktop and mobile

### 🤖 Multi-Provider AI Support
- **Anthropic Claude**: Best reasoning and detailed planning
  - Claude Sonnet 4.5, Opus 4.5, Claude 3.5 Sonnet
- **OpenAI ChatGPT**: Fast responses and great performance
  - GPT-4o, GPT-4o-mini, GPT-4 Turbo, GPT-3.5 Turbo
- **Google Gemini**: Free tier available, multimodal capabilities
  - Gemini 2.0 Flash, Gemini 1.5 Pro, Gemini 1.5 Flash

### 🗓️ Conversational Calendar
- **No API Integration**: Share schedule through natural language text
- **Full Privacy**: Your actual calendar stays private
- **Weekly Updates**: Tell the agent about your week in plain text
- **Visual Plans**: See your commitments and scheduled tasks clearly
- **Learning Loop**: Report what actually happened for continuous improvement

### 🧠 Adaptive Learning
- **Weekly Reviews**: Compare planned vs actual completion
- **Pattern Recognition**: Learns your productive hours and work patterns
- **Improved Estimates**: Adjusts time predictions based on your feedback
- **Personalized Plans**: Gets better at planning for you over time

### 📊 Insights & Analytics
- **Productivity Patterns**: Understand when you work best
- **Task Analysis**: Track completion rates and time estimates
- **Personalized Recommendations**: Get AI-powered suggestions
- **Progress Tracking**: Monitor your improvement week by week

## 🚀 Quick Start

### Option 1: Streamlit Web UI (Recommended)

```bash
# 1. Clone and install
git clone <repository-url>
cd AI_Agent
pip install -r requirements.txt

# 2. Run Streamlit app
python -m streamlit run streamlit_app.py

# 3. Configure in browser
# - Select AI provider (Claude/ChatGPT/Gemini)
# - Paste your API key
# - Choose model
# - Start planning!
```

**Get your API key:**
- Anthropic Claude: [console.anthropic.com](https://console.anthropic.com/)
- OpenAI ChatGPT: [platform.openai.com](https://platform.openai.com/)
- Google Gemini: [ai.google.dev](https://ai.google.dev/) *(Free tier available!)*

### Option 2: Command Line Interface

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API key

# 3. Run
python main.py setup
python main.py add-task "Your task" --priority high --duration 2
python main.py plan
```

## 📚 Documentation

- **[Streamlit UI Guide](STREAMLIT_README.md)** - Web interface documentation
- **[Multi-Provider Setup](MULTI_PROVIDER_README.md)** - Claude, ChatGPT, Gemini configuration
- **[Conversational Calendar](CONVERSATIONAL_CALENDAR_README.md)** - Text-based schedule sharing
- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- **[Usage Guide](USAGE_GUIDE.md)** - Comprehensive CLI documentation
- **[Example Usage](example_usage.py)** - Code examples

## 💻 Installation

### Prerequisites
- **Python 3.9+** (Python 3.13 recommended)
- **AI Provider API Key** (choose one):
  - Anthropic Claude ([Get key](https://console.anthropic.com/))
  - OpenAI ChatGPT ([Get key](https://platform.openai.com/))
  - Google Gemini ([Get key](https://ai.google.dev/)) - Free tier available!

### Install Dependencies

```bash
# Using Python 3.13 (or your preferred version)
py -3.13 -m pip install -r requirements.txt

# Or standard pip
pip install -r requirements.txt
```

### Configuration Methods

#### Method 1: Streamlit UI (Easiest)
Just run the app and configure through the web interface:
```bash
python -m streamlit run streamlit_app.py
```

#### Method 2: Environment File
1. Create `.env` file:
```bash
cp .env.example .env
```

2. Edit `.env`:
```env
# Choose your provider
AI_PROVIDER=anthropic  # Options: anthropic, openai, google

# Add your API key
ANTHROPIC_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here
# OR
GOOGLE_API_KEY=your_key_here

# Choose model
MODEL_NAME=claude-sonnet-4-5-20250929
```

## 📁 Project Structure

```
AI_Agent/
├── streamlit_app.py                    # Streamlit web UI (main interface)
├── main.py                             # CLI entry point
├── agent.py                            # Core agent logic
├── models/                             # Data models
│   ├── task.py                         # Task model
│   ├── calendar_event.py               # Calendar event model
│   └── user_profile.py                 # User profile & preferences
├── services/
│   ├── ai_planner_multi.py            # Multi-provider AI service (NEW!)
│   ├── text_calendar_service.py       # Conversational calendar (NEW!)
│   ├── calendar_service.py            # External calendar integration
│   └── preference_learner.py          # Learning engine
├── database/
│   └── db_manager.py                   # SQLite database management
├── config/
│   └── settings.py                     # Configuration & settings
└── docs/
    ├── STREAMLIT_README.md             # Streamlit UI guide
    ├── MULTI_PROVIDER_README.md        # Multi-provider setup
    └── CONVERSATIONAL_CALENDAR_README.md  # Calendar guide
```

## 🎯 Usage

### Streamlit Web Interface (Recommended)

```bash
# Start the app
python -m streamlit run streamlit_app.py

# Open browser to http://localhost:8501
```

**Using the Interface:**

1. **💬 Chat Page** - Talk with your AI assistant
   - Discuss tasks and priorities
   - Ask for scheduling advice
   - Get personalized recommendations

2. **📝 Tasks Page** - Manage your tasks
   - Add tasks with priorities and deadlines
   - Track task status
   - Mark tasks complete or in-progress

3. **🗓️ Schedule Page** - Share your weekly schedule
   - Describe your week in natural language
   - View visual schedule summary
   - Record weekly reviews for learning

4. **📅 Planning Page** - Generate AI plans
   - Create optimal schedules
   - Refine plans with feedback
   - Execute and track plans

5. **📊 Insights Page** - View analytics
   - Productivity patterns
   - Task completion rates
   - Personalized recommendations

### Command Line Interface

```bash
# Add a task
python main.py add-task "Complete project report" \
  --priority high \
  --duration 3.5 \
  --deadline 2025-12-20

# List tasks
python main.py list-tasks

# Generate AI plan
python main.py plan --days 14

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

## 🔄 How It Works

### Conversational Workflow

#### 1. **Share Your Weekly Schedule** 🗓️
Tell the agent about your week in natural language:
```
Monday: Team meeting 9-10am, lunch 12-1pm, gym 6-7pm
Tuesday: Free morning, workshop 2-5pm
Wednesday: All-day conference
Thursday: Meetings 9-11am, rest of day flexible
Friday: Sprint planning 10-11am, afternoon for deep work
```

#### 2. **Add Your Tasks** 📝
Define what you need to accomplish:
- Task descriptions
- Priorities (high, medium, low)
- Estimated durations
- Deadlines
- Special requirements

#### 3. **Get AI-Generated Plans** 🤖
The AI analyzes everything and creates an optimal schedule considering:
- Your availability from shared schedule
- Task priorities and deadlines
- Learned productivity patterns
- Deep focus requirements
- Work-life balance

#### 4. **Refine and Execute** ✅
- Review the AI's proposed plan
- Provide feedback for refinement
- Execute the plan that works for you

#### 5. **Weekly Review** 📊
At week's end, share what actually happened:
```
Monday: Meeting went well, but gym was skipped
Tuesday: Workshop ended early at 4pm, used extra time for project work
Wednesday: Conference was valuable, made great connections
...
```

#### 6. **Continuous Learning** 🧠
The AI learns from your feedback:
- Adjusts time estimates based on actual completion
- Identifies your productive hours
- Understands your work patterns
- Improves future planning recommendations

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│              User Interfaces                        │
│  • Streamlit Web UI (Primary)                      │
│  • Command Line Interface                          │
│  • Python API                                      │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              AI Planning Agent                      │
│  ┌──────────────────────────────────────────────┐  │
│  │    Multi-Provider AI Planner                 │  │
│  │  • Anthropic Claude (Sonnet/Opus)           │  │
│  │  • OpenAI ChatGPT (GPT-4o/mini)             │  │
│  │  • Google Gemini (Flash/Pro)                │  │
│  │  • Generate & refine plans                   │  │
│  │  • Natural language chat                     │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │    Text Calendar Service (NEW!)              │  │
│  │  • Conversational schedule sharing          │  │
│  │  • No external API integration              │  │
│  │  • Weekly review & learning                 │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │       Preference Learner                     │  │
│  │  • Learn from weekly reviews                │  │
│  │  • Track productivity patterns              │  │
│  │  • Update user profile                      │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              Database (SQLite)                      │
│  • Tasks  • Events  • User Profile  • History      │
│  • All data stored locally - full privacy          │
└─────────────────────────────────────────────────────┘
```

### Tech Stack

- **AI Providers**:
  - Anthropic Claude (claude-sonnet-4-5, claude-opus-4-5)
  - OpenAI ChatGPT (gpt-4o, gpt-4o-mini)
  - Google Gemini (gemini-2.0-flash-exp, gemini-1.5-pro)
- **Web UI**: Streamlit 1.40+
- **Language**: Python 3.9+ (3.13 recommended)
- **Database**: SQLite (portable, no setup required)
- **CLI**: Typer + Rich (for command-line interface)
- **Data Models**: Pydantic (type-safe data validation)
- **AI SDKs**: anthropic, openai, google-generativeai

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

## 🎯 What's New in v2.0

### ✅ Recently Added
- **Streamlit Web UI** - Beautiful, responsive interface
- **Multi-Provider AI** - Support for Claude, ChatGPT, and Gemini
- **Conversational Calendar** - Share schedule through text (no API integration)
- **Weekly Review System** - Report actual completion for learning
- **Provider Switching** - Change AI provider anytime
- **Visual Dashboard** - Clear visualization of schedule and plans

### 🚀 Roadmap

- [ ] Enhanced AI schedule parsing (better natural language understanding)
- [ ] Calendar export (.ics files)
- [ ] Mobile-optimized interface
- [ ] Team collaboration features
- [ ] Integration with project management tools (Jira, Asana, Trello)
- [ ] Voice interface
- [ ] Slack/Discord bot
- [ ] Advanced analytics dashboard
- [ ] Pattern recognition for recurring events
- [ ] Smart notifications

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
