"""CLI entry point for the Project Management Tool."""

import argparse
from models.user import User
from models.project import Project
from models.task import Task
from utils.helpers import parse_due_date, find_user, find_project
from utils.storage import load_data, save_data
from utils.ui import (
    show_header,
    show_success,
    show_error,
    show_info,
    render_users,
    render_projects,
    render_tasks,
)


def handle_add_user(args) -> None:
    """Handle adding a new user."""
    users = load_data()

    if find_user(users, args.name):
        show_error(f"User '{args.name}' already exists.")
        return

    user = User(name=args.name, email=args.email or "")
    users.append(user)
    save_data(users)
    show_success(f"User '{args.name}' added successfully.")


def handle_list_users(args) -> None:
    """Handle listing all users."""
    users = load_data()

    if not users:
        show_info("No users found.")
        return

    render_users(users)


def handle_add_project(args) -> None:
    """Handle adding a project to a user."""
    users = load_data()
    user = find_user(users, args.user)

    if not user:
        show_error(f"User '{args.user}' not found.")
        return

    if user.get_project_by_title(args.title):
        show_error(f"Project '{args.title}' already exists for user '{args.user}'.")
        return

    due_date = parse_due_date(args.due_date) if args.due_date else ""
    contributors = (
        [name.strip() for name in args.contributors.split(",")]
        if args.contributors
        else []
    )

    project = Project(
        title=args.title,
        description=args.description or "",
        due_date=due_date,
        contributors=contributors,
    )
    user.add_project(project)
    save_data(users)
    show_success(f"Project '{args.title}' added to user '{args.user}'.")


def handle_list_projects(args) -> None:
    """Handle listing projects for a user."""
    users = load_data()
    user = find_user(users, args.user)

    if not user:
        show_error(f"User '{args.user}' not found.")
        return

    if not user.projects:
        show_info(f"No projects found for '{args.user}'.")
        return

    render_projects(user)


def handle_add_task(args) -> None:
    """Handle adding a task to a project."""
    users = load_data()
    owner, project = find_project(users, args.project)

    if not project:
        show_error(f"Project '{args.project}' not found.")
        return

    task = Task(title=args.title, assigned_to=args.assigned_to or "")
    project.add_task(task)
    save_data(users)
    show_success(f"Task '{args.title}' added to project '{project.title}'.")


def handle_list_tasks(args) -> None:
    """Handle listing tasks for a project."""
    users = load_data()
    owner, project = find_project(users, args.project)

    if not project:
        show_error(f"Project '{args.project}' not found.")
        return

    if not project.tasks:
        show_info(f"No tasks found for project '{project.title}'.")
        return

    render_tasks(project)


def handle_complete_task(args) -> None:
    """Handle marking a task as complete."""
    users = load_data()
    owner, project = find_project(users, args.project)

    if not project:
        show_error(f"Project '{args.project}' not found.")
        return

    task = project.get_task_by_id(args.task_id)

    if not task:
        show_error(f"Task ID {args.task_id} not found in project '{project.title}'.")
        return

    task.mark_complete()
    save_data(users)
    show_success(f"Task ID {args.task_id} marked as complete.")


def handle_search_project(args) -> None:
    """Handle searching for a project across all users."""
    users = load_data()
    owner, project = find_project(users, args.title)

    if not project:
        show_error(f"Project '{args.title}' not found.")
        return

    show_success(f"Project '{project.title}' belongs to user '{owner.name}'.")
    render_tasks(project)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool",
    )

    subparsers = parser.add_subparsers(dest="command")

    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True, help="User name")
    add_user_parser.add_argument("--email", default="", help="User email")
    add_user_parser.set_defaults(func=handle_add_user)

    list_users_parser = subparsers.add_parser("list-users", help="List all users")
    list_users_parser.set_defaults(func=handle_list_users)

    add_project_parser = subparsers.add_parser(
        "add-project", help="Add a project to a user"
    )
    add_project_parser.add_argument("--user", required=True, help="Owner user name")
    add_project_parser.add_argument("--title", required=True, help="Project title")
    add_project_parser.add_argument(
        "--description", default="", help="Project description"
    )
    add_project_parser.add_argument("--due-date", default="", help="Project due date")
    add_project_parser.add_argument(
        "--contributors", default="", help="Comma-separated contributor names"
    )
    add_project_parser.set_defaults(func=handle_add_project)

    list_projects_parser = subparsers.add_parser(
        "list-projects", help="List a user's projects"
    )
    list_projects_parser.add_argument("--user", required=True, help="User name")
    list_projects_parser.set_defaults(func=handle_list_projects)

    add_task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    add_task_parser.add_argument("--project", required=True, help="Project title")
    add_task_parser.add_argument("--title", required=True, help="Task title")
    add_task_parser.add_argument("--assigned-to", default="", help="Task assignee")
    add_task_parser.set_defaults(func=handle_add_task)

    list_tasks_parser = subparsers.add_parser(
        "list-tasks", help="List tasks for a project"
    )
    list_tasks_parser.add_argument("--project", required=True, help="Project title")
    list_tasks_parser.set_defaults(func=handle_list_tasks)

    complete_task_parser = subparsers.add_parser(
        "complete-task", help="Mark a task complete"
    )
    complete_task_parser.add_argument("--project", required=True, help="Project title")
    complete_task_parser.add_argument(
        "--task-id", type=int, required=True, help="Task ID"
    )
    complete_task_parser.set_defaults(func=handle_complete_task)

    search_project_parser = subparsers.add_parser(
        "search-project", help="Search for a project"
    )
    search_project_parser.add_argument("--title", required=True, help="Project title")
    search_project_parser.set_defaults(func=handle_search_project)

    return parser


def main() -> None:
    """Main program entry point."""
    show_header()
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    try:
        args.func(args)
    except ValueError as error:
        show_error(str(error))
    except Exception as error:
        show_error(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
