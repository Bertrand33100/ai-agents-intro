"""Configuration commune des modèles utilisés par les agents."""

import os

from dotenv import load_dotenv


load_dotenv()

DEFAULT_MODEL_NAME = "ollama_chat/qwen3:1.7b"
MODEL_NAME = os.getenv("MODEL_NAME", "").strip()
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "").strip().rstrip("/")


def get_model_name() -> str:
    """Retourne un modèle utilisable avant la vérification de configuration."""

    return MODEL_NAME or DEFAULT_MODEL_NAME
