# Stdlib Imports
from typing import Dict, List, Union

# Own Imports
from config.secrets import get_settings

# Third Party Imports
import httpx


# Set settings
settings = get_settings()


class EmailManager(object):
    """
    Responsible for sending emails
    """

    def __init__(self, receiver_email: str) -> None:
        self.receiver_email = receiver_email
        self.api_mode = settings.EMAIL_MODE
        self.api_url = settings.EMAIL_API_URL
        self.sender = settings.EMAIL_HOST_SENDER
        self.host_token = settings.EMAIL_HOST_TOKEN

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Api-Token": self.host_token,
        }

    async def send(self, subject: str, content: str, provider: str) -> bool:
        """
        Sends an email to the specified receiver address based on the provider.

        Args:
            subject (str): The subject of the email to send
            content (str): The content of the email to send
            provider (str): The email provider to use

        Returns:
            response (bool): response of the mail
        """

        async with httpx.AsyncClient() as client:
            if provider == "mailtrap":
                response = await self.with_mailtrap(client, subject, content)
            elif provider == "sendgrid":
                response = await self.with_sendgrid(client, subject, content)
            return response

    async def with_mailtrap(
        self, client: httpx.AsyncClient, subject: str, content: str
    ) -> bool:
        """Send email using mailtrap.

        Args:
            client (httpx.AsyncClient): the async client
            subject (str): the subject of the email
            content (str): the body of the email

        Returns:
            bool: email was sent successfully
        """

        if self.api_mode == "sandbox":
            url = self.api_url + "send/2410689"  # my sandbox inbox id
        elif self.api_mode == "production":
            url = self.api_url + "send"

        response = await client.post(
            url,
            json={
                "to": [{"email": self.receiver_email}],
                "from": {
                    "email": self.sender,
                    "name": "Natini Initiatives",
                },
                "subject": subject,
                "text": content,
            },
            headers=self.headers,
        )
        response_data = response.json()
        if response.status_code == 200:
            return response_data["success"]
        return response_data["success"]
