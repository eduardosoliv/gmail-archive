"""
Table formatter for displaying Gmail emails in CLI.
"""

import email.utils
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class EmailTableFormatter:  # pylint: disable=too-few-public-methods
    """Formatter for displaying emails in a rich CLI table."""

    def __init__(self):
        """Initialize the formatter with a console."""
        self.console = Console()

    def display_emails(
        self, emails: List[Dict], max_results: int = 50
    ) -> None:
        """
        Display emails in a formatted table.

        Args:
            emails: List of email dictionaries
            max_results: Maximum number of emails to display
        """
        if not emails:
            self.console.print(
                Panel(
                    "No unread emails found! 📭",
                    style="blue",
                    border_style="blue",
                )
            )
            return

        # Create the table
        table = Table(
            title="📧 Unread Gmail Messages",
            show_header=True,
            header_style="bold magenta",
            border_style="blue",
            title_style="bold cyan",
        )

        # Add columns
        table.add_column("From", style="cyan", width=30, no_wrap=True)
        table.add_column("Subject", style="white", width=50, no_wrap=False)
        table.add_column("Date", style="green", width=20, no_wrap=True)

        # Add rows
        for _email in emails:
            from_text = self._format_sender(_email.get("from", ""))
            subject_text = self._format_subject(_email.get("subject", ""))
            date_text = self._format_date(_email.get("date", ""))

            table.add_row(from_text, subject_text, date_text)
            # Don't add empty row after the last email
            if _email != emails[-1]:
                table.add_row("", "", "")

        # Display the table
        self.console.print(table)

        # Show summary
        count = len(emails)
        if count < max_results:
            self.console.print(
                f"\n[bold green]Found {count} unread email(s)[/bold green]"
            )
        else:
            self.console.print(
                f"\n[bold green]Showing {count} unread email(s)[/bold green]"
            )

    def _format_sender(self, sender: str) -> str:
        """
        Format sender email for display.

        Args:
            sender: Raw sender string

        Returns:
            Formatted sender string
        """
        if not sender:
            return "Unknown"

        # Extract name from "Name <email@domain.com>" format
        if "<" in sender and ">" in sender:
            name = sender.split("<")[0].strip()
            email_address = sender.split("<")[1].split(">")[0].strip()
            if name:
                return f"{name}\n[dim]{email_address}[/dim]"
            return email_address

        return sender

    def _format_subject(self, subject: str) -> str:
        """
        Format subject line for display.

        Args:
            subject: Raw subject string

        Returns:
            Formatted subject string
        """
        if not subject:
            return "[dim](No subject)[/dim]"

        # Truncate long subjects
        if len(subject) > 85:
            return subject[:82] + "..."

        return subject

    def _format_date(self, date_string: str) -> str:
        """
        Format email date for display.

        Args:
            date_string: Raw date string from email

        Returns:
            Formatted date string or original string if parsing fails
        """
        try:
            parsed_date = email.utils.parsedate_to_datetime(date_string)
            return parsed_date.strftime("%Y-%m-%d %H:%M")
        except Exception:
            print(f"Error parsing date: {date_string}")
            return date_string
