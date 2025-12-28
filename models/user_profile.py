"""User profile model for storing preferences and learning data."""

from datetime import datetime, time
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class WorkingHoursPreference(BaseModel):
    """User's working hours preferences."""
    start_time: time = Field(default=time(9, 0), description="Typical work start time")
    end_time: time = Field(default=time(17, 0), description="Typical work end time")
    break_duration: float = Field(1.0, description="Lunch/break duration in hours")
    break_start: Optional[time] = Field(time(12, 0), description="Preferred break time")


class ProductivityPattern(BaseModel):
    """Learned productivity patterns."""
    peak_hours: list[int] = Field(
        default_factory=list,
        description="Hours of day when most productive (0-23)"
    )
    low_energy_hours: list[int] = Field(
        default_factory=list,
        description="Hours when energy is typically low"
    )
    preferred_task_duration: float = Field(
        2.0,
        description="Preferred task session duration in hours"
    )
    average_focus_span: float = Field(
        1.5,
        description="Average focus span before break needed (hours)"
    )


class ScheduleAdherence(BaseModel):
    """Tracking schedule adherence patterns."""
    total_tasks_scheduled: int = 0
    tasks_completed_on_time: int = 0
    tasks_completed_early: int = 0
    tasks_completed_late: int = 0
    average_delay_hours: float = 0.0
    average_early_hours: float = 0.0

    @property
    def adherence_rate(self) -> float:
        """Calculate overall adherence rate."""
        if self.total_tasks_scheduled == 0:
            return 0.0
        return (self.tasks_completed_on_time / self.total_tasks_scheduled) * 100


class UserProfile(BaseModel):
    """User profile containing preferences and learned behaviors."""

    user_id: str = Field(default="default_user", description="User identifier")

    # Explicit Preferences
    timezone: str = Field(default="UTC", description="User's timezone")
    working_hours: WorkingHoursPreference = Field(
        default_factory=WorkingHoursPreference
    )
    preferred_calendar: str = Field(
        default="text",
        description="Calendar type: text (conversational), google, outlook"
    )

    # Task Preferences
    prefer_morning_deep_work: bool = Field(
        True,
        description="Prefer deep focus tasks in the morning"
    )
    max_daily_work_hours: float = Field(8.0, description="Maximum work hours per day")
    min_buffer_between_tasks: float = Field(
        0.25,
        description="Minimum buffer between tasks (hours)"
    )
    allow_weekend_scheduling: bool = Field(
        False,
        description="Allow tasks to be scheduled on weekends"
    )

    # Learned Patterns
    productivity_pattern: ProductivityPattern = Field(
        default_factory=ProductivityPattern
    )
    schedule_adherence: ScheduleAdherence = Field(
        default_factory=ScheduleAdherence
    )

    # Custom preferences (flexible key-value store)
    custom_preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional user-defined preferences"
    )

    # Learning metadata
    learning_enabled: bool = Field(True, description="Enable preference learning")
    total_plans_generated: int = Field(0, description="Total plans generated")
    total_feedback_received: int = Field(0, description="Total feedback instances")
    last_plan_date: Optional[datetime] = Field(None, description="Last planning date")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "timezone": "America/New_York",
                "working_hours": {
                    "start_time": "09:00:00",
                    "end_time": "17:00:00",
                    "break_duration": 1.0
                },
                "prefer_morning_deep_work": True,
                "max_daily_work_hours": 8.0
            }
        }
