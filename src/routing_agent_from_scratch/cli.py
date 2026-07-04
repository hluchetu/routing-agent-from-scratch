from __future__ import annotations

import argparse
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from sophons.agents.hooks import AfterModelCall

from .main import run
from .routes import Route

console = Console()

_PROMPT_STYLE = Style.from_dict({"prompt": "bold #5f87ff"})
_HISTORY_FILE = Path.home() / ".routing_agent_history"

_ROUTE_COLORS = {
    "research": "#f97316",
    "math": "#a78bfa",
    "general": "#2dba4e",
}


def _print_header(thinking: bool) -> None:
    suffix = "  [dim cyan]--thinking[/dim cyan]" if thinking else ""
    console.print()
    console.print(
        Panel.fit(
            f"[bold white]Routing Agent[/bold white]  [dim]deepseek-chat → deepseek-reasoner[/dim]{suffix}\n"
            "[dim]Type your question and press Enter. [bold]exit[/bold] or Ctrl+C to quit.[/dim]",
            border_style="bright_black",
            padding=(0, 2),
        )
    )
    console.print()


def _print_user(text: str) -> None:
    console.print(Panel(
        Text(text, style="white"),
        title="[bold #5f87ff]You[/bold #5f87ff]",
        border_style="#5f87ff",
        padding=(0, 1),
    ))


def _print_route(route: Route) -> None:
    color = _ROUTE_COLORS.get(route.name, "#2dba4e")
    console.print(f"\n  [dim]→ route:[/dim] [bold {color}]{route.name}[/bold {color}]\n")


def _print_response(text: str, route: Route) -> None:
    color = _ROUTE_COLORS.get(route.name, "#2dba4e")
    console.print(Panel(
        Markdown(text),
        title=f"[bold {color}]Agent[/bold {color}]",
        subtitle=f"[dim]route={route.name}[/dim]",
        border_style=color,
        padding=(0, 1),
    ))


def _on_after_model(event: AfterModelCall) -> None:
    reasoning = event.message.metadata.get("reasoning")
    if reasoning:
        console.print(Panel(
            reasoning,
            title="[bold magenta]Thinking[/bold magenta]",
            border_style="magenta",
            padding=(0, 1),
        ))


def main() -> None:
    parser = argparse.ArgumentParser(prog="routing-chat", description="Routing agent CLI")
    parser.add_argument("--thinking", action="store_true", help="Show model reasoning")
    args = parser.parse_args()

    _print_header(args.thinking)

    session: PromptSession = PromptSession(
        history=FileHistory(str(_HISTORY_FILE)),
        style=_PROMPT_STYLE,
    )

    while True:
        try:
            user_input = session.prompt("  You › ", style=_PROMPT_STYLE).strip()
        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted.[/dim]")
            break
        except EOFError:
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "/exit", "/quit"}:
            console.print("[dim]Goodbye.[/dim]")
            break

        console.print()
        _print_user(user_input)
        console.print()

        route_ref: list = []

        try:
            with console.status("[dim]Classifying...[/dim]", spinner="dots") as status:
                def on_route_chosen(route: Route) -> None:
                    route_ref.append(route)
                    _print_route(route)
                    status.update("[dim]Running...[/dim]")

                result = run(
                    request=user_input,
                    on_route_chosen=on_route_chosen,
                )

            console.print()
            _print_response(result.response, result.route)
            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]Cancelled.[/dim]\n")
        except Exception as exc:
            console.print(f"\n[bold red]Error:[/bold red] {exc}\n")
