from typing import List, Union

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Mail, To

from app.core.config import settings
from app.core.tokens import email_confirmation_token_generator

__all__ = ["email_client"]


class EmailClient:
    def __init__(self):
        self.client = SendGridAPIClient(api_key=settings.SENDGRID.API_KEY)
        self.from_email = Email(
            settings.EMAIL.NO_REPLY_EMAIL, settings.EMAIL.NO_REPLY_NAME
        )

    def send_email(
        self,
        to_emails: Union[List[str], str],
        dynamic_template_id,
        dynamic_template_email: dict,
    ) -> None:
        print("mock called")
        if not isinstance(to_emails, list):
            to_emails = [to_emails]

        to_emails = [To(email) for email in to_emails]

        mail = Mail(from_email=self.from_email, to_emails=to_emails)
        mail.template_id = "d-977239e8c4bc4164800a05976bdfd1ba"
        mail.dynamic_template_data = dynamic_template_email

        return self.client.send(mail)

    def send_registration_email(self, to_user: "User"):
        """Sends welcome email to the user after its registration."""

        # TODO: move to settings
        dynamic_template_id = settings.SENDGRID.REGISTRATION_TPL

        token = email_confirmation_token_generator.create_token(to_user)

        email_confirmation_url = (
            f"{settings.API_URL}/users/verify?id={str(to_user.id)}&token={token}"
        )

        dynamic_template_email = {
            "full_name": to_user.full_name,
            "email_confirmation_url": email_confirmation_url,
        }

        return self.send_email(
            to_emails=to_user.email,
            dynamic_template_id=dynamic_template_id,
            dynamic_template_email=dynamic_template_email,
        )


email_client = EmailClient()
