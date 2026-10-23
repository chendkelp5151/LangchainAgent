import os
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))

def validate_config():
    """Ensure essential configuration parameters are present."""
    if not NVIDIA_API_KEY or NVIDIA_API_KEY == "nvapi-your-nvidia-api-key-here":
        print("\n[ERROR] NVIDIA_API_KEY is not set or using the default placeholder!")
        print("Please configure your API key in a .env file:")
        print("1. Copy .env.example to .env")
        print("2. Get a free API key from https://build.nvidia.com/")
        print("3. Set NVIDIA_API_KEY=... in .env\n")
        return False
    return True
