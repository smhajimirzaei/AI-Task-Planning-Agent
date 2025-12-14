# AI Task Planning Agent - Workflow Diagrams

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                            USER                                 │
│  (Defines tasks, provides feedback, completes work)            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                        │
│                                                                 │
│  ┌────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  CLI Commands  │  │  Interactive    │  │  Python API     │ │
│  │  (Typer)       │  │  Mode           │  │  (Direct)       │ │
│  └────────────────┘  └─────────────────┘  └─────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AI PLANNING AGENT                             │
│                    (agent.py)                                   │
│                                                                 │
│  Core Responsibilities:                                         │
│  • Orchestrate all components                                  │
│  • Manage agent lifecycle                                      │
│  • Coordinate planning, execution, monitoring                  │
│                                                                 │
│  ┌────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Task Manager  │  │  Plan Executor  │  │  Monitor        │ │
│  └────────────────┘  └─────────────────┘  └─────────────────┘ │
└───────┬───────────────────┬───────────────────┬─────────────────┘
        │                   │                   │
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌────────────────┐  ┌─────────────────────┐
│               │  │                │  │                     │
│  AI Planner   │  │  Calendar      │  │  Preference         │
│  Service      │  │  Service       │  │  Learner            │
│               │  │                │  │                     │
│ ┌───────────┐ │  │ ┌────────────┐ │  │ ┌─────────────────┐│
│ │  Claude   │ │  │ │  Google    │ │  │ │ Pattern         ││
│ │  API      │ │  │ │  Calendar  │ │  │ │ Recognition     ││
│ │           │ │  │ │            │ │  │ │                 ││
│ │ • Plan    │ │  │ │ • Events   │ │  │ │ • Track         ││
│ │ • Refine  │ │  │ │ • Sync     │ │  │ │ • Learn         ││
│ │ • Analyze │ │  │ │ • CRUD     │ │  │ │ • Adapt         ││
│ └───────────┘ │  │ └────────────┘ │  │ └─────────────────┘│
│               │  │                │  │                     │
│               │  │ ┌────────────┐ │  │                     │
│               │  │ │  Outlook   │ │  │                     │
│               │  │ │  Calendar  │ │  │                     │
│               │  │ └────────────┘ │  │                     │
└───────────────┘  └────────────────┘  └─────────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER                               │
│                   (SQLite / PostgreSQL)                         │
│                                                                 │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │   Tasks      │  │  Calendar       │  │  User Profile    │  │
│  │   Table      │  │  Events Table   │  │  Table           │  │
│  │              │  │                 │  │                  │  │
│  │ • Metadata   │  │ • Events        │  │ • Preferences    │  │
│  │ • Status     │  │ • Scheduled     │  │ • Patterns       │  │
│  │ • Tracking   │  │ • Sync info     │  │ • Learning data  │  │
│  └──────────────┘  └─────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Planning Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  1. USER ADDS TASKS                                          │
│     python main.py add-task "Task" --priority high --duration 2
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  2. TASKS STORED IN DATABASE                                 │
│     • Task metadata saved                                    │
│     • Status set to PENDING                                  │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  3. USER INITIATES PLANNING                                  │
│     python main.py plan --days 14                            │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  4. AGENT GATHERS CONTEXT                                    │
│     • Load pending tasks from DB                             │
│     • Fetch calendar events (Google/Outlook)                 │
│     • Load user profile & preferences                        │
│     • Retrieve learned patterns                              │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  5. AI PLANNING (Claude)                                     │
│     • Analyze tasks, calendar, preferences                   │
│     • Consider priorities, deadlines, dependencies           │
│     • Apply learned productivity patterns                    │
│     • Generate optimal schedule                              │
│     • Provide reasoning & warnings                           │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  6. PRESENT PLAN TO USER                                     │
│     • Display schedule in formatted table                    │
│     • Show AI reasoning                                      │
│     • List warnings & suggestions                            │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  7. USER REVIEW & FEEDBACK                                   │
│     "Would you like to refine this plan?"                    │
│                                                              │
│     YES → Provide feedback → AI refines plan (loop to step 5)│
│     NO → Proceed to execution                                │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  8. EXECUTE PLAN                                             │
│     • Create calendar events for each scheduled task        │
│     • Sync to Google/Outlook calendar                        │
│     • Update task status to SCHEDULED                        │
│     • Store scheduled times in DB                            │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  9. MONITORING BEGINS                                        │
│     • Background thread starts                               │
│     • Tracks schedule adherence                              │
│     • Ready for task execution                               │
└──────────────────────────────────────────────────────────────┘
```

## Learning Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  USER STARTS TASK                                            │
│  python main.py start <task_id>                              │
│                                                              │
│  • actual_start = now()                                      │
│  • status = IN_PROGRESS                                      │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
              User works on task...
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  USER COMPLETES TASK                                         │
│  python main.py complete <task_id>                           │
│                                                              │
│  • actual_end = now()                                        │
│  • actual_duration = actual_end - actual_start               │
│  • status = COMPLETED                                        │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  PREFERENCE LEARNER ANALYZES                                 │
│                                                              │
│  Schedule Adherence:                                         │
│  • Compare actual_end vs scheduled_end                       │
│  • Update on_time / early / late counters                    │
│  • Calculate adherence rate                                  │
│                                                              │
│  Productivity Patterns:                                      │
│  • Identify hour of day (morning/afternoon/evening)          │
│  • Update peak_hours if completed early/on-time              │
│  • Track average_focus_span for deep work tasks              │
│                                                              │
│  Duration Learning:                                          │
│  • Store actual_duration vs estimated_duration               │
│  • Build history of similar tasks                            │
│  • Calculate estimation accuracy                             │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  IF SIGNIFICANT DEVIATION                                    │
│  (More than 15 minutes off schedule)                         │
│                                                              │
│  AI DEVIATION ANALYSIS:                                      │
│  • Claude analyzes why deviation occurred                    │
│  • Identifies patterns (task type, time of day, etc.)        │
│  • Recommends profile adjustments                            │
│  • Updates preferences if needed                             │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  UPDATE USER PROFILE                                         │
│  • Save updated productivity patterns                        │
│  • Update schedule adherence metrics                         │
│  • Adjust time estimation factors                            │
│  • Store learning metadata                                   │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  FUTURE PLANS BENEFIT                                        │
│  • Next plan uses updated patterns                           │
│  • Better time estimates                                     │
│  • Improved scheduling decisions                             │
│  • More personalized recommendations                         │
└──────────────────────────────────────────────────────────────┘
```

