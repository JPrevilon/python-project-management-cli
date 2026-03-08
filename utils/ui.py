"""Rich UI helpers for a polished command-line interface."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def show_header() -> None:
    """Display the application header."""
    console.print(
        Panel.fit(
            "[bold cyan]Project Management CLI Tool[/bold cyan]\n[dim]Dark-mode styled terminal dashboard[/dim]",
            border_style="bright_blue",
        )
    )


def show_success(message: str) -> None:
    """Display a success message."""
    console.print(f"[bold green]✔ {message}[/bold green]")


def show_error(message: str) -> None:
    """Display an error message."""
    console.print(f"[bold red]✘ {message}[/bold red]")


def show_info(message: str) -> None:
    """Display an informational message."""
    console.print(f"[bold yellow]➜ {message}[/bold yellow]")


def render_users(users: list) -> None:
    """Render users in a rich table."""
    table = Table(title="Users", header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Email", style="green")
    table.add_column("Project Count", style="yellow")

    for user in users:
        table.add_row(
            str(user.id), user.name, user.email or "-", str(len(user.projects))
        )

    console.print(table)


def render_projects(user) -> None:
    """Render projects for a specific user."""
    table = Table(title=f"Projects for {user.name}", header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Description", style="green")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tasks", style="bright_blue")

    for project in user.projects:
        table.add_row(
            str(project.id),
            project.title,
            project.description or "-",
            project.due_date or "-",
            str(len(project.tasks)),
        )

    console.print(table)


def render_tasks(project) -> None:
    """Render tasks for a project."""
    table = Table(title=f"Tasks for {project.title}", header_style="bold magenta")
    table.add_column("Task ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Assigned To", style="green")
    table.add_column("Status", style="yellow")

    for task in project.tasks:
        status = (
            "[green]complete[/green]"
            if task.status == "complete"
            else "[red]pending[/red]"
        )
        table.add_row(str(task.id), task.title, task.assigned_to or "-", status)

    console.print(table)
