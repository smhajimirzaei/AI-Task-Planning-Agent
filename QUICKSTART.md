# Quick Start Guide

Get up and running with the AI Task Planning Agent in 5 minutes!

## Two Ways to Get Started

### Option 1: Streamlit Web UI (Recommended) ⭐

The easiest way to use the agent - beautiful interface, no configuration files needed!

#### 1. Install Dependencies (1 min)

```bash
# Clone the repository
git clone <repository-url>
cd AI_Agent

# Install packages
pip install -r requirements.txt

# Or with specific Python version
py -3.13 -m pip install -r requirements.txt
```

#### 2. Launch Streamlit App (30 seconds)

```bash
python -m streamlit run streamlit_app.py

# Or with specific Python version
py -3.13 -m streamlit run streamlit_app.py
```

The app automatically opens at `http://localhost:8501`

#### 3. Configure in Browser (1 min)

In the sidebar:

1. **Select AI Provider**:
   - Anthropic Claude (best reasoning)
   - OpenAI ChatGPT (fast, reliable)
   - Google Gemini (free tier!)

2. **Get API Key** - Click the link for your provider:
   - Anthropic: [console.anthropic.com](https://console.anthropic.com/)
   - OpenAI: [platform.openai.com](https://platform.openai.com/)
   - Google: [ai.google.dev](https://ai.google.dev/)

3. **Paste API Key** in the form

4. **Choose Model** from dropdown

5. **Click "Save & Initialize"**

✅ **Done!** You're ready to use the agent.

#### 4. Share Your Schedule (1 min)

Navigate to **🗓️ Schedule** page and describe your week:

```
Monday: Team standup 9-9:30am, client call 2-3pm
Tuesday: Free morning, workshop 3-5pm
Wednesday: All-day conference
Thursday: Meetings 9-11am, afternoon flexible
Friday: Sprint review 10-11am, rest of day open
Weekend: Personal time
```

Click "Update Schedule"

#### 5. Add Tasks (1 min)

Go to **📝 Tasks** page and add tasks:

- **Title**: "Write project proposal"
- **Priority**: High
- **Duration**: 2.5 hours
- **Deadline**: Select date
- **Deep Focus**: ✓ (if needed)

Click "Add Task"

Repeat for more tasks.

#### 6. Generate Your Plan (1 min)

Navigate to **📅 Planning** page:

1. Set date range (defaults to next 2 weeks)
2. (Optional) Add context: "I work best in mornings"
3. Click **Generate Plan**
4. Review the AI's proposed schedule
5. (Optional) Refine with feedback
6. Click **Execute Plan** when ready

**🎉 You're all set!** Your schedule is planned and ready.

---

### Option 2: Command Line Interface

For developers who prefer the terminal.

#### 1. Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

#### 2. Configure API Key (1 min)

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API key
```

**.env file:**
```env
# Choose provider
AI_PROVIDER=anthropic  # or openai, or google

# Add your key
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
# OR
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
# OR
GOOGLE_API_KEY=xxxxxxxxxxxxx

# Choose model
MODEL_NAME=claude-sonnet-4-5-20250929
```

Get your key from:
- Anthropic: [console.anthropic.com](https://console.anthropic.com/)
- OpenAI: [platform.openai.com](https://platform.openai.com/)
- Google: [ai.google.dev](https://ai.google.dev/)

#### 3. Run Setup (1 min)

```bash
python main.py setup
```

Answer questions about your working hours and preferences.

#### 4. Add Your First Tasks (1 min)

```bash
python main.py add-task "Write project proposal" \
  --priority high \
  --duration 2.5 \
  --deadline 2025-12-20

python main.py add-task "Code review" \
  --priority medium \
  --duration 1.5

python main.py add-task "Update documentation" \
  --priority low \
  --duration 1.0
```

#### 5. Generate Your First Plan (1 min)

```bash
python main.py plan
```

The AI will:
- ✓ Analyze your tasks
- ✓ Check your schedule
- ✓ Generate an optimal plan
- ✓ Let you refine with feedback
- ✓ Save to database

**Example interaction:**

```
🤖 Generating plan from 2025-12-28 to 2026-01-11...

✓ Plan generated with 3 scheduled tasks

📊 AI Reasoning: Prioritized high-priority task with upcoming deadline.
Scheduled deep focus work in morning hours based on preferences.
Distributed tasks across the week with adequate buffers.

📅 Generated Task Plan
┌────────────────────────┬──────────────┬──────────────┬──────────┐
│ Task                   │ Start Time   │ End Time     │ Duration │
├────────────────────────┼──────────────┼──────────────┼──────────┤
│ Write project proposal │ Dec 30, 9:00 │ Dec 30, 11:30│ 2.5h     │
│ Code review            │ Dec 31, 14:00│ Dec 31, 15:30│ 1.5h     │
│ Update documentation   │ Jan 2, 10:00 │ Jan 2, 11:00 │ 1.0h     │
└────────────────────────┴──────────────┴──────────────┴──────────┘

Would you like to refine this plan? [y/N]:
```

---

## What's Next?

### Streamlit UI Users

**Weekly Routine:**

1. **Monday Morning**:
   - Update Schedule page with this week's commitments
   - Add new tasks on Tasks page
   - Generate plan on Planning page

2. **During the Week**:
   - Mark tasks in-progress and completed
   - Chat with AI for questions
   - Add new tasks as they arise

3. **Friday Evening**:
   - Complete weekly review on Schedule page
   - Check Insights page for patterns
   - Plan next week

### CLI Users

**Track Your Progress:**

```bash
# When you start a task
python main.py start <task_id>

# When you complete it
python main.py complete <task_id>
```

**View Insights:**

```bash
python main.py insights
```

**Interactive Mode:**

```bash
python main.py interactive
```

Chat with the agent directly in terminal!

## Features You Should Try

### 1. Conversational Calendar

**Why it's great**: No calendar API integration needed!

- Share schedule through natural language
- Full privacy - your actual calendar stays private
- Update anytime with new text descriptions

[Learn more →](CONVERSATIONAL_CALENDAR_README.md)

### 2. Multi-Provider AI

**Why it's great**: Choose the best AI for your needs!

- Anthropic Claude: Best reasoning and planning
- OpenAI ChatGPT: Fast and reliable
- Google Gemini: Free tier available

Switch anytime - your data persists!

[Learn more →](MULTI_PROVIDER_README.md)

### 3. Weekly Reviews

**Why it's great**: Agent learns from your feedback!

Every week, tell the agent what actually happened vs the plan.

The AI learns:
- Your actual working patterns
- How long tasks really take
- When you're most productive
- What kind of plans work for you

Plans get better every week!

### 4. Visual Interface

**Why it's great**: See everything clearly!

- Task dashboard with filters
- Visual schedule summaries
- Plan comparisons
- Productivity insights

## Common Workflows

### Planning a New Project

**Streamlit:**
1. Go to Tasks → Add all project tasks
2. Go to Planning → Generate plan
3. Review and refine
4. Execute

**CLI:**
```bash
python main.py add-task "Design API" --priority high --duration 4
python main.py add-task "Implement API" --priority high --duration 8
python main.py add-task "Write tests" --priority medium --duration 3
python main.py plan --context "New API project, deadline in 2 weeks"
```

### Adapting to Schedule Changes

**Streamlit:**
1. Update Schedule with new commitments
2. Go to Planning → Generate new plan
3. Existing tasks automatically rescheduled

**CLI:**
```bash
python main.py replan --reason "Unexpected meeting added"
```

### Reviewing Your Week

**Streamlit:**
1. Go to Schedule → Weekly Review
2. Describe what actually happened
3. Get AI feedback and learning

**CLI:**
```bash
python main.py insights
# Review productivity patterns
```

## Tips for Best Results

### General Tips

1. **Be Realistic with Estimates**
   - Start with your best guess
   - Agent learns and adjusts over time

2. **Update Schedule Weekly**
   - Share your commitments
   - More data = better plans

3. **Complete Weekly Reviews**
   - This is where the AI learns
   - Be honest about what happened

4. **Use Priorities Wisely**
   - High: Urgent and important
   - Medium: Important but flexible
   - Low: Nice to have

5. **Trust the Learning Process**
   - First plans may not be perfect
   - Agent improves with each week
   - Refinement is part of the workflow

### Getting Good AI Responses

**When chatting:**
```
Good: "When should I schedule deep focus work on the API design task?"
Bad: "What do you think?"

Good: "Move my coding tasks to mornings, I'm more productive then"
Bad: "Change the schedule"
```

**When providing context:**
```
Good: "I have a hard deadline Friday, need to finish report before then"
Bad: "Make it fast"
```

## CLI Command Reference

```bash
# Add tasks
python main.py add-task "Task title" [options]
  --priority [high|medium|low]
  --duration HOURS
  --deadline YYYY-MM-DD
  --deep-focus

# List tasks
python main.py list-tasks [--status pending|scheduled|completed]

# Generate plan
python main.py plan [--days 7] [--context "Additional instructions"]

# Track progress
python main.py start <task_id>
python main.py complete <task_id>

# View insights
python main.py insights

# Interactive mode
python main.py interactive

# Help
python main.py --help
```

## Troubleshooting

### "API Key Invalid" Error

- Double-check you copied the complete key
- Ensure you're using the right key for selected provider
- Check you have credits/quota available

### Streamlit Won't Start

```bash
# Try with module syntax
python -m streamlit run streamlit_app.py

# Or with specific Python version
py -3.13 -m streamlit run streamlit_app.py
```

### "No tasks found" When Planning

- Add at least one task first
- Check task status (should be "pending")
- Try `list-tasks` to verify tasks exist

### Plans Don't Match Your Schedule

- Make sure you updated schedule on Schedule page
- Provide context when generating plans
- Use plan refinement feature to adjust

## Get More Help

- 📖 **Streamlit UI Guide**: [STREAMLIT_UI_GUIDE.md](STREAMLIT_UI_GUIDE.md)
- 🤖 **Multi-Provider Setup**: [MULTI_PROVIDER_README.md](MULTI_PROVIDER_README.md)
- 📅 **Calendar Guide**: [CONVERSATIONAL_CALENDAR_README.md](CONVERSATIONAL_CALENDAR_README.md)
- 📘 **Full Documentation**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- 💻 **Code Examples**: [example_usage.py](example_usage.py)

## Try the Example

```bash
# Run the full example
python example_usage.py
```

This demonstrates all features with sample tasks.

---

## You're Ready! 🚀

**Streamlit Users**: Visit `http://localhost:8501` and start planning!

**CLI Users**: Run `python main.py interactive` to chat with your AI assistant!

The agent learns from every task and gets smarter over time. Start simple, provide feedback, and watch your productivity improve week by week.

**Happy Planning!** 🎯