## Monitoring & Replanning Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  MONITORING LOOP (Background Thread)                         │
│  Runs every N minutes (default: 15)                          │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  CHECK SCHEDULED TASKS                                       │
│  • Get all tasks with status = SCHEDULED                     │
│  • Check current time vs scheduled times                     │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│  DEVIATION DETECTION                                         │
│                                                              │
│  For each task:                                              │
│  IF (now > scheduled_start + 15min) AND status=SCHEDULED:    │
│    → Task is LATE to start                                   │
│                                                              │
│  IF (now > scheduled_end) AND status=IN_PROGRESS:            │
│    → Task is OVERDUE                                         │
│                                                              │
│  IF task missed deadline:                                    │
│    → Update status to OVERDUE                                │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
                 Deviation detected?
                      │
            ┌─────────┴─────────┐
           NO                  YES
            │                   │
            │                   ▼
            │    ┌──────────────────────────────────────────┐
            │    │  ALERT USER                              │
            │    │  • Console notification                  │
            │    │  • Log the deviation                     │
            │    │  • (Future: Email/SMS notification)      │
            │    └─────────────┬────────────────────────────┘
            │                  │
            │                  ▼
            │    ┌──────────────────────────────────────────┐
            │    │  TRIGGER REPLAN?                         │
            │    │  • Automatic if configured               │
            │    │  • Or user manually triggers:            │
            │    │    python main.py replan                 │
            │    └─────────────┬────────────────────────────┘
            │                  │
            │                  ▼
            │    ┌──────────────────────────────────────────┐
            │    │  REPLANNING PROCESS                      │
            │    │                                          │
            │    │  1. Gather incomplete tasks              │
            │    │     (pending + scheduled + overdue)      │
            │    │                                          │
            │    │  2. Reset to pending status              │
            │    │     (clear old scheduled times)          │
            │    │                                          │
            │    │  3. Fetch updated calendar               │
            │    │                                          │
            │    │  4. Generate new plan with context       │
            │    │     "Replanning due to: [reason]"        │
            │    │                                          │
            │    │  5. Prioritize overdue tasks             │
            │    │                                          │
            │    │  6. Present to user for approval         │
            │    │                                          │
            │    │  7. Execute new plan                     │
            │    └─────────────┬────────────────────────────┘
            │                  │
            └──────────────────┴───────────┐
                                           │
                                           ▼
                              ┌────────────────────────────┐
                              │  Continue monitoring       │
                              │  Wait N minutes            │
                              │  Loop back to start        │
                              └────────────────────────────┘
