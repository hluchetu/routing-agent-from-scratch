from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Route:
    name: str
    description: str
    system_prompt: str
    has_tools: bool = False


ROUTES: list[Route] = [
    Route(
        name="research",
        description="Current events, recent news, live data, or any question where up-to-date information is needed.",
        system_prompt=(
            "You are a research assistant with access to web search. "
            "Use your tools to find current, accurate information. "
            "Ground every claim in what you retrieve. Be specific: names, dates, numbers."
        ),
        has_tools=True,
    ),
    Route(
        name="math",
        description="Calculations, equations, unit conversions, statistics, or any question that requires precise numerical reasoning.",
        system_prompt=(
            "You are a precise math assistant. "
            "Show your working step by step. "
            "Double-check your arithmetic before answering. "
            "Use exact values where possible."
        ),
        has_tools=False,
    ),
    Route(
        name="general",
        description="Explanations, concepts, opinions, writing, or any question that does not require live data or calculation.",
        system_prompt=(
            "You are a helpful assistant. "
            "Answer clearly and concisely. "
            "If you are uncertain about something, say so."
        ),
        has_tools=False,
    ),
]

FALLBACK_ROUTE = ROUTES[-1]
