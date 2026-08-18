from pathlib import Path
from fastapi_mail import ConnectionConfig
from config.env.env import env


class MailerConfig:
    def __init__(self):
        self.config = ConnectionConfig(
            MAIL_USERNAME=env.mailUsername,
            MAIL_PASSWORD=env.mailPassword,
            MAIL_FROM=env.mailFrom,
            MAIL_PORT=env.mailPort,
            MAIL_SERVER=env.mailServer,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            MAIL_FROM_NAME=env.mailFromName,
            USE_CREDENTIALS=False,
            VALIDATE_CERTS=False,
            TEMPLATE_FOLDER=Path(__file__).parent / "templates",
        )


mailer_config = MailerConfig().config
