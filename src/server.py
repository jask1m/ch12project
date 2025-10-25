#!/usr/bin/env python3
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

mcp = FastMCP("Wingman MCP")

# store user's "crush state" in memory
user_sessions = {}

def research_crush_with_perplexity(crush_name: str) -> str:
    """Research a person using Perplexity AI."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key or api_key == "your_perplexity_api_key_here":
        return "Perplexity API key not configured. Please set PERPLEXITY_API_KEY in your environment."
    
    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Create a comprehensive research query
        query = f"""Tell me about {crush_name}. Include any public information about their:
        - Education (school, major, graduation year)
        - Professional background or career
        - Interests and hobbies
        - Social media presence (Instagram, LinkedIn, etc.)
        - Clubs, organizations, or activities they're involved in
        - Any notable achievements or public information
        
        Focus on publicly available information that would help someone understand their interests and background."""
        
        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.2
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        research_result = data["choices"][0]["message"]["content"]
        
        return research_result
        
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Perplexity API: {str(e)}"
    except KeyError as e:
        return f"Error parsing Perplexity API response: {str(e)}"
    except Exception as e:
        return f"Unexpected error during research: {str(e)}"

# Session Management
def get_user_session(user_id: str) -> dict:
    return user_sessions.get(user_id, {})

def set_user_crush(user_id: str, crush_name: str, crush_info: str) -> None:
    user_sessions[user_id] = {
        "crush_name": crush_name,
        "crush_info": crush_info,
        "timestamp": datetime.now().isoformat()
    }

def has_crush_info(user_id: str) -> bool:
    session = get_user_session(user_id)
    return bool(session.get("crush_name") and session.get("crush_info"))

def get_crush_summary(user_id: str) -> str:
    session = get_user_session(user_id)
    if not has_crush_info(user_id):
        return "No crush information stored yet."
    
    crush_name = session.get("crush_name", "Unknown")
    timestamp = session.get("timestamp", "Unknown time")
    return f"Crush: {crush_name} (stored on {timestamp})"

# Wingman MCP Tools
@mcp.tool(description="Set crush information and research them using web search")
def set_crush_info(crush_name: str, additional_context: str = "") -> str:
    user_id = "default_user"
    research_result = research_crush_with_perplexity(crush_name)
    set_user_crush(user_id, crush_name, research_result)
    return f"Got it! I've researched {crush_name} and stored their information. I now know about them and can help you with personalized advice!"

@mcp.tool(description="Get personalized advice about your crush")
def get_crush_advice(question: str) -> str:
    user_id = "default_user"
    
    if not has_crush_info(user_id):
        return "I'd love to help you with your crush! But first, I need to know who they are. Can you tell me about your crush using the set_crush_info tool?"
    
    session = get_user_session(user_id)
    crush_name = session.get("crush_name", "your crush")
    crush_info = session.get("crush_info", "")
    
    advice = f"Based on what I know about {crush_name}, here's my advice for your question: '{question}'\n\n"
    advice += f"Context about {crush_name}: {crush_info[:500]}...\n\n"
    advice += f"Given this information, I'd suggest focusing on their interests and background when approaching them. "
    advice += f"Since I know about {crush_name}'s profile, I can give you more specific advice if you ask about particular situations!"
    
    return advice

@mcp.tool(description="Check if crush information is stored and get summary")
def check_crush_status() -> str:
    user_id = "default_user"
    return get_crush_summary(user_id)

@mcp.tool(description="Greet a user by name with a welcome message from the MCP server")
def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to our sample MCP server running on Heroku!"

@mcp.tool(description="Get information about the MCP server including name, version, environment, and Python version")
def get_server_info() -> dict:
    return {
        "server_name": "Sample MCP Server",
        "version": "1.0.0",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0]
    }

@mcp.tool(description="Test tool: if you say 'jason' I'll respond 'kim'!")
def jason_kim_test(message: str) -> str:
    """A simple test tool to verify the MCP server is working."""
    if "jason" in message.lower():
        return "kim! 🎉"
    else:
        return f"You said '{message}', but I only respond to 'jason'!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting FastMCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
