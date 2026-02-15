from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

FARMOS_BASE_URL = os.getenv("FARMOS_BASE_URL")