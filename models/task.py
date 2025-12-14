"""Task model for representing user tasks."""

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    """Task completion status."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class Task(BaseModel):
    """Represents a user task to be scheduled."""

    id: Optional[str] = None
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Detailed task description")
    priority: Priority = Field(Priority.MEDIUM, description="Task priority")
    estimated_duration: float = Field(..., description="Estimated duration in hours")
    deadline: Optional[datetime] = Field(None, description="Task deadline")

    # Preferences
    preferred_time_of_day: Optional[str] = Field(
        None,
        description="Preferred time: morning, afternoon, evening"
    )
    requires_deep_focus: bool = Field(False, description="Requires uninterrupted focus")
    can_split: bool = Field(True, description="Can be split into multiple sessions")
    min_session_duration: Optional[float] = Field(
        None,
        description="Minimum session duration if split (hours)"
    )

    # Status tracking
    status: TaskStatus = Field(TaskStatus.PENDING, description="Current task status")
    actual_duration: Optional[float] = Field(None, description="Actual time taken (hours)")
    scheduled_start: Optional[datetime] = Field(None, description="Scheduled start time")
    scheduled_end: Optional[datetime] = Field(None, description="Scheduled end time")
    actual_start: Optional[datetime] = Field(None, description="Actual start time")
    actual_end: Optional[datetime] = Field(None, description="Actual completion time")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str] = Field(default_factory=list, description="Task tags/categories")
    dependencies: list[str] = Field(
        default_factory=list,
        description="List of task IDs this task depends on"
    )

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "title": "Complete project report",
                "description": "Finish Q4 analysis and recommendations",
                "priority": "high",
                "estimated_duration": 3.5,
                "deadline": "2025-12-20T17:00:00",
                "preferred_time_of_day": "morning",
                "requires_deep_focus": True,
                "tags": ["work", "reports"]
            }
        }
