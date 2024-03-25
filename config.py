from dotenv import load_dotenv

import os


load_dotenv()

TOKEN_DIRECTUS = os.getenv("TOKEN_DIRECTUS")

TOKEN_BOT = os.getenv("TOKEN_BOT")

DIRECTUS_API_URL = os.getenv("DIRECTUS_API_URL")

REDIS_URL = os.getenv("REDIS_URL")

URL_UPDATE="https://b453947.leadteh.ru/webhooks/telegram/302636:DCAHOybbWWTXR4DNtn54XQ3h5D7EyADMLUWVgHHQ6VdmM3ft0Z54utt0D6xpJosF"