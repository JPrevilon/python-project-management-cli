"""Task model for project task tracking."""


class Task:
    """Represents a task that belongs to a project."""

    _id_counter = 1

    def __init__(
        self,
        title: str,
        assigned_to: str = "",
        status: str = "pending",
        task_id: int | None = None,
    ) -> None:
        """Initialize a task with title, assignee, and status."""
        if task_id is None:
            self.id = Task._id_counter
            Task._id_counter += 1
        else:
            self.id = task_id
            Task._id_counter = max(Task._id_counter, task_id + 1)

        self.title = title
        self.assigned_to = assigned_to
        self.status = status

    @property
    def title(self) -> str:
        """Return the task title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title with validation."""
        value = value.strip()
        if not value:
            raise ValueError("Task title cannot be empty.")
        self._title = value

    @property
    def status(self) -> str:
        """Return the task status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Set the task status and ensure it is valid."""
        value = value.strip().lower()
        valid_statuses = {"pending", "complete"}
        if value not in valid_statuses:
            raise ValueError("Status must be 'pending' or 'complete'.")
        self._status = value

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.status = "complete"

    def to_dict(self) -> dict:
        """Convert the task to a serializable dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task object from a dictionary."""
        return cls(
            title=data["title"],
            assigned_to=data.get("assigned_to", ""),
            status=data.get("status", "pending"),
            task_id=data.get("id"),
        )

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"
