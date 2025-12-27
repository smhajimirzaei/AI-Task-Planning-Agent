"""
Streamlit UI for AI Task Planning Agent
========================================
A user-friendly interface to interact with the AI Task Planning Agent.
"""

import streamlit as st
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import traceback

# Configure page
st.set_page_config(
    page_title="AI Task Planning Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "configured" not in st.session_state:
    st.session_state.configured = False
if "agent" not in st.session_state:
    st.session_state.agent = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None
if "user_id" not in st.session_state:
    st.session_state.user_id = "streamlit_user"

def save_env_config(provider: str, api_key: str, model_name: str):
    """Save configuration to .env file"""
    env_path = Path(".env")

    # Determine which API key to set
    api_keys = {
        "ANTHROPIC_API_KEY": api_key if provider == "anthropic" else "",
        "OPENAI_API_KEY": api_key if provider == "openai" else "",
        "GOOGLE_API_KEY": api_key if provider == "google" else ""
    }

    env_content = f"""# AI Task Planning Agent Configuration
AI_PROVIDER={provider}
ANTHROPIC_API_KEY={api_keys["ANTHROPIC_API_KEY"]}
OPENAI_API_KEY={api_keys["OPENAI_API_KEY"]}
GOOGLE_API_KEY={api_keys["GOOGLE_API_KEY"]}
MODEL_NAME={model_name}
MAX_TOKENS=4096
TEMPERATURE=0.7

# Database
DATABASE_URL=sqlite:///./ai_agent.db

# Calendar Integration (Optional - configure if needed)
# GOOGLE_CALENDAR_CREDENTIALS=credentials.json
# GOOGLE_CALENDAR_TOKEN=token.json
# MICROSOFT_CLIENT_ID=your_client_id
# MICROSOFT_CLIENT_SECRET=your_client_secret
# MICROSOFT_TENANT_ID=your_tenant_id

# Agent Settings
DEFAULT_TIMEZONE=UTC
MONITORING_INTERVAL_MINUTES=15
LEARNING_MODE=enabled
"""
    env_path.write_text(env_content)
    return True

def initialize_agent(user_id: str, provider: str = "anthropic", api_key: str = None, model_name: str = None):
    """Initialize the AI Task Planning Agent with custom provider"""
    try:
        # Import the multi-provider service
        from services.ai_planner_multi import AIPlannerService
        from database.db_manager import DatabaseManager

        # Create a custom agent-like object
        class CustomAgent:
            def __init__(self, user_id, provider, api_key, model_name):
                self.user_id = user_id
                self.db = DatabaseManager()
                self.user_profile = self.db.get_profile(user_id)
                self.ai_planner = AIPlannerService(provider=provider, api_key=api_key, model_name=model_name)

                # Import other services
                from services.calendar_service import CalendarService
                from services.preference_learner import PreferenceLearner

                self.calendar_service = CalendarService(provider=self.user_profile.preferred_calendar)
                self.preference_learner = PreferenceLearner()
                self.monitoring_active = False
                self.monitoring_thread = None

            # Delegate methods to maintain compatibility
            def add_task(self, **kwargs):
                from models import Task, Priority
                task = Task(**kwargs)
                self.db.save_task(task)
                return task

            def list_tasks(self, status=None):
                return self.db.get_tasks(self.user_id, status=status)

            def mark_task_in_progress(self, task_id):
                from models import TaskStatus
                return self.db.update_task_status(task_id, TaskStatus.IN_PROGRESS)

            def mark_task_completed(self, task_id):
                from models import TaskStatus
                return self.db.update_task_status(task_id, TaskStatus.COMPLETED)

            def generate_plan(self, start_date=None, end_date=None, context=None):
                from datetime import datetime, timedelta
                if start_date is None:
                    start_date = datetime.now()
                if end_date is None:
                    end_date = start_date + timedelta(days=14)

                tasks = self.db.get_tasks(self.user_id, status="pending")
                calendar_events = self.calendar_service.get_events(start_date, end_date)
                return self.ai_planner.generate_plan(tasks, calendar_events, self.user_profile, context)

            def refine_plan(self, feedback, current_plan):
                return self.ai_planner.refine_plan(feedback, current_plan)

            def execute_plan(self, plan):
                from models import CalendarEvent, EventType
                from datetime import datetime
                events = []
                for scheduled_task in plan.get('scheduled_tasks', []):
                    event = CalendarEvent(
                        calendar_id=self.user_profile.preferred_calendar,
                        title=scheduled_task['title'],
                        description=f"Task: {scheduled_task['task_id']}",
                        start_time=datetime.fromisoformat(scheduled_task['scheduled_start']),
                        end_time=datetime.fromisoformat(scheduled_task['scheduled_end']),
                        event_type=EventType.SCHEDULED_TASK
                    )
                    self.calendar_service.create_event(event)
                    events.append(event)
                return events

            def get_insights(self):
                return self.preference_learner.get_insights(self.user_id, self.db)

        agent = CustomAgent(user_id, provider, api_key, model_name)
        return agent, None
    except Exception as e:
        import traceback
        return None, f"{str(e)}\n{traceback.format_exc()}"

# Sidebar - Configuration
with st.sidebar:
    st.title("🤖 AI Task Agent")
    st.markdown("---")

    if not st.session_state.configured:
        st.header("⚙️ Configuration")

        with st.form("config_form"):
            # AI Provider Selection
            ai_provider = st.selectbox(
                "AI Provider",
                options=["Anthropic (Claude)", "OpenAI (ChatGPT)", "Google (Gemini)"],
                help="Select which AI provider to use"
            )

            # Map display names to provider codes
            provider_map = {
                "Anthropic (Claude)": "anthropic",
                "OpenAI (ChatGPT)": "openai",
                "Google (Gemini)": "google"
            }
            provider_code = provider_map[ai_provider]

            # API Key input with dynamic label
            api_key_labels = {
                "anthropic": "Anthropic API Key (from console.anthropic.com)",
                "openai": "OpenAI API Key (from platform.openai.com)",
                "google": "Google API Key (from ai.google.dev)"
            }

            api_key = st.text_input(
                api_key_labels[provider_code],
                type="password",
                help=f"Enter your {ai_provider} API key"
            )

            user_id = st.text_input(
                "User ID",
                value=st.session_state.user_id,
                help="Unique identifier for your profile"
            )

            # Model selection based on provider
            model_options = {
                "anthropic": [
                    "claude-sonnet-4-5-20250929",
                    "claude-opus-4-5-20251101",
                    "claude-3-5-sonnet-20241022"
                ],
                "openai": [
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "gpt-3.5-turbo"
                ],
                "google": [
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-pro",
                    "gemini-1.5-flash"
                ]
            }

            model_name = st.selectbox(
                "Model",
                options=model_options[provider_code],
                help="Select the AI model to use"
            )

            submit = st.form_submit_button("💾 Save & Initialize", use_container_width=True)

            if submit:
                if not api_key:
                    st.error("Please provide an API key")
                else:
                    with st.spinner("Saving configuration and initializing agent..."):
                        # Save to .env
                        save_env_config(provider_code, api_key, model_name)

                        # No need to reload settings - we pass the values directly to the agent
                        # Initialize agent with custom provider
                        agent, error = initialize_agent(user_id, provider_code, api_key, model_name)

                        if error:
                            st.error(f"Failed to initialize agent: {error}")
                        else:
                            st.session_state.agent = agent
                            st.session_state.configured = True
                            st.session_state.user_id = user_id
                            st.session_state.provider = provider_code
                            st.session_state.model = model_name
                            st.success(f"✅ Agent initialized successfully with {ai_provider}!")
                            st.rerun()
    else:
        st.success("✅ Agent Ready")
        st.markdown(f"**User:** {st.session_state.user_id}")

        # Show provider info
        if "provider" in st.session_state:
            provider_names = {
                "anthropic": "Anthropic Claude",
                "openai": "OpenAI ChatGPT",
                "google": "Google Gemini"
            }
            st.markdown(f"**Provider:** {provider_names.get(st.session_state.provider, 'Unknown')}")

        if "model" in st.session_state:
            st.markdown(f"**Model:** {st.session_state.model}")

        if st.button("🔄 Reconfigure", use_container_width=True):
            st.session_state.configured = False
            st.session_state.agent = None
            st.rerun()

    st.markdown("---")

    # Navigation
    if st.session_state.configured:
        st.header("📋 Navigation")
        page = st.radio(
            "Select Page",
            ["💬 Chat", "📝 Tasks", "📅 Planning", "📊 Insights"],
            label_visibility="collapsed"
        )
    else:
        page = None

# Main content area
if not st.session_state.configured:
    # Welcome screen
    st.title("Welcome to AI Task Planning Agent 🤖")
    st.markdown("""
    ### Your AI-Powered Productivity Assistant

    This intelligent agent helps you:
    - 📝 **Manage tasks** with AI-powered prioritization
    - 📅 **Generate optimal schedules** based on your preferences
    - 🔄 **Adapt and learn** from your work patterns
    - 📊 **Track insights** and improve productivity
    - 🗓️ **Integrate with calendars** (Google Calendar, Outlook)

    ---

    ### Getting Started

    1. **Get an API Key**: Sign up at [console.anthropic.com](https://console.anthropic.com/)
    2. **Configure**: Enter your API key in the sidebar
    3. **Start Planning**: Add tasks and let AI optimize your schedule!

    ---

    ### Features

    - **Natural Language Chat**: Talk to your agent naturally
    - **Smart Scheduling**: AI considers priorities, deadlines, and focus requirements
    - **Real-time Monitoring**: Track schedule adherence and trigger replanning
    - **Adaptive Learning**: Gets smarter as it learns your preferences
    - **Calendar Sync**: Integrates with your existing calendar

    👈 **Configure your agent in the sidebar to begin!**
    """)

else:
    agent = st.session_state.agent

    # ==================== CHAT PAGE ====================
    if page == "💬 Chat":
        st.title("💬 Chat with Your AI Agent")
        st.markdown("Ask questions, add tasks, or request plans using natural language.")

        # Chat container
        chat_container = st.container()

        with chat_container:
            # Display chat history
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask your agent anything..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    message_placeholder = st.empty()

                    try:
                        # Process user input through AI
                        response = agent.ai_planner.chat(prompt)

                        # Store in history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response
                        })

                        message_placeholder.markdown(response)

                    except Exception as e:
                        error_msg = f"Error: {str(e)}"
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": error_msg
                        })
                        message_placeholder.error(error_msg)

        # Quick actions
        st.markdown("---")
        st.subheader("Quick Actions")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📋 List all tasks", use_container_width=True):
                tasks = agent.list_tasks()
                if tasks:
                    response = "**Current Tasks:**\n\n"
                    for task in tasks:
                        response += f"- [{task.priority.value}] {task.title} ({task.status.value})\n"
                else:
                    response = "No tasks found. Add some tasks to get started!"

                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

        with col2:
            if st.button("📊 Show insights", use_container_width=True):
                try:
                    insights = agent.get_insights()
                    response = f"**Productivity Insights:**\n\n{json.dumps(insights, indent=2, default=str)}"
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error getting insights: {e}")

        with col3:
            if st.button("🔄 Clear chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

    # ==================== TASKS PAGE ====================
    elif page == "📝 Tasks":
        st.title("📝 Task Management")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Add New Task")

            with st.form("add_task_form"):
                title = st.text_input("Task Title *", placeholder="e.g., Complete project report")
                description = st.text_area("Description", placeholder="Additional details...")

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
                with col_b:
                    duration = st.number_input("Duration (hours)", min_value=0.25, value=1.0, step=0.25)
                with col_c:
                    deadline_days = st.number_input("Deadline (days from now)", min_value=0, value=7, step=1)

                col_d, col_e = st.columns(2)
                with col_d:
                    requires_focus = st.checkbox("Requires Deep Focus")
                with col_e:
                    can_split = st.checkbox("Can be Split", value=True)

                tags = st.text_input("Tags (comma-separated)", placeholder="work, urgent, research")

                submitted = st.form_submit_button("➕ Add Task", use_container_width=True)

                if submitted:
                    if not title:
                        st.error("Task title is required")
                    else:
                        try:
                            deadline = datetime.now() + timedelta(days=deadline_days) if deadline_days > 0 else None
                            task_tags = [t.strip() for t in tags.split(",")] if tags else []

                            task = agent.add_task(
                                title=title,
                                description=description,
                                priority=priority,
                                estimated_duration=duration,
                                deadline=deadline,
                                requires_deep_focus=requires_focus,
                                can_split=can_split,
                                tags=task_tags
                            )

                            st.success(f"✅ Task '{task.title}' added successfully!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"Error adding task: {e}")
                            st.code(traceback.format_exc())

        with col2:
            st.subheader("Task Statistics")
            tasks = agent.list_tasks()

            # Count by status
            pending = len([t for t in tasks if t.status.value == "pending"])
            in_progress = len([t for t in tasks if t.status.value == "in_progress"])
            completed = len([t for t in tasks if t.status.value == "completed"])

            st.metric("Total Tasks", len(tasks))
            st.metric("Pending", pending)
            st.metric("In Progress", in_progress)
            st.metric("Completed", completed)

        st.markdown("---")
        st.subheader("Your Tasks")

        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            status_filter = st.selectbox("Filter by Status", ["All", "pending", "in_progress", "completed", "cancelled"])
        with filter_col2:
            sort_by = st.selectbox("Sort by", ["Priority", "Deadline", "Created"])

        # Display tasks
        filtered_tasks = agent.list_tasks(status=None if status_filter == "All" else status_filter)

        if filtered_tasks:
            for task in filtered_tasks:
                with st.expander(f"{'✅' if task.status.value == 'completed' else '📌'} [{task.priority.value.upper()}] {task.title}"):
                    st.markdown(f"**Description:** {task.description or 'No description'}")
                    st.markdown(f"**Status:** `{task.status.value}`")
                    st.markdown(f"**Duration:** {task.estimated_duration} hours")
                    if task.deadline:
                        st.markdown(f"**Deadline:** {task.deadline.strftime('%Y-%m-%d %H:%M')}")
                    if task.tags:
                        st.markdown(f"**Tags:** {', '.join(task.tags)}")

                    st.markdown(f"**Preferences:**")
                    st.markdown(f"- Deep Focus Required: {'Yes' if task.requires_deep_focus else 'No'}")
                    st.markdown(f"- Can Split: {'Yes' if task.can_split else 'No'}")

                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if task.status.value == "pending" and st.button("▶️ Start", key=f"start_{task.id}"):
                            agent.mark_task_in_progress(task.id)
                            st.rerun()
                    with col2:
                        if task.status.value != "completed" and st.button("✅ Complete", key=f"complete_{task.id}"):
                            agent.mark_task_completed(task.id)
                            st.rerun()
        else:
            st.info("No tasks found. Add your first task above!")

    # ==================== PLANNING PAGE ====================
    elif page == "📅 Planning":
        st.title("📅 AI Planning & Execution")

        st.subheader("Generate Optimal Schedule")

        with st.form("planning_form"):
            col1, col2 = st.columns(2)

            with col1:
                start_date = st.date_input("Start Date", value=datetime.now().date())
                start_time = st.time_input("Start Time", value=datetime.now().time())

            with col2:
                end_date = st.date_input("End Date", value=(datetime.now() + timedelta(days=14)).date())
                end_time = st.time_input("End Time", value=datetime.now().time())

            context = st.text_area(
                "Additional Context (Optional)",
                placeholder="e.g., 'Focus on urgent tasks first', 'Avoid scheduling on weekends', etc."
            )

            generate = st.form_submit_button("🧠 Generate Plan", use_container_width=True)

            if generate:
                with st.spinner("AI is generating your optimal schedule..."):
                    try:
                        start_dt = datetime.combine(start_date, start_time)
                        end_dt = datetime.combine(end_date, end_time)

                        plan = agent.generate_plan(
                            start_date=start_dt,
                            end_date=end_dt,
                            context=context if context else None
                        )

                        st.session_state.current_plan = plan
                        st.success("✅ Plan generated successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error generating plan: {e}")
                        st.code(traceback.format_exc())

        # Display current plan
        if st.session_state.current_plan:
            st.markdown("---")
            st.subheader("📋 Current Plan")

            plan = st.session_state.current_plan

            # Plan metadata
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Reasoning:** {plan.get('reasoning', 'N/A')}")
            with col2:
                if plan.get('warnings'):
                    st.warning(f"**Warnings:** {', '.join(plan['warnings'])}")

            if plan.get('suggestions'):
                st.success(f"**Suggestions:** {', '.join(plan['suggestions'])}")

            # Scheduled tasks
            st.markdown("### Scheduled Tasks")

            if plan.get('scheduled_tasks'):
                for idx, scheduled in enumerate(plan['scheduled_tasks'], 1):
                    with st.expander(f"{idx}. {scheduled['title']} - {scheduled['scheduled_start']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Start:** {scheduled['scheduled_start']}")
                            st.markdown(f"**End:** {scheduled['scheduled_end']}")
                            st.markdown(f"**Duration:** {scheduled['duration_hours']} hours")
                        with col2:
                            st.markdown(f"**Task ID:** `{scheduled['task_id']}`")
                            if scheduled.get('split_session'):
                                st.markdown(f"**Session:** {scheduled['split_session']} of {scheduled['total_sessions']}")

                        st.markdown(f"**Rationale:** {scheduled['rationale']}")

            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🚀 Execute Plan (Add to Calendar)", use_container_width=True):
                    with st.spinner("Executing plan and adding to calendar..."):
                        try:
                            events = agent.execute_plan(plan)
                            st.success(f"✅ Added {len(events)} events to calendar!")
                        except Exception as e:
                            st.error(f"Error executing plan: {e}")

            with col2:
                feedback = st.text_input("Provide feedback for refinement")
                if st.button("🔄 Refine Plan", use_container_width=True) and feedback:
                    with st.spinner("Refining plan based on your feedback..."):
                        try:
                            refined = agent.refine_plan(feedback, plan)
                            st.session_state.current_plan = refined
                            st.success("✅ Plan refined!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error refining plan: {e}")

            with col3:
                if st.button("🗑️ Clear Plan", use_container_width=True):
                    st.session_state.current_plan = None
                    st.rerun()

    # ==================== INSIGHTS PAGE ====================
    elif page == "📊 Insights":
        st.title("📊 Productivity Insights & Analytics")

        try:
            insights = agent.get_insights()

            # Metrics
            st.subheader("Key Metrics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Tasks",
                    insights.get("total_tasks", 0)
                )
            with col2:
                st.metric(
                    "Completed",
                    insights.get("completed_tasks", 0)
                )
            with col3:
                completion_rate = insights.get("completion_rate", 0)
                st.metric(
                    "Completion Rate",
                    f"{completion_rate:.1f}%"
                )
            with col4:
                st.metric(
                    "Avg Task Duration",
                    f"{insights.get('average_task_duration', 0):.1f}h"
                )

            # Detailed insights
            st.markdown("---")
            st.subheader("Detailed Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Task Distribution by Priority")
                if insights.get("tasks_by_priority"):
                    for priority, count in insights["tasks_by_priority"].items():
                        st.write(f"**{priority.upper()}:** {count} tasks")
                else:
                    st.info("No priority data available")

            with col2:
                st.markdown("### Task Distribution by Status")
                if insights.get("tasks_by_status"):
                    for status, count in insights["tasks_by_status"].items():
                        st.write(f"**{status.title()}:** {count} tasks")
                else:
                    st.info("No status data available")

            # Recommendations
            if insights.get("recommendations"):
                st.markdown("---")
                st.subheader("🎯 AI Recommendations")
                for rec in insights["recommendations"]:
                    st.success(rec)

            # Raw insights
            with st.expander("📄 View Raw Insights Data"):
                st.json(insights)

        except Exception as e:
            st.error(f"Error loading insights: {e}")
            st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "AI Task Planning Agent | Powered by Claude"
    "</div>",
    unsafe_allow_html=True
)
