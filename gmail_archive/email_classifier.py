"""
Email classifier using OpenAI API to categorize emails.
"""

import os
from typing import Dict
from openai import OpenAI
from .message_utils import MessageUtils


class EmailClassifier:
    """Classifier for categorizing emails using OpenAI API."""

    def __init__(self):
        """Initialize the email classifier."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.message_utils = MessageUtils()

        if not self.api_key:
            raise ValueError(
                "\nOpenAI API key not found.\n"
                "Please set OPENAI_API_KEY environment variable."
            )

        self.client = OpenAI(api_key=self.api_key)

    def classify_email(self, email: Dict) -> str:
        """
        Classify an email into one of four categories.

        Args:
            data: Dict with 'from', 'subject', 'body'

        Returns:
            'Informational' or
            'Promotional/Marketing' or
            'Personal' or
            'Other' or
            'Unknown'
        """
        try:
            content = f"From: {email.get('from', '')}\n"
            content += f"Subject: {email.get('subject', '')}\n"
            content += (
                # limiting length to avoid sending large payloads
                f"Body: {email.get('body', '')[:5000]}"
            )

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                # pylint: disable=line-too-long
                # flake8: noqa: E501
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an email classifier. Analyze the email content and "
                            "classify it into exactly one of these four categories:\n"
                            "1. Informational - News, updates, notifications.\n"
                            "2. Promotional/Marketing - Sales, offers, newsletters, advertisements, promotional content.\n"
                            "3. Personal - Personal correspondence or work-related correspondence.\n"
                            "4. Other - Anything that doesn't fit the above categories\n"
                            "Respond with only the category name, nothing else."
                        ),
                    },
                    {"role": "user", "content": content},
                ],
                max_tokens=10,
                temperature=0.1,
            )

            classification = (
                response.choices[0].message.content or ""
            ).strip()

            # Validate and normalize the response
            valid_categories = [
                "Informational",
                "Promotional/Marketing",
                "Personal",
                "Other",
            ]
            if classification in valid_categories:
                return classification

            # Try to map common variations
            classification_lower = classification.lower()
            if (
                "informational" in classification_lower
                or "info" in classification_lower
            ):
                return "Informational"

            if (
                "promotional" in classification_lower
                or "marketing" in classification_lower
            ):
                return "Promotional/Marketing"

            if (
                "personal" in classification_lower
                or "work" in classification_lower
                or "correspondence" in classification_lower
            ):
                return "Personal"

            return "Other"

        except Exception as e:
            self.message_utils.info(f"Failed to classify email: {str(e)}")
            return "Unknown"

    def classify_emails(self, emails: list) -> list:
        """
        Classify a list of emails.

        Args:
            emails: List of email dictionaries

        Returns:
            List of email dictionaries with added 'classification' key
        """
        if not emails:
            return emails

        self.message_utils.info(
            f"Classifying {len(emails)} emails using OpenAI!"
        )

        classified_emails = []
        for email in emails:
            classification = self.classify_email(email)
            email_with_classification = email.copy()
            email_with_classification["classification"] = classification
            classified_emails.append(email_with_classification)

        self.message_utils.success(
            f"Successfully classified {len(emails)} emails!"
        )
        return classified_emails
