# Wingman MCP

A stateful [FastMCP](https://github.com/jlowin/fastmcp) server that acts as your
personal wingman, helping you with crush-related advice by maintaining context
and performing web research.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/InteractionCo/mcp-server-template)

## Features

- **Stateful Memory**: Remembers who your crush is across conversations
- **Smart Clarification**: Asks who your crush is if not yet specified
- **Web Research**: Performs initial research on your crush using Perplexity AI
- **Personalized Advice**: Provides tailored advice based on your crush's
  profile
- **Multi-User Support**: Architecture supports multiple users with separate
  contexts

## Wingman Tools

### 1. `set_crush_info(crush_name, school, major, additional_context="")`

- Store crush information (name, school, major) and perform initial web research
- Uses Perplexity AI to gather public information about your crush with targeted
  school/major context
- Returns confirmation with research summary

### 2. `get_crush_advice(question)`

- Get personalized advice about your crush
- If no crush info exists: asks for clarification with name, school, and major
- If crush info exists: provides advice based on stored research

### 3. `check_crush_status()`

- Check current status of stored crush information
- Returns summary of crush info or "No crush information stored yet"

## Local Development

### Setup

Fork the repo, then run:

```bash
git clone <your-repo-url>
cd wingman-mcp
conda create -n mcp-server python=3.13
conda activate mcp-server
pip install -r requirements.txt
```

### Configure Perplexity API

1. Get your API key from
   [Perplexity AI Settings](https://www.perplexity.ai/settings/api)
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   PERPLEXITY_API_KEY=your_actual_api_key_here
   ```

### Test

```bash
python src/server.py
# then in another terminal run:
npx @modelcontextprotocol/inspector
```

Open http://localhost:3000 and connect to `http://localhost:8000/mcp` using
"Streamable HTTP" transport (NOTE THE `/mcp`!).

### Test Wingman Features

1. **Test sanity check**: Use the `jason_kim_test` tool with "jason" to verify
   server is working
2. **Test crush setup**: Use `set_crush_info` with crush name, school, and major
   to test research functionality
3. **Test advice**: Use `get_crush_advice` to test personalized advice
4. **Test status**: Use `check_crush_status` to verify stateful memory

## Deployment

### Option 1: One-Click Deploy

Click the "Deploy to Render" button above.

### Option 2: Manual Deployment

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect your forked repository
5. Render will automatically detect the `render.yaml` configuration

Your server will be available at `https://your-service-name.onrender.com/mcp`
(NOTE THE `/mcp`!)

## Poke Integration

### Setup

1. Deploy your server to Render (see Deployment section)
2. Go to [poke.com/settings/connections](https://poke.com/settings/connections)
3. Add your deployed server URL: `https://your-service-name.onrender.com/mcp`
4. Name the connection "Wingman MCP"

### Usage

Once connected, you can ask Poke questions like:

- "How do I impress my crush today?"
- "What should I talk to my crush about?"
- "Give me advice about my crush"

The Wingman MCP will:

1. **First time**: Ask who your crush is if not specified
2. **After setup**: Provide personalized advice based on research
3. **Remember context**: Maintain crush information across conversations

### Testing Connection

To test the connection explicitly, ask Poke:

```
Tell the subagent to use the "Wingman MCP" integration's "check_crush_status" tool
```

If you run into persistent issues, send `clearhistory` to Poke to delete message
history and start fresh.

## Architecture

### Stateful Session Management

The server maintains user sessions in memory:

```python
user_sessions = {
    "default_user": {
        "crush_name": "Sarah Chen",
        "crush_info": "Sarah is a computer science student...",
        "timestamp": "2024-10-25T10:30:00"
    }
}
```

### Perplexity AI Integration

- **Endpoint**: `https://api.perplexity.ai/chat/completions`
- **Model**: `sonar`
- **Research**: Gathers education, interests, activities, and social media
  presence
- **Error Handling**: Graceful fallback for API issues

### Multi-User Support

The architecture supports multiple users with separate contexts:

- Each user gets their own session data
- Isolated crush information per user
- Scalable to production with database storage

## Customization

Add more wingman features by decorating functions with `@mcp.tool`:

```python
@mcp.tool
def get_conversation_starters(crush_name: str) -> str:
    """Generate conversation starters based on crush's interests."""
    # Your custom wingman logic here
    return "Here are some conversation starters..."
```
