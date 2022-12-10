Google spreadsheet email reporter
=================================
This is used to read data from a google spreadsheet, generate a graph from the spreadsheet,
and send it as an email report.
 
# Installation
* Create a virtualenv for the project, python3 is required
```
virtualenv env -p `which python3`
```
* Activate the virtualenv from the project dir for working in terminal
```
$ source env/bin/activate
```
(Setup the project interpreter in PyCharm)

* Install the project requirements by running
```
$ pip3 install -r requirements.txt
```
* Create the environment variables, it should have gmail user and app specific password.
In order to obtain app specific password, go to [accounts.google.com](accounts.google.com)
and under **Security** go to **App passwords**
```python
SMTP_SERVER_USER = "you@gmail.com"
SMTP_SERVER_PASSWORD = "xxx"  # Generate app specific code if you have 2FA
```
alternatively, you can add these to `settings.py`

# Usage
Edit `settings.py` to match your required needs
```python
# Load secrets from environment variables
import os
SMTP_SERVER_USER = os.getenv('SMTP_SERVER_USER', None)
SMTP_SERVER_PASSWORD = os.getenv('SMTP_SERVER_PASSWORD', None)

if not SMTP_SERVER_USER or not SMTP_SERVER_PASSWORD:
    print('SMTP_SERVER_USER not set, exiting')
    exit(1)
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
```

Afterwards, run 
```
$ python main.py
```

To run periodically, you can use cron, edit your crontab and add the following:
```
# Run every first of the month
0 0 1 * * ~/projects/gsheets-report/run.sh
```

### Tech
* pandas - manipulate dataframe
* matplotlib - generate image from dataframe
* jinja2 - templates

### Development
* You can edit the template being sent under `templates/report.html`


