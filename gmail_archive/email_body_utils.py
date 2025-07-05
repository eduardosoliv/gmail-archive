"""
Email body utilities for cleaning and processing email content.
"""

import re


class EmailBodyUtils:
    """Utility class for cleaning and processing email body content."""

    @staticmethod
    def clean_strip(body: str) -> str:
        """
        Clean and strip email body text.

        Args:
            body: Raw email body text

        Returns:
            Cleaned body text without whitespace and newlines
        """
        if not body:
            return body

        body = EmailBodyUtils.clean_html(body)
        body = EmailBodyUtils.clean_css(body)
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

        # Remove extra whitespace and newlines
        body = " ".join(body.split())

        # Remove extra whitespace
        body = re.sub(r"\s+", " ", body).strip()

        return body

    @staticmethod
    def clean_html(body: str) -> str:
        """
        Remove HTML tags from email body.

        Args:
            body: Raw email body text

        Returns:
            Cleaned body text without HTML tags
        """
        if not body:
            return body

        # Remove HTML tags
        body = re.sub(r"<[^>]+>", "", body)

        # Remove extra whitespace
        body = re.sub(r"\s+", " ", body).strip()

        return body

    @staticmethod
    def clean_css(body: str) -> str:
        """
        Remove CSS content from email body.

        Args:
            body: Raw email body text

        Returns:
            Cleaned body text without CSS content
        """
        if not body:
            return body

        # Remove CSS blocks (between <style> tags)
        body = re.sub(
            r"<style[^>]*>.*?</style>",
            "",
            body,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove @import statements
        body = re.sub(r"@import[^;]*;", "", body, flags=re.IGNORECASE)

        # Remove CSS comments
        body = re.sub(r"/\*.*?\*/", "", body, flags=re.DOTALL)

        # Remove CSS rules with braces - more comprehensive pattern
        body = re.sub(r"[a-zA-Z#\.][a-zA-Z0-9\-_\.\s]*\s*\{[^}]*\}", "", body)

        # Remove CSS selectors and properties that might remain
        css_patterns = [
            r"font-family\s*:\s*[^;]+;",
            r"color\s*:\s*[^;]+;",
            r"background-color\s*:\s*[^;]+;",
            r"background\s*:\s*[^;]+;",
            r"padding\s*:\s*[^;]+;",
            r"margin\s*:\s*[^;]+;",
            r"border\s*:\s*[^;]+;",
            r"width\s*:\s*[^;]+;",
            r"height\s*:\s*[^;]+;",
            r"display\s*:\s*[^;]+;",
            r"position\s*:\s*[^;]+;",
            r"float\s*:\s*[^;]+;",
            r"clear\s*:\s*[^;]+;",
            r"overflow\s*:\s*[^;]+;",
            r"text-align\s*:\s*[^;]+;",
            r"line-height\s*:\s*[^;]+;",
            r"font-size\s*:\s*[^;]+;",
            r"font-weight\s*:\s*[^;]+;",
            r"text-decoration\s*:\s*[^;]+;",
            r"!important;",
            # Add more CSS properties
            r"outline\s*:\s*[^;]+;",
            r"border-collapse\s*:\s*[^;]+;",
            r"table-layout\s*:\s*[^;]+;",
            r"overflow-wrap\s*:\s*[^;]+;",
            r"word-wrap\s*:\s*[^;]+;",
            r"word-break\s*:\s*[^;]+;",
            r"-webkit-text-size-adjust\s*:\s*[^;]+;",
            r"-ms-word-break\s*:\s*[^;]+;",
            r"src\s*:\s*[^;]+;",
            r"format\s*:\s*[^;]+;",
            r"font-style\s*:\s*[^;]+;",
        ]

        for pattern in css_patterns:
            body = re.sub(pattern, "", body, flags=re.IGNORECASE)

        # Remove incomplete CSS properties (without semicolons)
        incomplete_css = [
            r"line-height\s*:\s*[^;]*$",
            r"background\s*:\s*[^;]*$",
            r"border\s*:\s*[^;]*$",
            r"width\s*:\s*[^;]*$",
            r"height\s*:\s*[^;]*$",
            r"display\s*:\s*[^;]*$",
            r"position\s*:\s*[^;]*$",
            r"float\s*:\s*[^;]*$",
            r"clear\s*:\s*[^;]*$",
            r"overflow\s*:\s*[^;]*$",
            r"text-align\s*:\s*[^;]*$",
            r"font-size\s*:\s*[^;]*$",
            r"font-weight\s*:\s*[^;]*$",
            r"text-decoration\s*:\s*[^;]*$",
            r"outline\s*:\s*[^;]*$",
            r"border-collapse\s*:\s*[^;]*$",
            r"table-layout\s*:\s*[^;]*$",
            r"overflow-wrap\s*:\s*[^;]*$",
            r"word-wrap\s*:\s*[^;]*$",
            r"word-break\s*:\s*[^;]*$",
            r"-webkit-text-size-adjust\s*:\s*[^;]*$",
            r"-ms-word-break\s*:\s*[^;]*$",
            r"src\s*:\s*[^;]*$",
            r"format\s*:\s*[^;]*$",
            r"font-style\s*:\s*[^;]*$",
        ]

        for pattern in incomplete_css:
            body = re.sub(pattern, "", body, flags=re.IGNORECASE)

        # Remove any remaining CSS-like patterns
        body = re.sub(r"[a-zA-Z\-]+\s*:\s*[^;]+;", "", body)

        # Remove extra whitespace
        body = re.sub(r"\s+", " ", body).strip()

        return body
