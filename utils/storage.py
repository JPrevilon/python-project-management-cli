"""JSON persistence utilities."""

import json
import os
from models.user import User

DATA_FILE = "data/project_data.json"


def ensure_data_file() -> None:
    """Ensure the data file exists and contains valid JSON structure."""
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump({"users": []}, file, indent=4)


def load_data() -> list[User]:
    """Load user data from JSON and return User objects."""
    ensure_data_file()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
            return [
                User.from_dict(user_data) for user_data in raw_data.get("users", [])
            ]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def save_data(users: list[User]) -> None:
    """Save User objects to JSON."""
    ensure_data_file()

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump({"users": [user.to_dict() for user in users]}, file, indent=4)
