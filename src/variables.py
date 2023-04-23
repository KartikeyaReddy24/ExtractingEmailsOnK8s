from import_utils import *


# SQS URL and Queue Name
SQS_URL = "https://sqs.us-east-1.amazonaws.com/492094906798/"
SQS_QUEUE_NAME = "MyQueue"

# SQS Region Name
REGION_NAME_SQS = "us-east-1"

# Maximum Search Resulsts Per Serach Using
MAX_RESULTS_PER_SEARCH = 1

# Delay Time After Making Every Search
DELAY_TIME_AFTER_EVERY_SEARCH = 25

# Maximu Websearches
MAX_WEBSEARCHES = 2

# Wait TIme After Reaching Maximum Websearches
WAIT_TIME_AFTER_REACHIGN_MAX_WEBSEARCHES = 90

# Extracting Emails
EMAIL_REGEX = r"-*([\w\-\.]{1,100}@(?!example.com)(?!wixpress.com)(?!email.com)(?!sentry-viewer.wixpress.com)(?!2x.gif)(?!sentry.o2dev.net)(?!2x.png.com)(?!sentry.wixpress.com)(?!sentry-next.wixpress.com)(?!sentry.io)(?!16.14.0.com)(?!16.14.0)(?!ingest.sentry.io)(?!aphixsoftware.com)(?:\w[\w\-]+\.)+(?!jpg)(?!png)(?!js)(?!gif)[\w]+)-*"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

# Database
DB_HOST= 'extracting-emails-database.cglvu9svk8cj.us-east-1.rds.amazonaws.com'
DB_PORT= 5432
INSERT_QUERY= (
        "INSERT INTO emails (email_address, source_url, created_at) VALUES %s ON CONFLICT DO NOTHING"
    )

# Database Batch Size
BATCH_SIZE = 4

# Database - Batch Size for Emails IDS
BATCH_SIZE_FOR_EMAILIDS = 4

# Get the timezone object for Eastern Time Zone
EASTERN_TIME_ZONE = pytz.timezone('US/Eastern')


