from __future__ import annotations

from sophons.integrations.models.deepseek import DeepSeekModel
from sophons.models.messages import Message

from .routes import FALLBACK_ROUTE, ROUTES, Route


def _build_prompt(request: str) -> str:
    route_list = "\n".join(f"- {r.name}: {r.description}" for r in ROUTES)
    return (
        f"You are a request classifier. Given a user request, choose the most appropriate route.\n\n"
        f"Available routes:\n{route_list}\n\n"
        f"User request: {request}\n\n"
        f"Reply with only the route name — one word, nothing else."
    )


def classify(request: str, model: DeepSeekModel) -> Route:
    messages = [Message(role="user", content=_build_prompt(request))]
    response = model.invoke(messages)
    chosen = response.content.strip().lower()

    for route in ROUTES:
        if route.name == chosen:
            return route

    return FALLBACK_ROUTE
