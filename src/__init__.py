import os

from dotenv import load_dotenv

# Define the path to the .env file
env_file = ".env"

# Check if the .env file exists
if not os.path.exists(env_file):
    raise ValueError(f"Error: .env file not found at {env_file}")

# Load environment variables from the .env file
load_dotenv(env_file)

FASTAPI_ENVIRONMENT = os.getenv("FA_ENVIRONMENT")

if FASTAPI_ENVIRONMENT is None:
    raise ValueError("FA_ENVIRONMENT environment variable not found")
