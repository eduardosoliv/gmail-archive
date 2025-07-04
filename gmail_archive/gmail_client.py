"""
Gmail API client for accessing unread emails.
"""

import os
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailClient:
    """Client for interacting with Gmail API."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(
        self,
        credentials_file: str = "credentials.json",
        token_file: str = "token.json",
    ):
        """
        Initialize Gmail client.

        Args:
            credentials_file: Path to OAuth credentials JSON file
            token_file: Path to store OAuth token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None

    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth 2.0.

        Returns:
            True if authentication successful, False otherwise
        """
        creds = None

        def _load_existing_token() -> Optional[Credentials]:
            if os.path.exists(self.token_file):
                try:
                    return Credentials.from_authorized_user_file(
                        self.token_file, self.SCOPES
                    )
                except Exception as e:
                    print(f"Error loading existing token: {e}")
                    return None
            return None

        creds = _load_existing_token()

        # If no valid credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None

            if not creds:
                if not os.path.exists(self.credentials_file):
                    print(f"Credentials '{self.credentials_file}' not found!")
                    print(
                        "Download your OAuth 2.0 credentials from GCP Console"
                    )
                    print(
                        "and save as 'credentials.json' in the project root."
                    )
                    return False

                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during authentication: {e}")
                    return False

            # Save the credentials for the next run
            try:
                with open(self.token_file, "w", encoding="utf-8") as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Error saving token: {e}")
                return False

        # Build the Gmail service
        try:
            self.service = build("gmail", "v1", credentials=creds)
            return True
        except Exception as e:
            print(f"Error building Gmail service: {e}")
            return False

    def get_unread_emails(self, max_results: int = 50) -> List[Dict]:
        """
        Retrieve unread emails from Gmail.

        Args:
            max_results: Maximum number of emails to retrieve

        Returns:
            List of email dictionaries with 'from', 'subject', 'date' keys
        """

        def _extract_header(headers: List[Dict], name: str) -> str:
            for header in headers:
                if header["name"] == name:
                    return header["value"]
            return ""

        if not self.service:
            print("Gmail service not initialized. Please authenticate first.")
            return []

        try:
            # Get unread message IDs
            results = (
                # pylint: disable=no-member
                self.service.users()
                .messages()
                .list(userId="me", labelIds=["UNREAD"], maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])

            if not messages:
                print("No unread messages found.")
                return []

            emails = []

            # Get full message details for each unread email
            for message in messages:
                msg = (
                    # pylint: disable=no-member
                    self.service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=message["id"],
                        format="metadata",
                        metadataHeaders=["From", "Subject", "Date"],
                    )
                    .execute()
                )

                headers = msg["payload"]["headers"]
                email_data = {
                    "from": _extract_header(headers, "From"),
                    "subject": _extract_header(headers, "Subject"),
                    "date": _extract_header(headers, "Date"),
                }

                emails.append(email_data)

            return emails

        except HttpError as error:
            print(f"Gmail API error: {error}")
            return []
        except Exception as e:
            print(f"Error retrieving emails: {e}")
            return []
