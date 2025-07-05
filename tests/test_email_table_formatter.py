# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from gmail_archive.email_table_formatter import EmailTableFormatter


class TestEmailTableFormatter:
    def test_format_sender(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert (
            formatter._format_sender("Test Sender <test@example.com>")
            == "Test Sender\n[dim]test@example.com[/dim]"
        )
        assert formatter._format_sender("") == "Unknown"

    def test_format_sender_only_email(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert (
            formatter._format_sender("test@example.com") == "test@example.com"
        )

    def test_format_sender_empty_string(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert formatter._format_sender("") == "Unknown"

    def test_format_sender_just_email(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert (
            formatter._format_sender(" <test@example.com>")
            == "test@example.com"
        )

    def test_format_subject(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert formatter._format_subject("Test Subject") == "Test Subject"
        assert formatter._format_subject("A" * 100) == "A" * 77 + "..."
        assert formatter._format_subject("") == "[dim](No subject)[/dim]"

    def test_format_date(self):
        formatter = EmailTableFormatter()
        assert (
            # pylint: disable=protected-access
            formatter._format_date("Mon, 1 Jan 2024 12:00:00 +0000")
            == "01/01/24"
        )

    def test_format_date_today(self):
        formatter = EmailTableFormatter()
        assert (
            # pylint: disable=protected-access
            formatter._format_date(
                datetime.now()
                .replace(hour=17, minute=6)
                .strftime("%a, %d %b %Y %H:%M:%S +0000")
            )
            == "5:06 PM"
        )

    def test_format_date_yesterday(self):
        formatter = EmailTableFormatter()
        yesterday = datetime.now() - timedelta(days=1)
        assert (
            # pylint: disable=protected-access
            formatter._format_date(
                yesterday.strftime("%a, %d %b %Y %H:%M:%S +0000")
            )
            == yesterday.strftime("%b %-d")
        )

    def test_format_date_invalid(self):
        formatter = EmailTableFormatter()
        assert (
            # pylint: disable=protected-access
            formatter._format_date("2025-01-01 12:00:05")
            == "2025-01-01 12:00:05"
        )

    def test_format_date_empty_string(self):
        formatter = EmailTableFormatter()
        # pylint: disable=protected-access
        assert formatter._format_date("") == ""

    @patch("gmail_archive.email_table_formatter.Console")
    def test_display_emails_empty_list(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        formatter = EmailTableFormatter()
        formatter.display_emails([])

        # Should call console.print with a Panel for empty emails
        mock_console.print.assert_called_once()
        call_args = mock_console.print.call_args[0][0]

        # Check that it's a Panel with the correct content
        assert hasattr(call_args, "renderable")
        assert call_args.renderable == "No unread emails found! 📭"

    @patch("gmail_archive.email_table_formatter.Console")
    def test_display_emails_single_email(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        formatter = EmailTableFormatter()
        emails = [
            {
                "from": "John Doe <john@example.com>",
                "subject": "Test Email",
                "date": "Mon, 1 Jan 2024 12:00:00 +0000",
            }
        ]
        formatter.display_emails(emails)

        # Should call console.print twice: once for table, once for summary
        assert mock_console.print.call_count == 2

        # Check first call (table)
        table_call = mock_console.print.call_args_list[0][0][0]
        assert hasattr(table_call, "title")
        assert table_call.title == "📧 Unread Gmail Messages"

        # Check second call (summary)
        summary_call = mock_console.print.call_args_list[1][0][0]
        assert "Found 1 unread email(s)" in str(summary_call)

    @patch("gmail_archive.email_table_formatter.Console")
    def test_display_emails_multiple_emails(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        formatter = EmailTableFormatter()
        emails = [
            {
                "from": "John Doe <john@example.com>",
                "subject": "First Email",
                "date": "Mon, 1 Jan 2024 12:00:00 +0000",
            },
            {
                "from": "Jane Smith <jane@example.com>",
                "subject": "Second Email",
                "date": "Mon, 1 Jan 2024 13:00:00 +0000",
            },
        ]
        formatter.display_emails(emails)

        # Should call console.print twice: once for table, once for summary
        assert mock_console.print.call_count == 2

        # Check first call (table)
        table_call = mock_console.print.call_args_list[0][0][0]
        assert hasattr(table_call, "title")
        assert table_call.title == "📧 Unread Gmail Messages"

        # Check second call (summary)
        summary_call = mock_console.print.call_args_list[1][0][0]
        assert "Found 2 unread email(s)" in str(summary_call)

    @patch("gmail_archive.email_table_formatter.Console")
    def test_display_emails_with_max_results(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        formatter = EmailTableFormatter()
        emails = [
            {
                "from": "John Doe <john@example.com>",
                "subject": "Test Email",
                "date": "Mon, 1 Jan 2024 12:00:00 +0000",
            }
        ]
        # Set max_results to 1, but we have 1 email (equal to max)
        formatter.display_emails(emails, max_results=1)

        # Should call console.print twice: once for table, once for summary
        assert mock_console.print.call_count == 2

        # Check summary message for max_results case
        summary_call = mock_console.print.call_args_list[1][0][0]
        assert "Showing 1 unread email(s)" in str(summary_call)

    @patch("gmail_archive.email_table_formatter.Console")
    def test_display_emails_table_structure(self, mock_console_class):
        """Test that the table has the correct structure and columns."""
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        formatter = EmailTableFormatter()
        emails = [
            {
                "from": "John Doe <john@example.com>",
                "subject": "Test Email",
                "date": "Mon, 1 Jan 2024 12:00:00 +0000",
            }
        ]
        formatter.display_emails(emails)

        # Check table structure
        table_call = mock_console.print.call_args_list[0][0][0]
        assert hasattr(table_call, "columns")

        # Check that table has 3 columns: From, Subject, Date
        column_names = [col.header for col in table_call.columns]
        assert column_names == ["From", "Subject", "Body", "Date"]

        # Check column styles
        assert table_call.columns[0].style == "cyan"
        assert table_call.columns[1].style == "white"
        assert table_call.columns[2].style == "grey50"
        assert table_call.columns[3].style == "green"
