"""Project model for grouping tasks."""

from models.task import Task


class Project:
    """Represents a project owned by a user."""

    _id_counter = 1

    def __init__(
        self,
        title: str,
        description: str = "",
        due_date: str = "",
        contributors: list[str] | None = None,
        tasks: list[Task] | None = None,
        project_id: int | None = None,
    ) -> None:
        """Initialize a project with metadata and tasks."""
        if project_id is None:
            self.id = Project._id_counter
            Project._id_counter += 1
        else:
            self.id = project_id
            Project._id_counter = max(Project._id_counter, project_id + 1)

        self.title = title
        self.description = description
        self.due_date = due_date
        self.contributors = contributors or []
        self.tasks = tasks or []

    @property
    def title(self) -> str:
        """Return the project title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the project title with validation."""
        value = value.strip()
        if not value:
            raise ValueError("Project title cannot be empty.")
        self._title = value

    def add_task(self, task: Task) -> None:
        """Add a task to the project."""
        self.tasks.append(task)

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Return a task by its ID if found."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def to_dict(self) -> dict:
        """Convert the project to a serializable dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "contributors": self.contributors,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """Create a Project object from a dictionary."""
        tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            contributors=data.get("contributors", []),
            tasks=tasks,
            project_id=data.get("id"),
        )

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Project(id={self.id}, title={self.title!r}, tasks={len(self.tasks)})"
