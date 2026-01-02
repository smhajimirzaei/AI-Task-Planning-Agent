# AI Task Planning Agent - Documentation

Complete documentation for the AI Task Planning Agent.

## Quick Navigation

### 🚀 Getting Started
Start here if you're new to the agent:
- **[Quick Start Guide](../QUICKSTART.md)** - Get up and running in 5 minutes
- **[Complete Features](FEATURES.md)** - Overview of all capabilities

### 📖 User Guides

#### Streamlit Web Interface (Recommended)
- **[Streamlit UI Guide](STREAMLIT_UI_GUIDE.md)** - Complete guide to using the web interface
  - Configuration and setup
  - All 5 pages explained (Chat, Tasks, Schedule, Planning, Insights)
  - Tips, best practices, and troubleshooting

#### Core Features
- **[Conversational Calendar](CONVERSATIONAL_CALENDAR_README.md)** - Share your schedule through text
  - No calendar API integration required
  - Weekly review system
  - Privacy-first approach

- **[Multi-Provider AI Setup](MULTI_PROVIDER_README.md)** - Choose your AI provider
  - Anthropic Claude setup
  - OpenAI ChatGPT setup
  - Google Gemini setup
  - Switching providers

#### Command Line Interface
- **[CLI Usage Guide](USAGE_GUIDE.md)** - Complete command-line documentation
  - All CLI commands
  - Python API usage
  - Advanced features

### 🔧 For Developers
- **[Contributing Guidelines](../CONTRIBUTING.md)** - How to contribute to the project
- **[Security Policy](../SECURITY.md)** - Security and vulnerability reporting
- **[Example Usage](../example_usage.py)** - Working code examples

## Documentation Structure

```
docs/
├── README.md                           # This file - documentation index
├── STREAMLIT_UI_GUIDE.md              # Complete Streamlit UI guide
├── CONVERSATIONAL_CALENDAR_README.md  # Calendar and scheduling guide
├── MULTI_PROVIDER_README.md           # AI provider setup guide
├── USAGE_GUIDE.md                     # CLI and Python API guide
└── FEATURES.md                        # Complete feature list

Root directory:
├── README.md                          # Main project documentation
├── QUICKSTART.md                      # 5-minute getting started guide
├── CONTRIBUTING.md                    # Contribution guidelines
├── SECURITY.md                        # Security policy
└── .env.example                       # Configuration template
```

## Common Questions

### How do I get started?
See the [Quick Start Guide](../QUICKSTART.md) - you can be up and running in 5 minutes.

### Which AI provider should I use?
- **Anthropic Claude**: Best for complex reasoning and detailed planning
- **OpenAI ChatGPT**: Fast, reliable, great performance
- **Google Gemini**: Free tier available!

See [Multi-Provider Setup](MULTI_PROVIDER_README.md) for details.

### Do I need calendar API credentials?
No! The agent now uses a **conversational calendar** approach. Just share your schedule through text. See [Conversational Calendar](CONVERSATIONAL_CALENDAR_README.md).

### Should I use the web UI or CLI?
**Streamlit Web UI** (recommended) - Easiest to use, visual interface, great for most users.

**Command Line** - For developers, automation, or if you prefer terminal interfaces.

Both have full feature parity. See [Streamlit UI Guide](STREAMLIT_UI_GUIDE.md) or [CLI Guide](USAGE_GUIDE.md).

### How does the agent learn?
Through **weekly reviews**! Tell the agent what actually happened vs what was planned. The AI learns your patterns and improves future plans. See [Conversational Calendar Guide](CONVERSATIONAL_CALENDAR_README.md#weekly-reviews).

### Can I switch AI providers?
Yes! Switch anytime without losing data. All your tasks, schedule, and learning persist. See [Multi-Provider Setup](MULTI_PROVIDER_README.md).

## Getting Help

**Found a bug?** Open an issue on GitHub following the [bug report template](../.github/ISSUE_TEMPLATE/bug_report.md).

**Have a feature request?** Open an issue using the [feature request template](../.github/ISSUE_TEMPLATE/feature_request.md).

**Want to contribute?** Check out the [Contributing Guidelines](../CONTRIBUTING.md).

**Security concern?** See our [Security Policy](../SECURITY.md).

## Version Information

This documentation is for **AI Task Planning Agent v2.0** which includes:
- ✅ Streamlit Web UI
- ✅ Multi-provider AI support (Claude, ChatGPT, Gemini)
- ✅ Conversational calendar (no API integration needed)
- ✅ Weekly review and learning system
- ✅ Local-first privacy approach

---

**Happy Planning!** 🎯

[← Back to Main README](../README.md)
