# AI Task Planning Agent - Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Initial Setup](#initial-setup)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [API Reference](#api-reference)
6. [Best Practices](#best-practices)

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_CALENDAR_CREDENTIALS=credentials.json
```

### 3. Google Calendar Setup (Optional but Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials
5. Download credentials and save as `credentials.json` in project root

## Initial Setup

Run the interactive setup wizard:

```bash
python main.py setup
```

This will configure:
- Working hours
- Productivity preferences
- Calendar integration
- Scheduling preferences

## Basic Usage

### Adding Tasks

#### Via CLI

```bash
# Simple task
python main.py add-task "Complete project report"

# With full options
python main.py add-task "Write documentation" \
  --desc "Update API docs with new endpoints" \
  --priority high \
  --duration 2.5 \
  --deadline 2025-12-20 \
  --deep-focus
```

#### Via Python API

```python
from agent import AITaskPlanningAgent

agent = AITaskPlanningAgent()

task = agent.add_task(
    title="Complete project report",
    description="Finish Q4 analysis",
    priority="high",
    estimated_duration=3.5,
    deadline=datetime(2025, 12, 20),
    requires_deep_focus=True
)
```

### Listing Tasks

```bash
# List all tasks
python main.py list-tasks

# Filter by status
python main.py list-tasks --status pending
python main.py list-tasks --status completed
```

### Generating a Plan

```bash
# Generate 2-week plan
python main.py plan

# Custom planning horizon
python main.py plan --days 30

# With additional context
python main.py plan --context "Prioritize urgent tasks this week"
```

The agent will:
1. Analyze your tasks, calendar, and preferences
2. Generate an optimal schedule
3. Display the plan for your review
4. Allow you to refine with feedback
5. Execute the plan (add to calendar)

### Interactive Planning Loop

When you generate a plan, you can iteratively refine it:

```
Would you like to refine this plan? [y/N]: y
What would you like to change?: Move deep work tasks to morning

[Agent generates refined plan]

Would you like to refine this plan? [y/N]: n
Execute this plan (add to calendar)? [Y/n]: y
```

### Tracking Progress

#### Start a Task

```bash
python main.py start task_1734123456
```

#### Complete a Task

```bash
python main.py complete task_1734123456
```

The agent will:
- Record actual duration
- Compare to estimated duration
- Learn from the deviation
- Update your productivity profile

### Real-Time Monitoring

Start monitoring mode to track schedule adherence:

```bash
python main.py monitor --interval 15
```

This will:
- Check every 15 minutes (configurable)
- Detect schedule deviations
- Alert on missed tasks
- Trigger automatic replanning if needed

Press `Ctrl+C` to stop monitoring.

### Dynamic Replanning

If your schedule gets disrupted:

```bash
python main.py replan --reason "Unexpected meetings added"
```

The agent will:
- Gather all incomplete tasks
- Consider new calendar state
- Generate a new optimal plan
- Allow you to review and execute

### Viewing Insights

See what the agent has learned about you:

```bash
python main.py insights
```

Shows:
- Peak productive hours
- Average focus duration
- Schedule adherence rate
- Personalized recommendations

## Advanced Features

### Interactive Mode

Launch an interactive session:

```bash
python main.py interactive
```

### Python API Usage

```python
from agent import AITaskPlanningAgent
from datetime import datetime, timedelta

# Initialize
agent = AITaskPlanningAgent(user_id="john_doe")

# Add multiple tasks
tasks = [
    agent.add_task("Task 1", priority="high", estimated_duration=2.0),
    agent.add_task("Task 2", priority="medium", estimated_duration=1.5),
]

# Generate plan
plan = agent.generate_plan(
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=7)
)

# Refine with feedback
refined_plan = agent.refine_plan(
    "Prefer afternoon slots for meetings",
    plan
)

# Execute
events = agent.execute_plan(refined_plan)

# Start monitoring
agent.start_monitoring(interval_minutes=10)

# ... later ...
agent.stop_monitoring()
```

### Customizing User Profile

```python
agent = AITaskPlanningAgent()
profile = agent.user_profile

# Update preferences
profile.prefer_morning_deep_work = True
profile.max_daily_work_hours = 6.0
profile.min_buffer_between_tasks = 0.5  # 30 minutes

# Update working hours
from datetime import time
profile.working_hours.start_time = time(8, 0)
profile.working_hours.end_time = time(16, 0)

