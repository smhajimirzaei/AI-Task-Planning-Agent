"""Example usage of the AI Task Planning Agent."""

from datetime import datetime, timedelta
from agent import AITaskPlanningAgent


def main():
    """Demonstrate the AI planning agent capabilities."""

    print("=" * 60)
    print("AI Task Planning Agent - Example Usage")
    print("=" * 60)

    # Initialize the agent
    agent = AITaskPlanningAgent()

    print("\n1. Adding Tasks")
    print("-" * 60)

    # Add some example tasks
    task1 = agent.add_task(
        title="Complete project proposal",
        description="Draft Q1 2025 project proposal for management review",
        priority="high",
        estimated_duration=3.0,
        deadline=datetime.now() + timedelta(days=7),
        requires_deep_focus=True
    )

    task2 = agent.add_task(
        title="Team meeting preparation",
        description="Prepare slides and agenda for weekly team sync",
        priority="medium",
        estimated_duration=1.5,
        deadline=datetime.now() + timedelta(days=2),
    )

    task3 = agent.add_task(
        title="Code review",
        description="Review pull requests from team members",
        priority="medium",
        estimated_duration=2.0,
        can_split=True
    )

    task4 = agent.add_task(
        title="Update documentation",
        description="Update API documentation with new endpoints",
        priority="low",
        estimated_duration=1.0,
    )

    task5 = agent.add_task(
        title="Client presentation",
        description="Prepare and deliver client demo presentation",
        priority="urgent",
        estimated_duration=2.5,
        deadline=datetime.now() + timedelta(days=3),
        requires_deep_focus=True
    )

    print(f"\n✓ Added {5} tasks")

    # List all tasks
    print("\n2. Listing All Tasks")
    print("-" * 60)
    tasks = agent.list_tasks()
    for task in tasks:
        print(f"  - {task.title} [{task.priority}] ({task.estimated_duration}h)")

    # Generate a plan
    print("\n3. Generating AI-Powered Plan")
    print("-" * 60)

    plan = agent.generate_plan(
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=14),
        context="Focus on deadline-critical tasks first"
    )

    print("\n📅 Generated Plan:")
    for scheduled_task in plan.scheduled_tasks:
        print(f"  • {scheduled_task['title']}")
        print(f"    Time: {scheduled_task['scheduled_start']} → {scheduled_task['scheduled_end']}")
        print(f"    Rationale: {scheduled_task['rationale']}\n")

    # Simulate user feedback and refinement
    print("\n4. Refining Plan with Feedback")
    print("-" * 60)

    feedback = "Move deep focus tasks to morning hours between 9-11 AM"
    refined_plan = agent.refine_plan(feedback, plan)

    print(f"\n✓ Plan refined based on feedback: '{feedback}'")

    # Execute the plan
    print("\n5. Executing Plan (Scheduling on Calendar)")
    print("-" * 60)

    # Note: This would actually add to calendar if credentials are set up
    try:
        events = agent.execute_plan(refined_plan)
        print(f"\n✓ {len(events)} tasks scheduled on calendar")
    except Exception as e:
        print(f"\n⚠️  Calendar sync skipped (configure credentials): {e}")

    # Simulate task completion
    print("\n6. Completing a Task")
    print("-" * 60)

    # Mark a task as in progress
    agent.mark_task_in_progress(task2.id)
    print(f"✓ Started: {task2.title}")

    # Simulate some work time
    import time
    time.sleep(1)  # Simulate work

    # Mark as completed
    completed_task = agent.mark_task_completed(task2.id)
    print(f"✓ Completed: {completed_task.title}")

    # View insights
    print("\n7. Viewing Productivity Insights")
    print("-" * 60)

    insights = agent.get_insights()

    print(f"\n📊 Productivity Summary:")
    print(f"  Peak Hours: {insights['productivity_summary']['peak_productive_hours'] or 'Learning...'}")
    print(f"  Average Focus Duration: {insights['productivity_summary']['average_focus_duration']:.1f}h")
    print(f"  Preferred Session Length: {insights['productivity_summary']['preferred_session_length']:.1f}h")

    print(f"\n📈 Schedule Adherence:")
    print(f"  Adherence Rate: {insights['schedule_adherence']['adherence_rate']:.1f}%")
    print(f"  On-Time Completion: {insights['schedule_adherence']['on_time_completion_rate']:.1f}%")

    print(f"\n📚 Learning Stats:")
    print(f"  Plans Generated: {insights['learning_stats']['total_plans_generated']}")
    print(f"  Feedback Received: {insights['learning_stats']['total_feedback_received']}")
    print(f"  Tasks Tracked: {insights['learning_stats']['tasks_tracked']}")

    if insights['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in insights['recommendations']:
            print(f"  - {rec}")

    # Demonstrate replanning
    print("\n8. Dynamic Replanning (Schedule Deviation)")
    print("-" * 60)

    print("Triggering replan due to schedule changes...")
    new_plan = agent.trigger_replan(reason="Unexpected meeting added to calendar")
    print(f"✓ New plan generated with {len(new_plan.scheduled_tasks)} tasks")

    print("\n" + "=" * 60)
    print("Example Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("  1. Set up your .env file with API keys")
    print("  2. Configure Google Calendar credentials")
    print("  3. Run: python main.py setup")
    print("  4. Run: python main.py interactive")
    print("\nFor CLI usage: python main.py --help")


if __name__ == "__main__":
    main()
