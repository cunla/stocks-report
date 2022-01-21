# Import from secrets.py
# SMTP_SERVER_USER = "xxx"
# SMTP_SERVER_PASSWORD = "xxx"

from smtp_secrets import *

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