```

## Data Flow Diagram

```
INPUT                    PROCESSING                   OUTPUT
──────                   ──────────                   ──────

Tasks                       ┌──────┐
Deadlines      ──────────>  │      │
Priorities                  │      │                Calendar Events
                            │  AI  │                (Google/Outlook)
Calendar       ──────────>  │ Plan │  ────────────>
Events                      │ Agent│                Updated Schedule
                            │      │
User Profile   ──────────>  │      │                Insights &
Preferences                 │      │  ────────────> Recommendations
                            │      │
Learned        ──────────>  └──────┘                Learned
Patterns                       │                    Patterns
                               │
                               │
                               ▼
                         [Database]
                         • Tasks
                         • Events
                         • Profile
```

## Feedback Loop

```
                    ┌───────────────────────┐
                    │  Initial Planning     │
                    └──────────┬────────────┘
                               │
                               ▼
                    ┌───────────────────────┐
          ┌────────│  Present Plan         │
          │        └──────────┬────────────┘
          │                   │
          │                   ▼
          │        ┌───────────────────────┐
          │        │  User Feedback        │
          │        │  • Specific changes   │
          │        │  • Preference updates │
          │        └──────────┬────────────┘
          │                   │
          │                   ▼
          │        ┌───────────────────────┐
          │        │  Preference Learner   │
          │        │  • Parse feedback     │
          │        │  • Update profile     │
          └────────│  • Refine plan        │
                   └──────────┬────────────┘
                              │
                              ▼
                   ┌───────────────────────┐
                   │  Execute & Monitor    │
                   └──────────┬────────────┘
                              │
                              ▼
                   ┌───────────────────────┐
                   │  Task Completion      │
                   │  • Track actual time  │
                   │  • Learn patterns     │
                   └──────────┬────────────┘
                              │
                              │ (Next planning cycle)
                              │
                              ▼
                   ┌───────────────────────┐
                   │  Improved Planning    │
                   │  Uses learned data    │
                   └───────────────────────┘
```

## Technology Stack Flow

```
┌─────────────────────────────────────────────────────────────┐
│  USER INTERACTION                                           │
│  • Command Line (Typer + Rich)                             │
│  • Python API (direct function calls)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER (Python)                                 │
│  • agent.py - Main orchestrator                            │
│  • main.py - CLI entry point                               │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌─────────────┐  ┌─────────────────┐
│  Services    │  │  Models     │  │  Database       │
│              │  │             │  │                 │
│ • AI Planner │  │ • Task      │  │ • SQLAlchemy    │
│ • Calendar   │  │ • Event     │  │ • SQLite        │
│ • Learner    │  │ • Profile   │  │                 │
│              │  │ (Pydantic)  │  │                 │
└──────┬───────┘  └─────────────┘  └─────────────────┘
       │
       ├─────────────┬────────────────┐
       │             │                │
       ▼             ▼                ▼
┌────────────┐  ┌──────────┐  ┌──────────────┐
│ Anthropic  │  │  Google  │  │  Microsoft   │
│ Claude API │  │ Calendar │  │  Graph API   │
└────────────┘  └──────────┘  └──────────────┘
```

---

## Key Interactions Summary

1. **User → Agent**: Add tasks, request planning
2. **Agent → Database**: Store/retrieve tasks, events, profile
3. **Agent → Calendar**: Fetch events, create task blocks
4. **Agent → AI**: Generate/refine plans, analyze deviations
5. **Agent → Learner**: Track completions, learn patterns
6. **Learner → Profile**: Update preferences, patterns
7. **Profile → AI**: Inform future planning decisions
8. **Monitor → Agent**: Detect deviations, trigger replans

All components work together in a continuous cycle of planning, execution, learning, and adaptation.
