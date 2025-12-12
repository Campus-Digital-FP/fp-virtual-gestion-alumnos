import os
from dotenv import load_dotenv

# Si se ha marcado entorno «test», cargamos .env.test
if os.getenv("APP_ENV") == "test":
    load_dotenv(dotenv_path=".env.test", override=True)