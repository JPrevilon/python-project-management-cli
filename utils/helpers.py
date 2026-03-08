"""Helper utilities for validation and searching."""

from dateutil.parser import parse


def parse_due_date(date_str: str) -> str:
    """Parse a date string into YYYY-MM-DD format."""
    if not date_str.strip():
        return ""
    parsed = parse(date_str)
    return parsed.strftime("%Y-%m-%d")


def find_user(users: list, name: str):
    """Find a user by name, case-insensitively."""
    for user in users:
        if user.name.lower() == name.lower():
            return user
    return None


def find_project(users: list, title: str):
    """Find a project by title across all users."""
    for user in users:
        for project in user.projects:
            if project.title.lower() == title.lower():
                return user, project
    return None, None
