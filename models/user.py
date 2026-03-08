"""User model representing an admin/team user."""

from models.person import Person
from models.project import Project


class User(Person):
    """Represents a system user who owns projects."""

    _id_counter = 1

    def __init__(
        self,
        name: str,
        email: str = "",
        projects: list[Project] | None = None,
        user_id: int | None = None,
    ) -> None:
        """Initialize a user and their project collection."""
        super().__init__(name, email)

        if user_id is None:
            self.id = User._id_counter
            User._id_counter += 1
        else:
            self.id = user_id
            User._id_counter = max(User._id_counter, user_id + 1)

        self.projects = projects or []

    def add_project(self, project: Project) -> None:
        """Add a project to the user."""
        self.projects.append(project)

    def get_project_by_title(self, title: str) -> Project | None:
        """Find a project by title."""
        for project in self.projects:
            if project.title.lower() == title.lower():
                return project
        return None

    def to_dict(self) -> dict:
        """Convert the user to a serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Create a User object from a dictionary."""
        projects = [
            Project.from_dict(project_data) for project_data in data.get("projects", [])
        ]
        return cls(
            name=data["name"],
            email=data.get("email", ""),
            projects=projects,
            user_id=data.get("id"),
        )

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"User(id={self.id}, name={self.name!r}, projects={len(self.projects)})"
