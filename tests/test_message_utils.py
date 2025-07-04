# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
from unittest.mock import patch, MagicMock
from gmail_archive.message_utils import MessageUtils


class TestMessageUtils:
    def test_init(self):
        message_utils = MessageUtils()
        assert hasattr(message_utils, "console")
        assert message_utils.console is not None

    @patch("gmail_archive.message_utils.Console")
    def test_error_message(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        message_utils.error("Test error message")

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == "❌ Test error message"
        assert panel.style == "red"
        assert panel.border_style == "red"

    @patch("gmail_archive.message_utils.Console")
    def test_success_message(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        message_utils.success("Test success message")

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == "✅ Test success message"
        assert panel.style == "green"
        assert panel.border_style == "green"

    @patch("gmail_archive.message_utils.Console")
    def test_info_message(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        message_utils.info("Test info message")

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == "ℹ️  Test info message"
        assert panel.style == "blue"
        assert panel.border_style == "blue"

    @patch("gmail_archive.message_utils.Console")
    def test_error_message_empty_string(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        message_utils.error("")

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == "❌ "
        assert panel.style == "red"
        assert panel.border_style == "red"

    @patch("gmail_archive.message_utils.Console")
    def test_success_message_empty_string(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        message_utils.success("")

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == "✅ "
        assert panel.style == "green"
        assert panel.border_style == "green"

    @patch("gmail_archive.message_utils.Console")
    def test_info_message_empty_string(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        message_utils.info("")

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == "ℹ️  "
        assert panel.style == "blue"
        assert panel.border_style == "blue"

    @patch("gmail_archive.message_utils.Console")
    def test_error_message_special_characters(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        message_utils.error("Error with special chars: !@#$%^&*()")

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == "❌ Error with special chars: !@#$%^&*()"
        assert panel.style == "red"
        assert panel.border_style == "red"

    @patch("gmail_archive.message_utils.Console")
    def test_success_message_long_text(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        # pylint: disable=line-too-long
        long_message = "This is a very long success message that contains multiple words and should be displayed properly in the panel without any issues or truncation"
        message_utils = MessageUtils()
        message_utils.success(long_message)

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == f"✅ {long_message}"
        assert panel.style == "green"
        assert panel.border_style == "green"

    @patch("gmail_archive.message_utils.Console")
    def test_info_message_multiline(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        multiline_message = "Line 1\nLine 2\nLine 3"
        message_utils = MessageUtils()
        message_utils.info(multiline_message)

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == f"ℹ️  {multiline_message}"
        assert panel.style == "blue"
        assert panel.border_style == "blue"

    @patch("gmail_archive.message_utils.Console")
    def test_multiple_message_calls(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()

        # Call all three message types
        message_utils.error("Error message")
        message_utils.success("Success message")
        message_utils.info("Info message")

        # Verify console.print was called three times
        assert mock_console.print.call_count == 3

        # Check each call
        calls = mock_console.print.call_args_list

        # Error call
        error_panel = calls[0][0][0]
        assert error_panel.renderable == "❌ Error message"
        assert error_panel.style == "red"

        # Success call
        success_panel = calls[1][0][0]
        assert success_panel.renderable == "✅ Success message"
        assert success_panel.style == "green"

        # Info call
        info_panel = calls[2][0][0]
        assert info_panel.renderable == "ℹ️  Info message"
        assert info_panel.style == "blue"

    @patch("gmail_archive.message_utils.Console")
    def test_message_with_unicode(self, mock_console_class):
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console

        message_utils = MessageUtils()
        unicode_message = "Mensagem com acentos: áéíóú çãõ"
        message_utils.info(unicode_message)

        # Verify console.print was called once
        mock_console.print.assert_called_once()

        # Get the Panel that was passed to console.print
        panel = mock_console.print.call_args[0][0]

        # Check that it's a Panel with correct content and styling
        assert hasattr(panel, "renderable")
        assert panel.renderable == f"ℹ️  {unicode_message}"
        assert panel.style == "blue"
        assert panel.border_style == "blue"
