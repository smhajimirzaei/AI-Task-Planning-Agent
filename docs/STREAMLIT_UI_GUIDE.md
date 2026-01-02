# Streamlit UI Guide

Complete guide to using the AI Task Planning Agent through the Streamlit web interface.

## Table of Contents

- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Pages Overview](#pages-overview)
- [Chat Page](#chat-page)
- [Tasks Page](#tasks-page)
- [Schedule Page](#schedule-page)
- [Planning Page](#planning-page)
- [Insights Page](#insights-page)
- [Tips & Best Practices](#tips--best-practices)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Launch the Application

```bash
# Using Python 3.13 (or your version)
py -3.13 -m streamlit run streamlit_app.py

# Or standard Python
python -m streamlit run streamlit_app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

### First Time Setup

On first launch, you'll see the welcome screen with:
- Overview of how the agent works
- Getting started instructions
- Links to get API keys

## Configuration

### Initial Configuration

1. In the **sidebar**, you'll see the configuration form
2. Select your **AI Provider**:
   - **Anthropic (Claude)** - Best for complex reasoning
   - **OpenAI (ChatGPT)** - Fast and reliable
   - **Google (Gemini)** - Free tier available
3. Enter your **API Key** for the selected provider
4. Choose a **Model** from the dropdown
5. Set your **User ID** (or keep default: `streamlit_user`)
6. Click **Save & Initialize**

### Getting API Keys

#### Anthropic Claude
1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new key
5. Copy and paste into Streamlit

#### OpenAI ChatGPT
1. Visit [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new secret key
5. Copy and paste into Streamlit

#### Google Gemini
1. Visit [ai.google.dev](https://ai.google.dev/)
2. Click "Get API key in Google AI Studio"
3. Sign in with Google account
4. Create an API key
5. Copy and paste into Streamlit

### Reconfiguring

To change providers or models:
1. Click **Reconfigure** button in the sidebar
2. Configuration form will appear again
3. Select new provider/model
4. Save & Initialize

Your tasks and data remain intact when switching providers.

## Pages Overview

The sidebar shows 5 main pages:

| Page | Icon | Purpose |
|------|------|---------|
| Chat | 💬 | Conversational interface with AI |
| Tasks | 📝 | Manage and track tasks |
| Schedule | 🗓️ | Share weekly schedule |
| Planning | 📅 | Generate and execute AI plans |
| Insights | 📊 | View analytics and patterns |

## Chat Page

### Overview
The Chat page provides a conversational interface to talk with your AI assistant about tasks, schedules, and planning.

### Features

**Natural Conversation**
- Ask questions about your schedule
- Discuss task priorities
- Get planning advice
- Request recommendations

**Chat History**
- Scrollable conversation history
- Persistent across sessions
- Clear formatting for readability

**Message Input**
- Large text area for detailed queries
- Send button to submit
- Support for multi-line messages

### Example Conversations

```
You: What should I prioritize this week?
AI: Based on your current tasks, I recommend focusing on:
    1. High-priority items with upcoming deadlines
    2. Deep focus work during your productive morning hours
    3. ...

You: When is the best time to schedule my code review task?
AI: Based on your shared schedule and productivity patterns...
```

### Tips
- Be specific about what you need
- Reference tasks by name
- Ask follow-up questions
- Use for planning discussions before generating formal plans

## Tasks Page

### Overview
Central hub for managing all your tasks with quick actions and status tracking.

### Add New Task

1. Fill in the **Add New Task** form:
   - **Task Title** (required) - Clear, descriptive name
   - **Description** (optional) - Additional details
   - **Priority** - High, Medium, or Low
   - **Duration** - Estimated hours (e.g., 2.5)
   - **Deadline** - Due date picker
   - **Deep Focus** - Check if requires uninterrupted time

2. Click **Add Task**

3. Task appears in the list immediately

### View Tasks

**Filter Options**
- All tasks
- Only pending tasks
- Only in-progress tasks
- Only completed tasks

**Task Cards Display**
Each task shows:
- Title and description
- Priority badge (color-coded)
- Duration estimate
- Deadline
- Deep focus indicator
- Current status

**Color Coding**
- 🔴 High priority (red)
- 🟡 Medium priority (yellow)
- 🟢 Low priority (green)

### Quick Actions

For each task, you can:
- **▶️ Start** - Mark as in-progress
- **✅ Complete** - Mark as completed

Status changes are instant and reflected immediately.

### Best Practices

1. **Be Realistic with Time Estimates**
   - Start with your best guess
   - Agent learns and improves estimates over time

2. **Use Priorities Wisely**
   - High: Urgent and important
   - Medium: Important but not urgent
   - Low: Nice to have

3. **Enable Deep Focus** when needed
   - Agent will schedule during productive hours
   - Ensures uninterrupted time blocks

4. **Add Details to Description**
   - Helps AI understand context
   - Improves plan quality

## Schedule Page

### Overview
Share your weekly schedule through natural language and view visual summaries. No calendar API integration required!

### Update Weekly Schedule

1. Navigate to **Update Your Weekly Schedule** section

2. In the text area, describe your week in natural language:

```
Example:

Monday: Team standup 9-9:30am, client meeting 2-3pm, gym 6-7pm
Tuesday: Free morning, lunch with mentor 12-1pm, workshop 3-6pm
Wednesday: All-day conference
Thursday: Meetings 9-11am, rest of day flexible
Friday: Sprint review 10-11am, afternoon for deep work
Weekend: Personal time
```

3. Select **Week starting from** date (defaults to current week's Monday)

4. Click **Update Schedule**

5. Success message confirms schedule saved

### View Schedule

**Schedule Summary**
- Shows all events for the current week
- Grouped by date
- Time ranges for each event
- All-day events marked clearly

**Quick Stats**
- Number of scheduled events
- Current week date range
- Time available for tasks

### Weekly Review

At the end of each week, use the Weekly Review section to help the AI learn:

1. Click to expand **Record What You Actually Did**

2. Describe what actually happened:

```
Example:

Monday: Standup was cancelled, used morning for focused work instead.
Client meeting went long until 4pm. Skipped gym.
Tuesday: Morning productive, lunch was great, workshop only until 4pm due to urgent issue.
Wednesday: Conference was valuable, made useful connections.
Thursday: Meetings ran over until noon, worked on project in afternoon.
Friday: Sprint planning was productive, spent afternoon on documentation as planned.
```

3. Select **Week ending** date

4. Click **Record Completion**

5. AI analyzes and provides feedback comparing plan vs reality

### Why Weekly Reviews Matter

The AI learns from your reviews:
- **Time Estimates**: Adjusts predictions based on actual durations
- **Patterns**: Identifies that meetings often run long
- **Productivity**: Learns your peak productive times
- **Preferences**: Understands your working style

Over time, this makes future plans increasingly accurate and personalized.

### Schedule Tips

**Be Conversational**
- Write naturally: "Monday morning I have..."
- Don't worry about perfect formatting
- AI understands various time formats

**Include All Commitments**
- Meetings and calls
- Personal appointments
- Gym, meals, breaks
- Commute time
- Fixed working hours

**Update Regularly**
- Weekly updates work best
- Can update mid-week if schedule changes
- Keep AI informed of your availability

## Planning Page

### Overview
Generate AI-powered optimal schedules and execute plans.

### Generate New Plan

1. Set **Planning Horizon**:
   - **Start Date**: When to begin planning
   - **End Date**: Planning window end

2. (Optional) Add **Context**:
   - Any special considerations
   - Preferences for this period
   - Constraints or requirements

3. Click **Generate Plan**

4. AI analyzes:
   - All pending tasks
   - Your shared schedule
   - Learned preferences
   - Time available

5. Plan appears below with:
   - Scheduled tasks
   - Time allocations
   - Rationale for decisions

### Refine Plan

Don't like the proposed schedule? Provide feedback:

1. In the **Refine Plan** section, describe changes:

```
Examples:
- "Move deep work tasks to mornings"
- "I need Wednesday afternoon free for a personal appointment"
- "Can we finish the report by Thursday instead?"
```

2. Click **Refine Plan**

3. AI generates updated plan based on your feedback

4. Can refine multiple times until satisfied

### Execute Plan

Once happy with the plan:

1. Click **Execute Plan**

2. Tasks are created as calendar events in the database

3. Success message shows number of events created

4. View in Schedule page

### Plan Display

Plans show:
- **Scheduled Tasks** table with:
  - Task title
  - Scheduled start time
  - Scheduled end time
  - Duration
  - Rationale

- **AI Reasoning** (if available):
  - Why tasks were scheduled at specific times
  - How priorities were balanced
  - Considerations made

### Planning Tips

**Provide Good Context**
```
Good examples:
- "I work best in the mornings"
- "Need to finish the report before Friday's meeting"
- "Wednesday afternoon I have a dental appointment"
```

**Iterate on Plans**
- First plan is a starting point
- Refine until it feels right
- AI learns from your refinement feedback

**Execute When Ready**
- No need to execute immediately
- Can generate multiple plans to compare
- Executing replaces previous plan events

## Insights Page

### Overview
View productivity analytics, patterns, and get personalized recommendations.

### Insights Display

**Productivity Patterns**
- Peak productive hours
- Task completion rates
- Average focus duration
- Schedule adherence

**Task Analysis**
- Estimation accuracy
- Time by priority level
- Completion velocity
- Blocked/delayed tasks

**Recommendations**
- Personalized suggestions based on your data
- Tips to improve productivity
- Scheduling advice
- Areas for improvement

### Using Insights

1. Navigate to Insights page

2. Click **Refresh Insights** to get latest analysis

3. Review displayed metrics

4. Apply recommendations to improve planning

### Insights Tips

**Need More Data**
- Insights improve with more task completions
- Weekly reviews provide valuable learning data
- Track at least 2-3 weeks for meaningful patterns

**Act on Recommendations**
- AI suggestions are based on your actual data
- Try implementing one recommendation at a time
- See if it improves your productivity

## Tips & Best Practices

### General Tips

1. **Start Simple**
   - Add a few tasks to begin
   - Share your schedule
   - Generate your first plan
   - Learn the interface

2. **Build the Habit**
   - Weekly schedule updates
   - Daily task additions
   - Weekly reviews
   - Regular plan generation

3. **Trust the Process**
   - AI gets better over time
   - Initial plans may not be perfect
   - Refinement is part of the workflow
   - Learning happens through feedback

### Workflow Recommendations

**Monday Morning Routine**
1. Update weekly schedule
2. Add new tasks for the week
3. Generate plan for the week
4. Review and refine if needed
5. Execute plan

**Daily Check-ins**
- Mark tasks as in-progress when starting
- Mark completed when done
- Add new tasks as they arise
- Check chat for quick questions

**Friday Evening Review**
1. Complete weekly review
2. Mark all finished tasks complete
3. Review insights
4. Prepare for next week

### Maximizing AI Learning

**Detailed Weekly Reviews**
- Be specific about what happened
- Mention deviations from plan
- Note what worked well
- Highlight challenges faced

**Consistent Feedback**
- Use plan refinement feature
- Explain your preferences
- Share context in chat
- Update schedule regularly

## Troubleshooting

### Common Issues

#### Agent Not Initialized
**Symptom**: Configuration screen keeps showing

**Solution**:
1. Check API key is correct
2. Verify you have credits/quota
3. Try different provider
4. Check browser console for errors

#### Plans Not Generating
**Symptom**: Error when clicking "Generate Plan"

**Solution**:
1. Ensure you have pending tasks
2. Verify schedule is updated
3. Check planning dates are valid
4. Try with context provided

#### Tasks Not Appearing
**Symptom**: Added task doesn't show in list

**Solution**:
1. Check status filter (might be filtered out)
2. Refresh page
3. Try adding again with different title
4. Check browser console

#### Schedule Not Saving
**Symptom**: Updated schedule doesn't persist

**Solution**:
1. Verify week start date is selected
2. Check schedule text is not empty
3. Look for success message
4. Refresh Schedule page to verify

### Getting Help

1. **Check Documentation**
   - MULTI_PROVIDER_README.md for provider issues
   - CONVERSATIONAL_CALENDAR_README.md for schedule help
   - This guide for UI questions

2. **Browser Console**
   - Press F12 to open developer tools
   - Check Console tab for errors
   - Share errors when reporting issues

3. **Reset Configuration**
   - Click "Reconfigure" in sidebar
   - Re-enter all settings
   - Re-initialize agent

### Performance Tips

**Slow Loading**
- Check internet connection (API calls require network)
- Try gpt-4o-mini or gemini-flash for faster responses
- Close other resource-intensive tabs

**Large Chat History**
- Chat history grows over time
- Consider clearing browser storage periodically
- Or start fresh with new user ID

## Advanced Features

### Switching Providers Mid-Session

You can switch AI providers at any time:

1. Click **Reconfigure**
2. Select different provider
3. Enter API key for new provider
4. All data persists (tasks, schedule, etc.)
5. Chat history preserved

Use cases:
- Try different AIs for different tasks
- Switch to free tier (Gemini) to save costs
- Use premium model (Opus) for complex planning

### Multiple User Profiles

Use different User IDs for separate contexts:

- `work` - Work-related tasks
- `personal` - Personal projects
- `team_planning` - Team coordination

Each user ID has separate:
- Tasks
- Schedule
- Preferences
- Chat history

### Custom Scheduling Logic

When refining plans, you can request:

- Batch similar tasks
- Spread out similar tasks
- Schedule by energy level
- Group by project
- Prioritize deadlines
- Balance work types

Example:
```
"Group all coding tasks together for deep focus.
Schedule meetings in the afternoon.
Keep mornings for creative work."
```

## Summary

The Streamlit UI provides an intuitive, conversational way to:

✅ Chat with AI about tasks and planning
✅ Manage tasks with visual feedback
✅ Share schedule through natural language
✅ Generate and refine AI-powered plans
✅ Track insights and improve over time

**Key to Success**: Regular use, honest weekly reviews, and iterative refinement.

Start simple, build habits, let the AI learn your patterns, and watch your productivity improve!

---

**Need more help?** Check out:
- [Multi-Provider Setup](MULTI_PROVIDER_README.md)
- [Conversational Calendar Guide](CONVERSATIONAL_CALENDAR_README.md)
- [Quick Start Guide](../QUICKSTART.md)
