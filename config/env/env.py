import os
from dotenv import load_dotenv

load_dotenv()


class Env:
    def __init__(self):
        self.beHost = os.getenv("BE_HOST", "0.0.0.0")
        self.bePort = int(os.getenv("BE_PORT", 3000))

        self.dbConnection = os.getenv("DB_CONNECTION", "mysql+pymysql")
        self.dbHost = os.getenv("DB_HOST", "localhost")
        self.dbPort = int(os.getenv("DB_PORT", 3306))
        self.dbUser = os.getenv("DB_USER", "root")
        self.dbPassword = os.getenv("DB_PASSWORD", "")
        self.dbName = os.getenv("DB_NAME", "test")

        self.dbLogging = os.getenv("DB_LOGGING", "false").lower() == "true"

        self.mailUsername = os.getenv("MAIL_USERNAME", "your_email@gmail.com")
        self.mailPassword = os.getenv("MAIL_PASSWORD", "your_app_password")
        self.mailFrom = os.getenv("MAIL_FROM", "noreply@yourdomain.com")
        self.mailPort = int(os.getenv("MAIL_PORT", 1025))
        self.mailServer = os.getenv("MAIL_SERVER", "localhost")
        self.mailFromName = os.getenv("MAIL_FROM_NAME", "Anti-Spoofing Admin")


env = Env()
