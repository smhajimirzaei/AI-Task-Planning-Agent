"""Main entry point for the AI Task Planning Agent."""

import sys
from datetime import datetime, timedelta
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
import typer

from agent import AITaskPlanningAgent
from models import Priority

app = typer.Typer()
console = Console()


def display_plan(plan):
    """Display a task plan in a formatted table."""
    if not plan.scheduled_tasks:
        console.print("[yellow]No tasks scheduled in this plan[/yellow]")
        return

    table = Table(title="📅 Generated Task Plan", show_header=True, header_style="bold magenta")
    table.add_column("Task", style="cyan")
    table.add_column("Start Time", style="green")
    table.add_column("End Time", style="green")
    table.add_column("Duration", justify="right")
    table.add_column("Rationale", style="dim")

    for task in plan.scheduled_tasks:
        start = datetime.fromisoformat(task['scheduled_start'])
        end = datetime.fromisoformat(task['scheduled_end'])

        session_info = ""
        if task.get('total_sessions', 1) > 1:
            session_info = f" (Session {task.get('split_session', 1)}/{task['total_sessions']})"

        table.add_row(
            task['title'] + session_info,
            start.strftime("%b %d, %H:%M"),
            end.strftime("%b %d, %H:%M"),
            f"{task['duration_hours']:.1f}h",
            task.get('rationale', '')[:50]
        )

    console.print(table)


def display_tasks(tasks, title="Tasks"):
    """Display tasks in a formatted table."""
    if not tasks:
        console.print(f"[yellow]No {title.lower()} found[/yellow]")
        return

    table = Table(title=f"📋 {title}", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="cyan")
    table.add_column("Priority", justify="center")
    table.add_column("Duration", justify="right")
    table.add_column("Deadline", style="yellow")
    table.add_column("Status")

    for task in tasks:
        priority_color = {
            "urgent": "red bold",
            "high": "red",
            "medium": "yellow",
            "low": "green"
        }.get(str(task.priority), "white")

        deadline_str = task.deadline.strftime("%b %d, %Y") if task.deadline else "-"

        table.add_row(
            task.id[:8] + "...",
            task.title,
            f"[{priority_color}]{task.priority}[/{priority_color}]",
            f"{task.estimated_duration:.1f}h",
            deadline_str,
            str(task.status)
        )

    console.print(table)


@app.command()
def add_task(
    title: str = typer.Argument(..., help="Task title"),
    description: str = typer.Option(None, "--desc", "-d", help="Task description"),
    priority: str = typer.Option("medium", "--priority", "-p", help="Priority: low, medium, high, urgent"),
    duration: float = typer.Option(1.0, "--duration", "-t", help="Estimated duration in hours"),
    deadline: str = typer.Option(None, "--deadline", "-D", help="Deadline (YYYY-MM-DD)"),
    deep_focus: bool = typer.Option(False, "--deep-focus", "-f", help="Requires deep focus"),
):
    """Add a new task to schedule."""
    agent = AITaskPlanningAgent()

    deadline_dt = None
    if deadline:
        try:
            deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Invalid deadline format. Use YYYY-MM-DD[/red]")
            return

    task = agent.add_task(
        title=title,
        description=description,
        priority=priority,
        estimated_duration=duration,
        deadline=deadline_dt,
        requires_deep_focus=deep_focus
    )

    console.print(f"[green]✓[/green] Task added: {task.title} (ID: {task.id})")


@app.command()
def list_tasks(
    status: str = typer.Option(None, "--status", "-s", help="Filter by status")
):
    """List all tasks."""
    agent = AITaskPlanningAgent()
    tasks = agent.list_tasks(status=status)
    display_tasks(tasks, title=f"{status.title() if status else 'All'} Tasks")


