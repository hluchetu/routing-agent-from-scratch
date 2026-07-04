from __future__ import annotations

from dataclasses import dataclass

from sophons.integrations.models.deepseek import DeepSeekModel

from .config import settings
from .dispatch import dispatch
from .router import classify
from .routes import Route


@dataclass
class RoutingResult:
    request: str
    route: Route
    response: str


def run(request: str, on_route_chosen=None) -> RoutingResult:
    classifier_model = DeepSeekModel(
        model="deepseek-chat",
        api_key=settings.deepseek_api_key,
    )

    route = classify(request, classifier_model)

    if callable(on_route_chosen):
        on_route_chosen(route)

    executor_model = DeepSeekModel(
        model="deepseek-reasoner",
        api_key=settings.deepseek_api_key,
        thinking=True,
    )

    response = dispatch(request, route, executor_model)

    return RoutingResult(request=request, route=route, response=response)
