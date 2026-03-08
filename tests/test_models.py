"""Unit tests for models."""

from models.user import User
from models.project import Project
from models.task import Task


def test_user_can_add_project():
    user = User("Alex", "alex@example.com")
    project = Project("CLI Tool", "A terminal app", "2026-03-10")
    user.add_project(project)

    assert len(user.projects) == 1
    assert user.projects[0].title == "CLI Tool"


def test_project_can_add_task():
    project = Project("CLI Tool")
    task = Task("Implement add-task", "Alex")
    project.add_task(task)

    assert len(project.tasks) == 1
    assert project.tasks[0].title == "Implement add-task"


def test_task_can_mark_complete():
    task = Task("Write tests")
    task.mark_complete()

    assert task.status == "complete"


def test_get_project_by_title():
    user = User("Alex")
    project = Project("CLI Tool")
    user.add_project(project)

    found = user.get_project_by_title("CLI Tool")
    assert found is not None
    assert found.title == "CLI Tool"
