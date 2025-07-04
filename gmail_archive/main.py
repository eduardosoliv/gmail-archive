"""
Main CLI entry point for Gmail CLI application.
"""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from .gmail_client import GmailClient
from .email_table_formatter import EmailTableFormatter
from .message_utils import MessageUtils


@click.command()
@click.option(
    "--max-results",
    "-m",
    default=50,
    help="Maximum number of emails to retrieve (default: 50)",
)
@click.option(
    "--credentials",
    "-c",
    default="credentials.json",
    help="Path to OAuth credentials file (default: credentials.json)",
)
@click.option(
    "--token",
    "-t",
    default="token.json",
    help="Path to OAuth token file (default: token.json)",
)
@click.version_option(version="0.1.0", prog_name="gmail-cli")
def main(max_results: int, credentials: str, token: str):
    """
    Gmail Archive CLI - A CLI tool to access Gmail and
    suggests unread emails that can be archived.

    This tool requires Gmail API credentials.
    Follow the setup instructions in the README to
    configure OAuth 2.0 credentials.
    """
    console = Console()
    formatter = EmailTableFormatter()
    message_utils = MessageUtils()

    console.print(
        Panel(
            "[bold cyan]Gmail Archive CLI[/bold cyan]\n"
            "Access Gmail and suggests unread emails that can be archived.",
            style="blue",
            border_style="blue",
        )
    )

    try:
        gmail_client = GmailClient(credentials, token)
        if not gmail_client.authenticate():
            message_utils.error(
                "Authentication failed! Please check your credentials file."
            )
            sys.exit(1)

        message_utils.success("Successfully authenticated with Gmail!")

        emails = gmail_client.get_unread_emails(max_results)
        formatter.display_emails(emails, max_results)
    except Exception as e:
        message_utils.error(f"An unexpected error occurred: {str(e)}")
        console.print(f"\n[dim]Error details: {type(e).__name__}: {e}[/dim]")
        sys.exit(1)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
