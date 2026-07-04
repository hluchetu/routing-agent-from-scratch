from __future__ import annotations

from sophons.agents.agent import Agent
from sophons.integrations.models.deepseek import DeepSeekModel
from sophons.integrations.tools import tavily_web_search

from .config import settings
from .routes import Route


def dispatch(request: str, route: Route, model: DeepSeekModel) -> str:
    tools = [tavily_web_search(api_key=settings.tavily_api_key)] if route.has_tools else []

    agent = Agent(
        model=model,
        tools=tools,
        system_prompt=route.system_prompt,
    )

    return agent(request).message
