"""Base person model for inheritance demonstration."""


class Person:
    """Represents a generic person with shared attributes."""

    def __init__(self, name: str, email: str = "") -> None:
        """Initialize a person with a name and optional email."""
        self.name = name
        self.email = email

    @property
    def name(self) -> str:
        """Return the person's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the person's name with basic validation."""
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self) -> str:
        """Return the person's email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set the person's email."""
        self._email = value.strip()

    def to_dict(self) -> dict:
        """Convert the person to a serializable dictionary."""
        return {
            "name": self.name,
            "email": self.email,
        }

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Person(name={self.name!r}, email={self.email!r})"
