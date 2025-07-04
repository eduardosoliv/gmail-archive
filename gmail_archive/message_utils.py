"""
Message display utilities for CLI applications.
"""

from rich.console import Console
from rich.panel import Panel


class MessageUtils:
    """Utility class for displaying formatted messages in CLI."""

    def __init__(self):
        """Initialize the message utils with a console."""
        self.console = Console()

    def error(self, message: str) -> None:
        """
        Display an error message.

        Args:
            message: Error message to display
        """
        self.console.print(
            Panel(f"❌ {message}", style="red", border_style="red")
        )

    def success(self, message: str) -> None:
        """
        Display a success message.

        Args:
            message: Success message to display
        """
        self.console.print(
            Panel(f"✅ {message}", style="green", border_style="green")
        )

    def info(self, message: str) -> None:
        """
        Display an info message.

        Args:
            message: Info message to display
        """
        self.console.print(
            Panel(f"ℹ️  {message}", style="blue", border_style="blue")
        )
