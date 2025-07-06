"""
Email body utilities for cleaning and processing email content.
"""

import re
import unicodedata
from html2text import html2text


class EmailBodyUtils:
    """Utility class for cleaning and processing email body content."""

    @staticmethod
    def to_text(body: str) -> str:
        """
        Clean and strip email body text.

        Args:
            body: Raw email body text

        Returns:
            Cleaned body text without whitespace and newlines
        """
        if not body:
            return body

        body = html2text(body)
        body = EmailBodyUtils.strip(body)

        return body

    @staticmethod
    def strip(body: str) -> str:
        """
        Strip whitespace and newlines from email body.

        Args:
            body: Raw email body text

        Returns:
            Cleaned body text without whitespace and newlines
        """
        if not body:
            return body

        # Remove invisible Unicode characters (zero-width spaces, etc.)
        body = "".join(
            char
            for char in body
            if unicodedata.category(char)[0] != "C" or char in "\n\r\t"
        )

        # Remove extra whitespace and newlines
        body = " ".join(body.split())

        # Remove extra whitespace
        body = re.sub(r"\s+", " ", body).strip()

        return body
