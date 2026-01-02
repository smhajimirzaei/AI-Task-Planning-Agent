# Conversational Calendar Mode

The AI Task Planning Agent now works entirely through **conversational input** - no calendar API integration required!

## What Changed

### No More Calendar APIs
- **Before**: Required Google Calendar or Outlook credentials
- **After**: Share your schedule through simple text conversations

### Text-Based Workflow

1. **📥 Share Your Schedule**
   - Tell the agent about your week in natural language
   - Example: "Monday I have team meeting 9-10am, lunch 12-1pm. Tuesday morning is free, afternoon workshop 2-5pm."

2. **📝 Add Tasks**
   - Create tasks with priorities and deadlines as before
   - Agent knows your availability from your shared schedule

3. **📅 Get AI Plans**
   - Agent generates optimal schedule around your commitments
   - Plans shown with clear visualization

4. **📊 Weekly Review**
   - At week's end, tell the agent what you actually did
   - Agent learns from differences between plan and reality
   - Improves future recommendations

## Using the New Schedule Page

### Update Your Weekly Schedule

Navigate to **🗓️ Schedule** page and describe your week:

```
Monday: Team standup 9-9:30am, client meeting 2-3pm, gym 6-7pm
Tuesday: Free morning, lunch with mentor 12-1pm, workshop 3-6pm
Wednesday: All-day conference
Thursday: Meetings 9-11am, rest of day flexible
Friday: Sprint review 10-11am, afternoon for deep work
Weekend: Personal time
```

The agent will:
- Parse your schedule
- Store it for planning
- Use it to avoid conflicts when generating plans

### View Your Schedule

The Schedule page shows:
- **Current week's commitments**
- **Scheduled tasks** from AI plans
- **Quick stats** (number of events, time available)

### Record What Actually Happened

At the end of each week, use the **Weekly Review** section:

```
Monday: Standup was cancelled, used morning for focused work instead.
Client meeting went long until 4pm. Skipped gym.
Tuesday: Morning productive, lunch was great, workshop only until 4pm due to urgent issue.
Wednesday: Conference was valuable, made useful connections.
...etc
```

The AI will:
- Compare to the original plan
- Identify patterns (meetings run long, mornings more productive, etc.)
- Adjust future plans based on learnings

## Benefits

### 1. **No Setup Hassle**
- No OAuth flows
- No credential files
- No API quotas to worry about

### 2. **Privacy**
- Your actual calendar stays private
- Share only what you want the agent to know
- Full control over your data

### 3. **Flexibility**
- Update schedule anytime
- Easy to describe irregular weeks
- Natural language is more expressive

### 4. **Learning Loop**
- Agent learns from your feedback
- Gets better at predicting realistic schedules
- Understands your actual work patterns

## Technical Details

### TextCalendarService

New service class that:
- Parses schedule text (can be enhanced with AI)
- Stores events in local database
- No external API calls
- Provides visualization helpers

### Key Methods

```python
# Update schedule from text
agent.update_schedule(schedule_text, week_start)

# Get schedule summary
summary = agent.get_schedule_summary(days=7)

# Record actual completion
agent.record_completion(task_id, completion_text, completion_date)
```

### Data Storage

- Schedules stored in SQLite database
- No external dependencies
- Portable and version-controlled

## Workflow Example

### Week 1: Setup

**Monday - Share Schedule:**
```
User: "This week: Monday/Wed/Fri I have morning meetings 9-11.
Tuesday/Thursday are flexible. Weekend is personal time."
```

**Monday - Add Tasks:**
- Write project proposal (4 hours, high priority, deadline Friday)
- Review code PRs (2 hours, medium priority)
- Update documentation (3 hours, low priority)

**Monday - Get Plan:**
Agent generates schedule:
- Tuesday morning: Project proposal (9am-1pm)
- Tuesday afternoon: Code reviews (2pm-4pm)
- Thursday morning: Continue proposal (9am-11am)
- Thursday afternoon: Documentation (2pm-5pm)

**Friday - Weekly Review:**
```
User: "Monday meetings went well. Tuesday I got proposal done but code reviews  took longer - spent all afternoon on them. Thursday documentation was productive.
Proposal submitted Wednesday, a day early!"
```

AI learns:
- Code reviews take longer than estimated
- User can work faster on proposals than expected
- Adjust future estimates accordingly

### Week 2: Improved Planning

Agent now knows:
- Budget more time for code reviews
- User is efficient with proposals
- Can schedule more aggressive deadlines when motivated

## Comparison

| Feature | Old (API) | New (Conversational) |
|---------|-----------|---------------------|
| Setup | Complex OAuth | Just describe schedule |
| Privacy | Calendar access required | Share only what you want |
| Updates | Sync required | Edit text anytime |
| Learning | Limited | Rich from weekly reviews |
| Dependencies | Multiple APIs | None |
| Flexibility | Rigid | Natural language |

## Future Enhancements

Potential improvements:
1. **AI-Powered Parsing**: Use LLM to extract events from natural language
2. **Calendar Export**: Generate .ics files for importing elsewhere
3. **Pattern Recognition**: Identify recurring commitments automatically
4. **Conflict Detection**: Warn about scheduling conflicts
5. **Smart Suggestions**: "Based on past reviews, you usually need more time for X"

## Migration from API Version

If you were using calendar API integration:

1. No migration needed - old data is ignored
2. Start fresh by sharing your current schedule
3. All your tasks remain intact
4. Just update `preferred_calendar` to `"text"` in your profile

## Summary

The conversational calendar mode makes the AI Task Planning Agent:
- **Easier to use** - no complex setup
- **More private** - you control what you share
- **Smarter** - learns from your weekly feedback
- **More flexible** - natural language is more expressive

Perfect for users who want AI planning help without granting calendar access!
