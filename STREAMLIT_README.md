# Streamlit UI for AI Task Planning Agent

A beautiful, user-friendly web interface for the AI Task Planning Agent, powered by Streamlit.

## Features

- **💬 Chat Interface**: Natural language interaction with your AI agent
- **📝 Task Management**: Add, view, and manage tasks with an intuitive UI
- **📅 AI Planning**: Generate optimal schedules with AI-powered planning
- **📊 Insights Dashboard**: View productivity analytics and recommendations
- **⚙️ Easy Configuration**: Simple setup with API key input

## Quick Start

### 1. Install Dependencies

First, make sure you have all required packages installed:

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

This will open the app in your default web browser at `http://localhost:8501`

### 3. Configure Your Agent

On first launch, you'll see the configuration page. Enter:

1. **Anthropic API Key**: Get one from [console.anthropic.com](https://console.anthropic.com/)
2. **User ID**: Choose a unique identifier for your profile (e.g., "john_doe")
3. **Claude Model**: Select your preferred model (default: Claude Sonnet 4.5)

Click "Save & Initialize" to start using the agent.

## Using the Interface

### 💬 Chat Page

Talk to your agent using natural language:

- "Add a task to write the quarterly report"
- "Show me all my pending tasks"
- "What should I work on today?"
- "Generate a plan for this week"

**Quick Actions:**
- List all tasks
- Show insights
- Clear chat history

### 📝 Tasks Page

**Add New Tasks:**
- Fill in task details (title, description, priority, duration)
- Set deadlines and preferences
- Add tags for organization

**Manage Existing Tasks:**
- View all tasks with filtering by status
- Start tasks (mark as in-progress)
- Complete tasks
- See task statistics

### 📅 Planning Page

**Generate AI-Powered Schedules:**
1. Select start and end dates/times
2. Provide optional context (e.g., "Focus on urgent items")
3. Click "Generate Plan"

**Work with Plans:**
- View AI reasoning and suggestions
- See scheduled tasks with time slots
- Execute plan (add to calendar)
- Refine plan based on feedback

### 📊 Insights Page

View productivity analytics:
- Total tasks and completion rate
- Task distribution by priority and status
- Average task duration
- AI-powered recommendations

## Configuration Details

### Environment Variables

The app automatically creates a `.env` file with your settings:

```env
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Model Configuration
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
TEMPERATURE=0.7

# Database
DATABASE_URL=sqlite:///./ai_agent.db

# Optional: Calendar Integration
# GOOGLE_CALENDAR_CREDENTIALS=credentials.json
# GOOGLE_CALENDAR_TOKEN=token.json
# MICROSOFT_CLIENT_ID=your_client_id
# MICROSOFT_CLIENT_SECRET=your_client_secret
# MICROSOFT_TENANT_ID=your_tenant_id

# Agent Settings
DEFAULT_TIMEZONE=UTC
MONITORING_INTERVAL_MINUTES=15
LEARNING_MODE=enabled
```

### Calendar Integration (Optional)

To enable Google Calendar or Outlook integration:

**Google Calendar:**
1. Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
2. Download `credentials.json` to project root
3. The app will handle OAuth flow automatically

**Microsoft Outlook:**
1. Register app in [Azure Portal](https://portal.azure.com/)
2. Add client ID, secret, and tenant ID to `.env`

### User Profiles

Each user ID gets its own profile with:
- Working hours and preferences
- Task history and learning data
- Calendar integrations
- Custom settings

To use multiple profiles, just change the User ID in the configuration.

## Troubleshooting

### "Failed to initialize agent"

**Possible causes:**
- Invalid API key → Check your Anthropic API key
- Missing dependencies → Run `pip install -r requirements.txt`
- Database issues → Delete `ai_agent.db` and restart

### "Error generating plan"

**Possible causes:**
- No tasks added → Add tasks before generating plans
- Invalid date range → Ensure end date is after start date
- API issues → Check your internet connection and API key

### Packages not installed warnings

Run the installation command:
```bash
pip install -r requirements.txt
```

### Port already in use

If port 8501 is busy, specify a different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

## Advanced Usage

### Running on a Custom Port

```bash
streamlit run streamlit_app.py --server.port 8080
```

### Running on Network

To access from other devices on your network:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### Headless Mode

For server deployment without auto-opening browser:

```bash
streamlit run streamlit_app.py --server.headless true
```

## Architecture

The Streamlit UI is a presentation layer that:
- Uses `AITaskPlanningAgent` from `agent.py`
- Stores configuration in `.env` via `config/settings.py`
- Manages state using Streamlit's session state
- Provides 4 main pages: Chat, Tasks, Planning, Insights

**Data Flow:**
```
User Input → Streamlit UI → AITaskPlanningAgent → Services (AI/Calendar/DB) → Response
```

## Tips for Best Experience

1. **Start with Tasks**: Add several tasks before generating plans
2. **Use Chat**: The chat interface is great for quick interactions
3. **Provide Context**: When generating plans, add context for better results
4. **Review Insights**: Check the insights page to optimize productivity
5. **Refine Plans**: Don't hesitate to refine plans with feedback

## Security Notes

- API keys are stored in `.env` (git-ignored)
- Never commit `.env` to version control
- Use environment variables in production
- Secure your `credentials.json` and `token.json` files

## Support

For issues or questions:
1. Check this README
2. Review error messages in the UI
3. Check the main project documentation
4. Examine logs in the terminal running Streamlit

## Development

To modify the UI:

1. Edit `streamlit_app.py`
2. Streamlit auto-reloads on file changes
3. Test changes in browser
4. Use `st.write()` for debugging

**Adding new pages:**
- Add new radio option in sidebar navigation
- Create corresponding `elif page == "New Page"` section
- Implement page logic

## License

Same as the main AI Task Planning Agent project.

---

**Enjoy your AI-powered productivity assistant!** 🤖
