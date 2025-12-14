"""Calendar event model."""

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Type of calendar event."""
    MEETING = "meeting"
    SCHEDULED_TASK = "scheduled_task"
    PERSONAL = "personal"
    BLOCKED = "blocked"
    FREE = "free"


class CalendarEvent(BaseModel):
    """Represents a calendar event (meeting, scheduled task, etc.)."""

    id: Optional[str] = None
    calendar_id: Optional[str] = Field(None, description="External calendar ID (Google/Outlook)")
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event description")

    start_time: datetime = Field(..., description="Event start time")
    end_time: datetime = Field(..., description="Event end time")

    event_type: EventType = Field(EventType.MEETING, description="Type of event")
    location: Optional[str] = Field(None, description="Event location")

    # Linked task (if this is a scheduled task)
    task_id: Optional[str] = Field(None, description="Associated task ID")

    # Metadata
    is_all_day: bool = Field(False, description="All-day event")
    is_recurring: bool = Field(False, description="Recurring event")
    organizer: Optional[str] = Field(None, description="Event organizer")
    attendees: list[str] = Field(default_factory=list, description="Event attendees")

    # Sync info
    source: str = Field("agent", description="Source: agent, google, outlook")
    synced: bool = Field(False, description="Synced to external calendar")
    last_synced: Optional[datetime] = Field(None, description="Last sync timestamp")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "title": "Team standup",
                "start_time": "2025-12-14T09:00:00",
                "end_time": "2025-12-14T09:30:00",
                "event_type": "meeting",
                "attendees": ["team@example.com"]
            }
        }
