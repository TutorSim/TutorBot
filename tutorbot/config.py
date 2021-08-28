import contexts
# Stores credential information
TELEGRAM_API_KEY='YOUR-TELEGRAM-BOT-KEY'

# Google Drive API, credentials
GOOGLE_SERVICE_KEY='YOUR-GOOGLE-SERVICE-KEY.json'

# Google Drive API, credentials
GOOGLE_SPREAD_SHEET='YOUR-GOOGLE-SPREADSHEET-NAME'

class Info:
    PROFESSOR_NAME = 'PROFESSOR_NAME'
    CONTACT_EMAIL = 'PROFESSOR_EMAIL'
    CONTACT_OFFICE = 'PROFESSOR_PHONE'

import os
if os.path.isfile("../instance/config.py"):
	from instance.config import *