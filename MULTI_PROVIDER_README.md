# Multi-Provider AI Support

The AI Task Planning Agent now supports multiple AI providers, giving you flexibility to choose the AI that best fits your needs and budget.

## Supported Providers

### 1. Anthropic Claude
- **Models**: Claude Sonnet 4.5, Claude Opus 4.5, Claude 3.5 Sonnet
- **Best for**: Complex reasoning, detailed planning, nuanced understanding
- **API Key**: Get from [console.anthropic.com](https://console.anthropic.com/)
- **Pricing**: Pay-per-token (see Anthropic pricing)

### 2. OpenAI ChatGPT
- **Models**: GPT-4o, GPT-4o-mini, GPT-4 Turbo, GPT-3.5 Turbo
- **Best for**: Fast responses, wide knowledge base, cost-effective options
- **API Key**: Get from [platform.openai.com](https://platform.openai.com/)
- **Pricing**: Varies by model (GPT-4o-mini is most economical)

### 3. Google Gemini
- **Models**: Gemini 2.0 Flash Exp, Gemini 1.5 Pro, Gemini 1.5 Flash
- **Best for**: Multimodal capabilities, fast inference, free tier available
- **API Key**: Get from [ai.google.dev](https://ai.google.dev/)
- **Pricing**: Free tier available, then pay-per-use

## Getting Started

### Step 1: Get an API Key

Choose your preferred provider and sign up for an API key:

**Anthropic Claude:**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key

**OpenAI ChatGPT:**
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new secret key

**Google Gemini:**
1. Go to https://ai.google.dev/
2. Click "Get API key in Google AI Studio"
3. Sign in with Google account
4. Create an API key

### Step 2: Configure in Streamlit UI

1. Run the Streamlit app:
   ```bash
   python -m streamlit run streamlit_app.py
   ```

2. In the sidebar configuration:
   - Select your **AI Provider** from the dropdown
   - Enter your **API Key**
   - Choose a **Model** (options update based on provider)
   - Set your **User ID**
   - Click **"Save & Initialize"**

3. The agent is now ready to use with your chosen provider!

### Step 3: Use the Agent

All features work the same regardless of provider:
- Chat with the agent
- Add and manage tasks
- Generate AI-powered plans
- View insights and analytics

## Configuration via Environment Variables

You can also configure the provider manually by editing the `.env` file:

```env
# AI Provider Configuration
AI_PROVIDER=anthropic  # Options: anthropic, openai, google

# API Keys (set the one for your chosen provider)
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# Model Name (provider-specific)
MODEL_NAME=claude-sonnet-4-5-20250929
```

## Programmatic Usage

You can also use different providers programmatically:

```python
from services.ai_planner_multi import AIPlannerService

# Use Anthropic Claude
planner = AIPlannerService(
    provider="anthropic",
    api_key="your_anthropic_key",
    model_name="claude-sonnet-4-5-20250929"
)

# Use OpenAI ChatGPT
planner = AIPlannerService(
    provider="openai",
    api_key="your_openai_key",
    model_name="gpt-4o"
)

# Use Google Gemini
planner = AIPlannerService(
    provider="google",
    api_key="your_google_key",
    model_name="gemini-2.0-flash-exp"
)

# Generate a plan (same interface for all providers)
plan = planner.generate_plan(tasks, calendar_events, user_profile, context)
```

## Model Recommendations

### For Budget-Conscious Users
- **Google Gemini 1.5 Flash**: Free tier, fast, good quality
- **OpenAI GPT-4o-mini**: Very affordable, excellent performance
- **Anthropic Claude 3.5 Sonnet**: Good balance of cost and quality

### For Maximum Quality
- **Anthropic Claude Opus 4.5**: Best reasoning and planning
- **OpenAI GPT-4o**: Strong performance, multimodal
- **Google Gemini 1.5 Pro**: Advanced capabilities

### For Speed
- **Google Gemini 2.0 Flash Exp**: Fastest inference
- **OpenAI GPT-4o-mini**: Quick responses
- **Anthropic Claude Sonnet 4.5**: Good speed-quality balance

## Switching Providers

You can switch between providers at any time:

1. Click **"Reconfigure"** in the Streamlit sidebar
2. Select a different AI provider
3. Enter the new API key
4. Choose a model
5. Click **"Save & Initialize"**

All your tasks, calendar events, and user profile remain intact when switching providers.

## Cost Comparison

| Provider | Model | Cost (Input) | Cost (Output) | Free Tier |
|----------|-------|--------------|---------------|-----------|
| Anthropic | Claude Sonnet 4.5 | $3/1M tokens | $15/1M tokens | No |
| Anthropic | Claude Opus 4.5 | $15/1M tokens | $75/1M tokens | No |
| OpenAI | GPT-4o | $2.50/1M tokens | $10/1M tokens | No |
| OpenAI | GPT-4o-mini | $0.15/1M tokens | $0.60/1M tokens | No |
| Google | Gemini 2.0 Flash | Free tier available | Free tier available | Yes |
| Google | Gemini 1.5 Pro | $1.25/1M tokens | $5/1M tokens | Limited |

*Prices as of December 2025 - check provider websites for current pricing*

## Features by Provider

All providers support the core features:
- ✅ Task planning and scheduling
- ✅ Natural language chat
- ✅ Plan refinement
- ✅ Deviation analysis
- ✅ Conversation history

Provider-specific notes:
- **Claude**: Excellent at detailed reasoning and explanations
- **ChatGPT**: Fast responses, great for quick iterations
- **Gemini**: Multimodal support (can analyze images if added to prompts)

## Troubleshooting

### "Invalid API Key" Error
- Double-check your API key is correct
- Ensure you're using the right key for the selected provider
- Check that your API key has sufficient credits/quota

### "Model Not Found" Error
- Verify the model name is correct for your provider
- Some models may require special access (e.g., GPT-4 access)
- Try a different model from the same provider

### Installation Issues
If you encounter import errors, install the required packages:

```bash
pip install -r requirements.txt
```

This includes:
- `anthropic>=0.39.0` - For Claude
- `openai>=1.0.0` - For ChatGPT
- `google-generativeai>=0.3.0` - For Gemini

## API Rate Limits

Be aware of rate limits for each provider:

- **Anthropic**: 50 requests/minute (tier-dependent)
- **OpenAI**: 500 requests/minute for GPT-4o-mini, 10,000 requests/day
- **Google Gemini**: 60 requests/minute (free tier), higher for paid

The agent will automatically handle rate limit errors when possible.

## Privacy & Security

- API keys are stored locally in `.env` file (git-ignored)
- Keys are never logged or shared
- All API calls are made directly to the provider
- Your task data stays in your local database

## Best Practices

1. **Start with free tier**: Try Google Gemini's free tier first
2. **Use appropriate models**: Don't use expensive models for simple tasks
3. **Monitor costs**: Check your provider dashboard regularly
4. **Secure your keys**: Never commit `.env` to version control
5. **Test different providers**: Each has strengths for different use cases

## Support

For provider-specific issues:
- **Anthropic Claude**: https://support.anthropic.com/
- **OpenAI ChatGPT**: https://help.openai.com/
- **Google Gemini**: https://ai.google.dev/support

For agent-specific issues, check the main project README or open an issue.

---

**Enjoy the flexibility of multi-provider AI support!** 🚀
