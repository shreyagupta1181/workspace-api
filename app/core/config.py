import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL host:", DATABASE_URL.split("@")[-1] if DATABASE_URL else "MISSING")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")