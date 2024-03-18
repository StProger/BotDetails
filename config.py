from dotenv import load_dotenv

import os


load_dotenv()

TOKEN_DIRECTUS = os.getenv("TOKEN_DIRECTUS")

TOKEN_BOT = os.getenv("TOKEN_BOT")

DIRECTUS_API_URL = os.getenv("DIRECTUS_API_URL")

REDIS_URL = os.getenv("REDIS_URL")

URL_UPDATE="https://b309120.leadteh.ru/webhooks/telegram/293619:a6T8ULYyV6dweMtF81iubXJOi9Z84uwzU2fSf4Rpdt45QWGBSYWKEIzjSUtnHB0C"
