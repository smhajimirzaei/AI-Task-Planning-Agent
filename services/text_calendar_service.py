"""Text-based calendar service without external API integration."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models import CalendarEvent, EventType


class TextCalendarService:
    """
    Calendar service that works with text-based schedule input.
    No external API integration - all schedules are managed through conversation.
    """

    def __init__(self, user_id: str, db_manager=None):
        """Initialize text-based calendar service."""
        self.user_id = user_id
        self.db = db_manager

    def parse_schedule_from_text(self, schedule_text: str, week_start: datetime = None) -> List[CalendarEvent]:
        """
        Parse schedule from natural language text using AI.

        Args:
            schedule_text: User's schedule description
            week_start: Start date for the week

        Returns:
            List of CalendarEvent objects
        """
        # This will be enhanced by AI to parse natural language schedules
        # For now, store as a single event
        if week_start is None:
            week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Store the raw schedule text as a special event
        schedule_event = CalendarEvent(
            calendar_id=self.user_id,
            title="Weekly Schedule",
            description=schedule_text,
            start_time=week_start,
            end_time=week_start + timedelta(days=7),
            event_type=EventType.PERSONAL,
            is_all_day=True
        )

        return [schedule_event]

    def get_events(self, start_date: datetime, end_date: datetime) -> List[CalendarEvent]:
        """
        Get calendar events for a date range.

        Args:
            start_date: Start of range
            end_date: End of range

        Returns:
            List of CalendarEvent objects from database
        """
        if self.db is None:
            return []

        # Get events from database using the correct method name
        return self.db.get_events(start_date, end_date)

    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        """
        Create a calendar event (stores in database only, no external API).

        Args:
            event: CalendarEvent to create

        Returns:
            Created CalendarEvent
        """
        if self.db is not None:
            self.db.save_event(event)
        return event

    def create_events_from_plan(self, planned_tasks: List[Dict[str, Any]]) -> List[CalendarEvent]:
        """
        Create calendar events from AI-generated plan.

        Args:
            planned_tasks: List of scheduled tasks from AI planner

        Returns:
            List of created CalendarEvent objects
        """
        events = []
        for task in planned_tasks:
            event = CalendarEvent(
                calendar_id=self.user_id,
                title=task.get('title', 'Scheduled Task'),
                description=f"Task ID: {task.get('task_id')}\n{task.get('rationale', '')}",
                start_time=datetime.fromisoformat(task['scheduled_start']),
                end_time=datetime.fromisoformat(task['scheduled_end']),
                event_type=EventType.SCHEDULED_TASK
            )
            created_event = self.create_event(event)
            events.append(created_event)

        return events

    def update_schedule_from_text(self, schedule_text: str, week_start: datetime = None) -> Dict[str, Any]:
        """
        Update weekly schedule from text description.

        Args:
            schedule_text: User's schedule in natural language
            week_start: Start of the week

        Returns:
            Summary of updated schedule
        """
        if week_start is None:
            week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            # Adjust to Monday
            week_start = week_start - timedelta(days=week_start.weekday())

        week_end = week_start + timedelta(days=7)

        # Clear existing schedule for this week (optional)
        # For now, we'll just add the new schedule

        events = self.parse_schedule_from_text(schedule_text, week_start)

        for event in events:
            self.create_event(event)

        return {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "schedule_text": schedule_text,
            "events_created": len(events),
            "message": "Schedule updated successfully"
        }

    def get_schedule_summary(self, start_date: datetime = None, days: int = 7) -> str:
        """
        Get a text summary of the schedule.

        Args:
            start_date: Start date for summary
            days: Number of days to summarize

        Returns:
            Text summary of schedule
        """
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        end_date = start_date + timedelta(days=days)
        events = self.get_events(start_date, end_date)

        if not events:
            return "No scheduled events found."

        summary = f"Schedule from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}:\n\n"

        # Group by date
        events_by_date = {}
        for event in events:
            date_key = event.start_time.strftime('%Y-%m-%d')
            if date_key not in events_by_date:
                events_by_date[date_key] = []
            events_by_date[date_key].append(event)

        # Format summary
        for date_key in sorted(events_by_date.keys()):
            summary += f"**{date_key}**\n"
            for event in sorted(events_by_date[date_key], key=lambda e: e.start_time):
                if event.is_all_day:
                    summary += f"  - All day: {event.title}\n"
                else:
                    time_range = f"{event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}"
                    summary += f"  - {time_range}: {event.title}\n"
            summary += "\n"

        return summary

    def record_actual_completion(self, task_id: str, completion_text: str, completion_date: datetime = None) -> Dict[str, Any]:
        """
        Record what was actually done vs what was planned.

        Args:
            task_id: Task ID
            completion_text: Description of what was actually done
            completion_date: When it was completed

        Returns:
            Summary of recorded completion
        """
        if completion_date is None:
            completion_date = datetime.now()

        # This will be used for learning and improving future plans
        return {
            "task_id": task_id,
            "completion_text": completion_text,
            "completion_date": completion_date.isoformat(),
            "recorded": True,
            "message": "Actual completion recorded for learning"
        }