# Save changes
agent.db.save_profile(profile)
```

### Learning from Feedback

The agent learns from:

1. **Task Completion Data**
   - Compares estimated vs actual duration
   - Identifies productive hours
   - Adjusts future estimates

2. **User Feedback**
   - Parses natural language feedback
   - Updates preferences automatically
   - Adapts planning strategy

3. **Schedule Adherence**
   - Tracks on-time completion rate
   - Identifies patterns in delays
   - Adjusts buffer times

Example feedback patterns:

```
"Move deep work to morning"          → Updates prefer_morning_deep_work
"Tasks are too long"                  → Reduces preferred_task_duration
"I need more time between tasks"     → Increases min_buffer_between_tasks
"Don't schedule on weekends"          → Sets allow_weekend_scheduling = False
```

## API Reference

### AITaskPlanningAgent

Main agent class.

**Methods:**

- `add_task(title, description, priority, estimated_duration, deadline, **kwargs)` - Add a task
- `generate_plan(start_date, end_date, context)` - Generate AI plan
- `refine_plan(feedback, current_plan)` - Refine plan with feedback
- `execute_plan(plan)` - Execute plan on calendar
- `mark_task_in_progress(task_id)` - Start a task
- `mark_task_completed(task_id)` - Complete a task
- `start_monitoring(interval_minutes)` - Start monitoring
- `stop_monitoring()` - Stop monitoring
- `trigger_replan(reason)` - Trigger replanning
- `get_insights()` - Get productivity insights
- `list_tasks(status)` - List tasks
- `get_calendar_events(start_date, end_date)` - Get calendar events

### Task Model

```python
Task(
    title: str,                          # Task title
    description: str,                    # Description
    priority: Priority,                  # low, medium, high, urgent
    estimated_duration: float,           # Hours
    deadline: datetime,                  # Optional deadline
    preferred_time_of_day: str,         # morning, afternoon, evening
    requires_deep_focus: bool,          # Requires uninterrupted time
    can_split: bool,                    # Can be split into sessions
    min_session_duration: float,        # Minimum session length if split
    tags: List[str],                    # Tags/categories
    dependencies: List[str]              # Task ID dependencies
)
```

## Best Practices

### 1. Accurate Time Estimates

- Start with conservative estimates
- The agent will learn and adjust over time
- Review actual vs estimated in insights

### 2. Set Realistic Deadlines

- Include buffer for unexpected issues
- The agent will warn about tight deadlines
- Consider dependencies

### 3. Use Priority Levels Wisely

- **Urgent**: Must be done today
- **High**: Important and time-sensitive
- **Medium**: Regular tasks
- **Low**: Can be delayed if needed

### 4. Provide Feedback

- Refine plans when they don't match your preference
- The agent learns from your feedback
- Be specific: "Move meeting prep to afternoon" vs "This doesn't work"

### 5. Regular Monitoring

- Run monitoring during work hours
- Let the agent detect and adapt to changes
- Review insights weekly

### 6. Mark Tasks Promptly

- Mark tasks as started when you begin
- Complete them when done
- Provides accurate learning data

### 7. Use Deep Focus Flag

- Tag tasks requiring uninterrupted focus
- Agent will schedule in optimal time slots
- Considers your learned productive hours

### 8. Split Long Tasks

- Enable `can_split` for tasks over 2-3 hours
- Prevents fatigue and maintains quality
- Agent respects `min_session_duration`

### 9. Review Insights Regularly

```bash
python main.py insights
```

- Check adherence rate
- Identify productivity patterns
- Follow recommendations

### 10. Replan When Needed

Don't stick to an outdated plan:

```bash
python main.py replan
```

The agent adapts quickly to changes.

## Troubleshooting

### Calendar Sync Issues

If calendar sync fails:

1. Check `credentials.json` is in project root
2. Delete `token.json` and re-authenticate
3. Verify Google Calendar API is enabled
4. Check internet connection

### Agent Not Learning

Ensure:

- `learning_mode=enabled` in `.env`
- You're marking tasks as complete
- Providing feedback on plans
- Using the same user_id

### Performance Issues

- Reduce monitoring interval
- Limit planning horizon (use --days 7 instead of 30)
- Check database size (SQLite performance)

## Example Workflows

### Daily Workflow

```bash
# Morning: Review plan
python main.py list-tasks --status scheduled

# During day: Track progress
python main.py start <task_id>
# ... work on task ...
python main.py complete <task_id>

# End of day: Check insights
python main.py insights
```

### Weekly Workflow

```bash
# Sunday evening: Add next week's tasks
python main.py add-task "Task 1" ...
python main.py add-task "Task 2" ...

# Generate weekly plan
python main.py plan --days 7

# Start monitoring
python main.py monitor &

# Friday: Review week
python main.py insights
```

### Recovery from Disruption

```bash
# When your day gets disrupted
python main.py replan --reason "Emergency meeting"

# Review new plan
python main.py list-tasks --status scheduled

# Execute if satisfied
```

## Support

For issues or questions:
- Check the README.md
- Review example_usage.py
- Check GitHub issues
- Consult the code documentation

Happy planning! 🤖
