from dotenv import load_dotenv

import os


load_dotenv()

TOKEN_DIRECTUS = os.getenv("TOKEN_DIRECTUS")

TOKEN_BOT = os.getenv("TOKEN_BOT")

DIRECTUS_API_URL = os.getenv("DIRECTUS_API_URL")

REDIS_URL = os.getenv("REDIS_URL")

URL_UPDATE="https://b463160.leadteh.ru/webhooks/telegram/308966:f8YzRIpSoD3PN9LGqQwJtamWUkjBjUgc7VoeqlwiGTun229EEXU623JbtOKr0PuM"