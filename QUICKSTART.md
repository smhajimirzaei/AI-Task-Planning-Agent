# Quick Start Guide

Get up and running with the AI Task Planning Agent in 5 minutes!

## 1. Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

## 2. Configure API Key (1 min)

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Anthropic API key
# Get your key from: https://console.anthropic.com/
```

**.env file:**
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

## 3. Run Setup (1 min)

```bash
python main.py setup
```

Answer a few questions about your working hours and preferences.

## 4. Add Your First Tasks (1 min)

```bash
python main.py add-task "Write project proposal" --priority high --duration 2.5 --deadline 2025-12-20

python main.py add-task "Code review" --priority medium --duration 1.5

python main.py add-task "Update documentation" --priority low --duration 1.0
```

## 5. Generate Your First Plan (1 min)

```bash
python main.py plan
```

The AI will:
- ✓ Analyze your tasks
- ✓ Check your calendar
- ✓ Generate an optimal schedule
- ✓ Let you refine with feedback
- ✓ Add to your calendar

**Example interaction:**

```
🤖 Generating plan from 2025-12-14 to 2025-12-28...
📅 Found 3 existing calendar events

✓ Plan generated with 3 scheduled tasks

📊 AI Reasoning: Prioritized high-priority task with upcoming deadline.
Scheduled deep focus work in morning hours based on preferences.
Distributed tasks across the week with adequate buffers.

📅 Generated Task Plan
┌────────────────────────┬──────────────┬──────────────┬──────────┬────────────────┐
│ Task                   │ Start Time   │ End Time     │ Duration │ Rationale      │
├────────────────────────┼──────────────┼──────────────┼──────────┼────────────────┤
│ Write project proposal │ Dec 14, 9:00 │ Dec 14, 11:30│ 2.5h     │ High priority  │
│ Code review            │ Dec 15, 14:00│ Dec 15, 15:30│ 1.5h     │ Medium priority│
│ Update documentation   │ Dec 16, 10:00│ Dec 16, 11:00│ 1.0h     │ Low priority   │
└────────────────────────┴──────────────┴──────────────┴──────────┴────────────────┘

Would you like to refine this plan? [y/N]: n
Execute this plan (add to calendar)? [Y/n]: y

✓ Plan executed and added to calendar!
```

## What's Next?

### Track Your Progress

```bash
# When you start a task
python main.py start task_1734123456

# When you complete it
python main.py complete task_1734123456
```

### Monitor in Real-Time

```bash
python main.py monitor
```

The agent watches your schedule and adapts automatically!

### View Your Insights

```bash
python main.py insights
```

See what the AI has learned about your working patterns.

### Use Interactive Mode

```bash
python main.py interactive
```

Chat with the agent directly!

## Optional: Google Calendar Integration

For full calendar sync:

1. **Get Google Calendar API credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project → Enable Calendar API → Create OAuth credentials
   - Download as `credentials.json`

2. **Place in project root:**
   ```
   AI_Agent/
   ├── credentials.json  ← Put it here
   ├── .env
   └── ...
   ```

3. **First run will open browser for authorization**

## CLI Command Reference

```bash
# Add tasks
python main.py add-task "Task title" [options]

# List tasks
python main.py list-tasks [--status pending|scheduled|completed]

# Generate plan
python main.py plan [--days 7] [--context "Additional instructions"]

# Track progress
python main.py start <task_id>
python main.py complete <task_id>

# Monitor (real-time)
python main.py monitor [--interval 15]

# Replan when needed
python main.py replan [--reason "Why replanning"]

# View insights
python main.py insights

# Interactive mode
python main.py interactive

# Help
python main.py --help
```

## Example Daily Usage

**Morning:**
```bash
python main.py list-tasks --status scheduled
# See what's planned for today
```

**During work:**
```bash
python main.py start task_xxx
# Work on task
python main.py complete task_xxx
```

**When plans change:**
```bash
python main.py replan --reason "Urgent meeting added"
```

**End of day:**
```bash
python main.py insights
# Review productivity patterns
```

## Tips for Best Results

1. **Be accurate with time estimates** - The agent learns and improves
2. **Provide feedback** - Refine plans to teach the agent your preferences
3. **Use priorities** - Helps the agent schedule optimally
4. **Mark tasks promptly** - Enables better learning
5. **Review insights weekly** - Track your productivity evolution

## Need Help?

- 📖 Full guide: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- 💻 Code examples: [example_usage.py](example_usage.py)
- 📘 Architecture: [README.md](README.md)

## Try It Now!

```bash
# Run the example
python example_usage.py
```

This demonstrates all features with sample tasks.

---

**You're all set!** The agent learns from every task and gets smarter over time. 🚀
