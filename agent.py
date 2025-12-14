"""Main AI Planning Agent orchestrator."""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import threading
import time

from models import Task, CalendarEvent, UserProfile, TaskStatus, Priority
from services import CalendarService, AIPlannerService, TaskPlan, PreferenceLearner
from database import DatabaseManager
from config import settings


class AITaskPlanningAgent:
    """
    Main AI Task Planning Agent that orchestrates planning, scheduling,
    monitoring, and learning.
    """

    def __init__(self, user_id: str = "default_user"):
        """Initialize the AI planning agent."""
        self.user_id = user_id

        # Initialize components
        self.db = DatabaseManager()
        self.user_profile = self.db.get_profile(user_id)
        self.calendar_service = CalendarService(
            provider=self.user_profile.preferred_calendar
        )
        self.ai_planner = AIPlannerService()
        self.preference_learner = PreferenceLearner()

        # Monitoring
        self.monitoring_active = False
        self.monitoring_thread = None

    def add_task(
        self,
        title: str,
        description: str = None,
        priority: str = "medium",
        estimated_duration: float = 1.0,
        deadline: datetime = None,
        **kwargs
    ) -> Task:
        """
        Add a new task to be scheduled.

        Args:
            title: Task title
            description: Task description
            priority: Task priority (low, medium, high, urgent)
            estimated_duration: Estimated duration in hours
            deadline: Task deadline
            **kwargs: Additional task parameters

        Returns:
            Created Task object
        """
        task = Task(
            title=title,
            description=description,
            priority=Priority(priority),
            estimated_duration=estimated_duration,
            deadline=deadline,
            **kwargs
        )

        # Save to database
        task = self.db.save_task(task)
        print(f"✓ Task added: {task.title} (ID: {task.id})")

        return task

    def generate_plan(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        context: str = None
    ) -> TaskPlan:
        """
        Generate an AI-powered task plan.

        Args:
            start_date: Planning period start (default: now)
            end_date: Planning period end (default: 2 weeks from now)
            context: Additional context or constraints

        Returns:
            Generated TaskPlan
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=14)

        print(f"\n🤖 Generating plan from {start_date.date()} to {end_date.date()}...")

        # Get pending tasks
        tasks = self.db.get_all_tasks(status="pending")
        if not tasks:
            print("No pending tasks to schedule.")
            return TaskPlan({
                "reasoning": "No tasks to schedule",
                "warnings": [],
                "suggestions": [],
                "scheduled_tasks": []
            })

        # Get calendar events
        calendar_events = self.calendar_service.get_events(start_date, end_date)
        print(f"📅 Found {len(calendar_events)} existing calendar events")

        # Generate plan using AI
        plan = self.ai_planner.generate_plan(
            tasks=tasks,
            calendar_events=calendar_events,
            user_profile=self.user_profile,
            context=context
        )

        # Update user profile
        self.user_profile.total_plans_generated += 1
        self.user_profile.last_plan_date = datetime.utcnow()
        self.db.save_profile(self.user_profile)

        print(f"\n✓ Plan generated with {len(plan.scheduled_tasks)} scheduled tasks")
        print(f"\n📊 AI Reasoning: {plan.reasoning}")

        if plan.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in plan.warnings:
                print(f"  - {warning}")

        if plan.suggestions:
            print(f"\n💡 Suggestions:")
            for suggestion in plan.suggestions:
                print(f"  - {suggestion}")

        return plan

    def refine_plan(self, feedback: str, current_plan: TaskPlan) -> TaskPlan:
        """
        Refine the current plan based on user feedback.

        Args:
            feedback: User's feedback on the plan
            current_plan: Current TaskPlan to refine

        Returns:
            Refined TaskPlan
        """
        print(f"\n🔄 Refining plan based on feedback...")

        refined_plan = self.ai_planner.refine_plan(feedback, current_plan)

        # Learn from feedback
        self.user_profile = self.preference_learner.learn_from_feedback(
            feedback=feedback,
            plan_context={'plan': current_plan},
            user_profile=self.user_profile
        )
        self.db.save_profile(self.user_profile)

        print(f"✓ Plan refined")
        print(f"\n📊 AI Reasoning: {refined_plan.reasoning}")

        return refined_plan

    def execute_plan(self, plan: TaskPlan) -> List[CalendarEvent]:
        """
        Execute the plan by scheduling tasks on the calendar.

        Args:
            plan: TaskPlan to execute

        Returns:
            List of created CalendarEvent objects
        """
        print(f"\n📅 Executing plan - scheduling {len(plan.scheduled_tasks)} tasks...")

        created_events = []

        for scheduled_task in plan.scheduled_tasks:
            task_id = scheduled_task['task_id']
            task = self.db.get_task(task_id)

            if not task:
                print(f"⚠️  Task {task_id} not found, skipping...")
                continue

            # Create calendar event
            event = CalendarEvent(
                title=f"[TASK] {task.title}",
                description=task.description or "",
                start_time=datetime.fromisoformat(scheduled_task['scheduled_start']),
                end_time=datetime.fromisoformat(scheduled_task['scheduled_end']),
                event_type="scheduled_task",
                task_id=task.id
            )

            # Save to database
            event = self.db.save_event(event)

            # Sync to external calendar
            try:
                event = self.calendar_service.create_event(event)
                self.db.save_event(event)  # Update with calendar_id
                print(f"  ✓ Scheduled: {task.title} ({scheduled_task['scheduled_start']})")
            except Exception as e:
                print(f"  ⚠️  Failed to sync {task.title} to calendar: {e}")

            # Update task status
            task.status = TaskStatus.SCHEDULED
            task.scheduled_start = event.start_time
            task.scheduled_end = event.end_time
            self.db.save_task(task)

            created_events.append(event)

        print(f"\n✓ Plan executed - {len(created_events)} tasks scheduled on calendar")
        return created_events

    def mark_task_in_progress(self, task_id: str) -> Task:
        """Mark a task as in progress."""
        task = self.db.get_task(task_id)
        if task:
            task.status = TaskStatus.IN_PROGRESS
            task.actual_start = datetime.utcnow()
            task = self.db.save_task(task)
            print(f"✓ Task started: {task.title}")
        return task

    def mark_task_completed(self, task_id: str) -> Task:
        """
        Mark a task as completed and learn from it.

        Args:
            task_id: Task ID to complete

        Returns:
            Updated Task object
        """
        task = self.db.get_task(task_id)
        if not task:
            print(f"Task {task_id} not found")
            return None

        # Update task
        task.status = TaskStatus.COMPLETED
        task.actual_end = datetime.utcnow()

        if task.actual_start:
            duration = (task.actual_end - task.actual_start).total_seconds() / 3600
            task.actual_duration = duration

        task = self.db.save_task(task)
        print(f"✓ Task completed: {task.title}")

        # Learn from completion
        self.user_profile = self.preference_learner.learn_from_task_completion(
            task=task,
            user_profile=self.user_profile
        )
        self.db.save_profile(self.user_profile)

        # Analyze deviation if scheduled
        if task.scheduled_end and task.actual_end:
            deviation_hours = (task.actual_end - task.scheduled_end).total_seconds() / 3600
            if abs(deviation_hours) > 0.25:  # More than 15 minutes deviation
                print(f"  📊 Analyzing deviation ({deviation_hours:+.2f} hours)...")
                analysis = self.ai_planner.analyze_deviation(
                    task=task,
                    scheduled_time=task.scheduled_end,
                    actual_completion_time=task.actual_end,
                    user_profile=self.user_profile
                )
                print(f"  💡 Insight: {analysis.get('deviation_reason', 'N/A')}")

        return task

    def start_monitoring(self, interval_minutes: int = None):
        """
        Start real-time monitoring of task progress.

        Args:
            interval_minutes: Monitoring check interval (default from settings)
        """
        if self.monitoring_active:
            print("Monitoring already active")
            return

        interval = interval_minutes or settings.monitoring_interval_minutes
        self.monitoring_active = True

        def monitor_loop():
            print(f"\n🔍 Started monitoring (checking every {interval} minutes)")
            while self.monitoring_active:
                self._check_schedule_adherence()
                time.sleep(interval * 60)

        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        print("🔍 Monitoring stopped")

    def _check_schedule_adherence(self):
        """Check if user is following the schedule and trigger replanning if needed."""
        now = datetime.utcnow()

        # Get all scheduled tasks
        scheduled_tasks = self.db.get_all_tasks(status="scheduled")

        for task in scheduled_tasks:
            if not task.scheduled_start or not task.scheduled_end:
                continue

            # Check if task should have started
            if now > task.scheduled_start and task.status == TaskStatus.SCHEDULED:
                # Task should be in progress
                time_overdue = (now - task.scheduled_start).total_seconds() / 60
                if time_overdue > 15:  # 15 minutes late
                    print(f"\n⚠️  Task '{task.title}' is {time_overdue:.0f} minutes overdue")
                    # Could trigger notification or replanning here

            # Check if task is past deadline
            if now > task.scheduled_end and task.status in [TaskStatus.SCHEDULED, TaskStatus.IN_PROGRESS]:
                print(f"\n⚠️  Task '{task.title}' missed its scheduled end time")
                # Mark as overdue
                task.status = TaskStatus.OVERDUE
                self.db.save_task(task)

    def trigger_replan(self, reason: str = "Schedule deviation detected"):
        """
        Trigger dynamic replanning.

        Args:
            reason: Reason for replanning
        """
        print(f"\n🔄 Replanning triggered: {reason}")

        # Get all non-completed tasks
        pending_tasks = self.db.get_all_tasks(status="pending")
        scheduled_tasks = self.db.get_all_tasks(status="scheduled")
        overdue_tasks = self.db.get_all_tasks(status="overdue")

        all_tasks = pending_tasks + scheduled_tasks + overdue_tasks

        # Reset their status to pending for replanning
        for task in all_tasks:
            if task.status != TaskStatus.PENDING:
                task.status = TaskStatus.PENDING
                task.scheduled_start = None
                task.scheduled_end = None
                self.db.save_task(task)

        # Generate new plan
        context = f"Replanning due to: {reason}. Please prioritize overdue tasks."
        new_plan = self.generate_plan(context=context)

        return new_plan

    def get_insights(self) -> Dict[str, Any]:
        """Get insights about learned preferences and patterns."""
        return self.preference_learner.generate_insights_report(self.user_profile)

    def list_tasks(self, status: str = None) -> List[Task]:
        """
        List tasks, optionally filtered by status.

        Args:
            status: Filter by status (pending, scheduled, completed, etc.)

        Returns:
            List of tasks
        """
        return self.db.get_all_tasks(status=status)

    def get_calendar_events(
        self,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[CalendarEvent]:
        """Get calendar events in a date range."""
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=7)

        return self.calendar_service.get_events(start_date, end_date)