@app.command()
def plan(
    days: int = typer.Option(14, "--days", "-d", help="Planning horizon in days"),
    context: str = typer.Option(None, "--context", "-c", help="Additional context"),
):
    """Generate an AI-powered task plan."""
    agent = AITaskPlanningAgent()

    start_date = datetime.now()
    end_date = start_date + timedelta(days=days)

    # Generate initial plan
    current_plan = agent.generate_plan(
        start_date=start_date,
        end_date=end_date,
        context=context
    )

    display_plan(current_plan)

    # Iterative refinement loop
    while True:
        console.print("\n")
        refine = Confirm.ask("Would you like to refine this plan?", default=False)

        if not refine:
            break

        feedback = Prompt.ask("What would you like to change?")
        current_plan = agent.refine_plan(feedback, current_plan)
        display_plan(current_plan)

    # Ask to execute
    console.print("\n")
    execute = Confirm.ask("Execute this plan (add to calendar)?", default=True)

    if execute:
        agent.execute_plan(current_plan)
        console.print("[green]✓ Plan executed and added to calendar![/green]")


@app.command()
def complete(task_id: str = typer.Argument(..., help="Task ID to mark as completed")):
    """Mark a task as completed."""
    agent = AITaskPlanningAgent()
    task = agent.mark_task_completed(task_id)

    if task:
        console.print(f"[green]✓[/green] Task completed: {task.title}")
    else:
        console.print(f"[red]✗[/red] Task {task_id} not found")


@app.command()
def start(task_id: str = typer.Argument(..., help="Task ID to mark as in progress")):
    """Mark a task as in progress."""
    agent = AITaskPlanningAgent()
    task = agent.mark_task_in_progress(task_id)

    if task:
        console.print(f"[green]✓[/green] Task started: {task.title}")
    else:
        console.print(f"[red]✗[/red] Task {task_id} not found")


@app.command()
def monitor(interval: int = typer.Option(15, "--interval", "-i", help="Check interval in minutes")):
    """Start real-time monitoring of schedule adherence."""
    agent = AITaskPlanningAgent()

    console.print("[cyan]Starting monitoring mode...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")

    try:
        agent.start_monitoring(interval_minutes=interval)
        # Keep main thread alive
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop_monitoring()
        console.print("\n[yellow]Monitoring stopped[/yellow]")


@app.command()
def replan(reason: str = typer.Option("Manual replan requested", "--reason", "-r")):
    """Trigger dynamic replanning."""
    agent = AITaskPlanningAgent()
    new_plan = agent.trigger_replan(reason=reason)
    display_plan(new_plan)

    execute = Confirm.ask("Execute this replanned schedule?", default=True)
    if execute:
        agent.execute_plan(new_plan)
        console.print("[green]✓ Replanned schedule executed![/green]")


@app.command()
def insights():
    """View insights about your working patterns and preferences."""
    agent = AITaskPlanningAgent()
    insights = agent.get_insights()

    console.print(Panel.fit(
        f"""[bold cyan]Productivity Insights[/bold cyan]

[yellow]Peak Hours:[/yellow] {', '.join(map(str, insights['productivity_summary']['peak_productive_hours'])) or 'Learning...'}
[yellow]Average Focus Duration:[/yellow] {insights['productivity_summary']['average_focus_duration']:.1f} hours
[yellow]Preferred Session Length:[/yellow] {insights['productivity_summary']['preferred_session_length']:.1f} hours

[cyan]Schedule Adherence[/cyan]
[yellow]Adherence Rate:[/yellow] {insights['schedule_adherence']['adherence_rate']:.1f}%
[yellow]On-Time Completion:[/yellow] {insights['schedule_adherence']['on_time_completion_rate']:.1f}%

[cyan]Learning Stats[/cyan]
[yellow]Plans Generated:[/yellow] {insights['learning_stats']['total_plans_generated']}
[yellow]Feedback Received:[/yellow] {insights['learning_stats']['total_feedback_received']}
[yellow]Tasks Tracked:[/yellow] {insights['learning_stats']['tasks_tracked']}
""",
        title="📊 Your Insights",
        border_style="green"
    ))

    if insights['recommendations']:
        console.print("\n[bold cyan]Recommendations:[/bold cyan]")
        for rec in insights['recommendations']:
            console.print(f"  💡 {rec}")


