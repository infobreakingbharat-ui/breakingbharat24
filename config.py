import os
from dotenv import load_dotenv


load_dotenv()




# GROQ
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# WORDPRESS
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
# --------------------
# NEWS API
# --------------------
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# --------------------
# PEXELS
# --------------------
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")