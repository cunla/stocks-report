import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SMTP_SERVER_USER = os.getenv('SMTP_SERVER_USER', None)
SMTP_SERVER_PASSWORD = os.getenv('SMTP_SERVER_PASSWORD', None)

#if not SMTP_SERVER_USER or not SMTP_SERVER_PASSWORD:
#    print('SMTP_SERVER_USER not set, exiting')
#    exit(1)
# Number of months to include in the report
NUMBER_OF_MONTHS = 24

# SMTP server settings, username and password are stored in secrets.py
SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER_PORT = 465

# Report sender name and email address
REPORT_SENDER = ("Stocks-report", "a@gmail.com")
# Report email subject
REPORT_SUBJECT = 'Report on stocks:'
# Report recipient name and email address
REPORT_RECIPIENT = [("Daniel", "style.daniel@gmail.com"),
                    ]

# Report template
REPORT_TEMPLATE = 'templates/email_report.html'