@app.command()
def setup():
    """Interactive setup wizard for first-time configuration."""
    console.print(Panel.fit(
        "[bold cyan]Welcome to AI Task Planning Agent![/bold cyan]\n\n"
        "Let's set up your preferences.",
        title="🤖 Setup Wizard",
        border_style="cyan"
    ))

    agent = AITaskPlanningAgent()
    profile = agent.user_profile

    # Working hours
    console.print("\n[yellow]Working Hours[/yellow]")
    start_hour = Prompt.ask("Start time (HH:MM)", default="09:00")
    end_hour = Prompt.ask("End time (HH:MM)", default="17:00")

    from datetime import time
    profile.working_hours.start_time = time.fromisoformat(start_hour)
    profile.working_hours.end_time = time.fromisoformat(end_hour)

    # Preferences
    console.print("\n[yellow]Preferences[/yellow]")
    profile.prefer_morning_deep_work = Confirm.ask(
        "Do you prefer deep focus work in the morning?",
        default=True
    )

    profile.max_daily_work_hours = float(Prompt.ask(
        "Maximum work hours per day",
        default="8.0"
    ))

    profile.allow_weekend_scheduling = Confirm.ask(
        "Allow scheduling tasks on weekends?",
        default=False
    )

    # Calendar
    console.print("\n[yellow]Calendar Integration[/yellow]")
    calendar_choice = Prompt.ask(
        "Preferred calendar",
        choices=["google", "outlook"],
        default="google"
    )
    profile.preferred_calendar = calendar_choice

    # Save profile
    agent.db.save_profile(profile)

    console.print("\n[green]✓ Setup complete![/green]")
    console.print("\n[cyan]Next steps:[/cyan]")
    console.print("  1. Add tasks: [bold]python main.py add-task 'Your task title'[/bold]")
    console.print("  2. Generate plan: [bold]python main.py plan[/bold]")
    console.print("  3. Start monitoring: [bold]python main.py monitor[/bold]")


@app.command()
def interactive():
    """Start interactive mode."""
    console.print(Panel.fit(
        "[bold cyan]AI Task Planning Agent - Interactive Mode[/bold cyan]\n\n"
        "Type 'help' for available commands, 'exit' to quit.",
        title="🤖 Interactive Mode",
        border_style="cyan"
    ))

    agent = AITaskPlanningAgent()

    while True:
        try:
            cmd = Prompt.ask("\n[cyan]agent>[/cyan]")

            if cmd.lower() in ['exit', 'quit']:
                break
            elif cmd.lower() == 'help':
                console.print("""
Available commands:
  - add: Add a new task
  - list: List all tasks
  - plan: Generate a plan
  - complete <task_id>: Mark task as completed
  - insights: View productivity insights
  - exit: Exit interactive mode
                """)
            elif cmd.lower() == 'add':
                # Interactive task addition
                title = Prompt.ask("Task title")
                desc = Prompt.ask("Description (optional)", default="")
                priority = Prompt.ask("Priority", choices=["low", "medium", "high", "urgent"], default="medium")
                duration = float(Prompt.ask("Estimated duration (hours)", default="1.0"))

                agent.add_task(title, desc, priority, duration)
            elif cmd.lower() == 'list':
                tasks = agent.list_tasks()
                display_tasks(tasks)
            elif cmd.lower() == 'plan':
                plan_obj = agent.generate_plan()
                display_plan(plan_obj)
            elif cmd.lower() == 'insights':
                insights_data = agent.get_insights()
                console.print(insights_data)
            else:
                console.print("[yellow]Unknown command. Type 'help' for available commands.[/yellow]")

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    console.print("\n[cyan]Goodbye![/cyan]")


if __name__ == "__main__":
    app()
