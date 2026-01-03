"""Database manager for persisting tasks, events, and user profile."""

import json
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config.settings import settings
from models import Task, CalendarEvent, UserProfile

Base = declarative_base()


class TaskDB(Base):
    """Database model for Task."""
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(String, nullable=False)
    estimated_duration = Column(Float, nullable=False)
    deadline = Column(DateTime)
    preferred_time_of_day = Column(String)
    requires_deep_focus = Column(Boolean, default=False)
    can_split = Column(Boolean, default=True)
    min_session_duration = Column(Float)
    status = Column(String, default="pending")
    actual_duration = Column(Float)
    scheduled_start = Column(DateTime)
    scheduled_end = Column(DateTime)
    actual_start = Column(DateTime)
    actual_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(Text)  # JSON array
    dependencies = Column(Text)  # JSON array


class CalendarEventDB(Base):
    """Database model for CalendarEvent."""
    __tablename__ = "calendar_events"

    id = Column(String, primary_key=True)
    calendar_id = Column(String)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    event_type = Column(String, default="meeting")
    location = Column(String)
    task_id = Column(String)
    is_all_day = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)
    organizer = Column(String)
    attendees = Column(Text)  # JSON array
    source = Column(String, default="agent")
    synced = Column(Boolean, default=False)
    last_synced = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserProfileDB(Base):
    """Database model for UserProfile."""
    __tablename__ = "user_profiles"

    user_id = Column(String, primary_key=True)
    timezone = Column(String, default="UTC")
    working_hours = Column(Text)  # JSON
    preferred_calendar = Column(String, default="google")
    prefer_morning_deep_work = Column(Boolean, default=True)
    max_daily_work_hours = Column(Float, default=8.0)
    min_buffer_between_tasks = Column(Float, default=0.25)
    allow_weekend_scheduling = Column(Boolean, default=False)
    productivity_pattern = Column(Text)  # JSON
    schedule_adherence = Column(Text)  # JSON
    custom_preferences = Column(Text)  # JSON
    learning_enabled = Column(Boolean, default=True)
    total_plans_generated = Column(Integer, default=0)
    total_feedback_received = Column(Integer, default=0)
    last_plan_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PlanRefinementDB(Base):
    """Database model for Plan Refinements - tracks user feedback on plans."""
    __tablename__ = "plan_refinements"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    original_plan = Column(Text)  # JSON of original plan
    refinement_request = Column(Text, nullable=False)  # What user asked to change
    refined_plan = Column(Text)  # JSON of refined plan
    feedback_category = Column(String)  # e.g., "timing", "workload", "preferences"
    plan_date = Column(DateTime)  # When the plan was for
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Manages database operations."""

    def __init__(self, database_url: str = None):
        """Initialize database connection."""
        self.database_url = database_url or settings.database_url
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()

    # Task operations
    def save_task(self, task: Task) -> Task:
        """Save or update a task."""
        session = self.get_session()
        try:
            if not task.id:
                task.id = f"task_{datetime.utcnow().timestamp()}"

            task_db = TaskDB(
                id=task.id,
                title=task.title,
                description=task.description,
                priority=task.priority.value if hasattr(task.priority, 'value') else task.priority,
                estimated_duration=task.estimated_duration,
                deadline=task.deadline,
                preferred_time_of_day=task.preferred_time_of_day,
                requires_deep_focus=task.requires_deep_focus,
                can_split=task.can_split,
                min_session_duration=task.min_session_duration,
                status=task.status.value if hasattr(task.status, 'value') else task.status,
                actual_duration=task.actual_duration,
                scheduled_start=task.scheduled_start,
                scheduled_end=task.scheduled_end,
                actual_start=task.actual_start,
                actual_end=task.actual_end,
                tags=json.dumps(task.tags),
                dependencies=json.dumps(task.dependencies),
            )

            existing = session.query(TaskDB).filter_by(id=task.id).first()
            if existing:
                session.delete(existing)
            session.add(task_db)
            session.commit()
            return task
        finally:
            session.close()

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID."""
        session = self.get_session()
        try:
            task_db = session.query(TaskDB).filter_by(id=task_id).first()
            if not task_db:
                return None
            return self._task_from_db(task_db)
        finally:
            session.close()

    def get_all_tasks(self, status: Optional[str] = None) -> List[Task]:
        """Retrieve all tasks, optionally filtered by status."""
        session = self.get_session()
        try:
            query = session.query(TaskDB)
            if status:
                query = query.filter_by(status=status)
            tasks_db = query.all()
            return [self._task_from_db(t) for t in tasks_db]
        finally:
            session.close()

    def _task_from_db(self, task_db: TaskDB) -> Task:
        """Convert database model to Task."""
        return Task(
            id=task_db.id,
            title=task_db.title,
            description=task_db.description,
            priority=task_db.priority,
            estimated_duration=task_db.estimated_duration,
            deadline=task_db.deadline,
            preferred_time_of_day=task_db.preferred_time_of_day,
            requires_deep_focus=task_db.requires_deep_focus,
            can_split=task_db.can_split,
            min_session_duration=task_db.min_session_duration,
            status=task_db.status,
            actual_duration=task_db.actual_duration,
            scheduled_start=task_db.scheduled_start,
            scheduled_end=task_db.scheduled_end,
            actual_start=task_db.actual_start,
            actual_end=task_db.actual_end,
            created_at=task_db.created_at,
            updated_at=task_db.updated_at,
            tags=json.loads(task_db.tags) if task_db.tags else [],
            dependencies=json.loads(task_db.dependencies) if task_db.dependencies else [],
        )

    # Calendar Event operations
    def save_event(self, event: CalendarEvent) -> CalendarEvent:
        """Save or update a calendar event."""
        session = self.get_session()
        try:
            if not event.id:
                event.id = f"event_{datetime.utcnow().timestamp()}"

            event_db = CalendarEventDB(
                id=event.id,
                calendar_id=event.calendar_id,
                title=event.title,
                description=event.description,
                start_time=event.start_time,
                end_time=event.end_time,
                event_type=event.event_type.value if hasattr(event.event_type, 'value') else event.event_type,
                location=event.location,
                task_id=event.task_id,
                is_all_day=event.is_all_day,
                is_recurring=event.is_recurring,
                organizer=event.organizer,
                attendees=json.dumps(event.attendees),
                source=event.source,
                synced=event.synced,
                last_synced=event.last_synced,
            )

            existing = session.query(CalendarEventDB).filter_by(id=event.id).first()
            if existing:
                session.delete(existing)
            session.add(event_db)
            session.commit()
            return event
        finally:
            session.close()

    def get_events(self, start_date: datetime = None, end_date: datetime = None) -> List[CalendarEvent]:
        """Retrieve calendar events within a date range."""
        session = self.get_session()
        try:
            query = session.query(CalendarEventDB)
            if start_date:
                query = query.filter(CalendarEventDB.end_time >= start_date)
            if end_date:
                query = query.filter(CalendarEventDB.start_time <= end_date)
            events_db = query.all()
            return [self._event_from_db(e) for e in events_db]
        finally:
            session.close()

    def _event_from_db(self, event_db: CalendarEventDB) -> CalendarEvent:
        """Convert database model to CalendarEvent."""
        return CalendarEvent(
            id=event_db.id,
            calendar_id=event_db.calendar_id,
            title=event_db.title,
            description=event_db.description,
            start_time=event_db.start_time,
            end_time=event_db.end_time,
            event_type=event_db.event_type,
            location=event_db.location,
            task_id=event_db.task_id,
            is_all_day=event_db.is_all_day,
            is_recurring=event_db.is_recurring,
            organizer=event_db.organizer,
            attendees=json.loads(event_db.attendees) if event_db.attendees else [],
            source=event_db.source,
            synced=event_db.synced,
            last_synced=event_db.last_synced,
            created_at=event_db.created_at,
            updated_at=event_db.updated_at,
        )

    # User Profile operations
    def save_profile(self, profile: UserProfile) -> UserProfile:
        """Save or update user profile."""
        session = self.get_session()
        try:
            profile_db = UserProfileDB(
                user_id=profile.user_id,
                timezone=profile.timezone,
                working_hours=profile.working_hours.model_dump_json(),
                preferred_calendar=profile.preferred_calendar,
                prefer_morning_deep_work=profile.prefer_morning_deep_work,
                max_daily_work_hours=profile.max_daily_work_hours,
                min_buffer_between_tasks=profile.min_buffer_between_tasks,
                allow_weekend_scheduling=profile.allow_weekend_scheduling,
                productivity_pattern=profile.productivity_pattern.model_dump_json(),
                schedule_adherence=profile.schedule_adherence.model_dump_json(),
                custom_preferences=json.dumps(profile.custom_preferences),
                learning_enabled=profile.learning_enabled,
                total_plans_generated=profile.total_plans_generated,
                total_feedback_received=profile.total_feedback_received,
                last_plan_date=profile.last_plan_date,
            )

            existing = session.query(UserProfileDB).filter_by(user_id=profile.user_id).first()
            if existing:
                session.delete(existing)
            session.add(profile_db)
            session.commit()
            return profile
        finally:
            session.close()

    def get_profile(self, user_id: str = "default_user") -> Optional[UserProfile]:
        """Retrieve user profile."""
        session = self.get_session()
        try:
            profile_db = session.query(UserProfileDB).filter_by(user_id=user_id).first()
            if not profile_db:
                # Create default profile
                default_profile = UserProfile(user_id=user_id)
                return self.save_profile(default_profile)
            return self._profile_from_db(profile_db)
        finally:
            session.close()

    def _profile_from_db(self, profile_db: UserProfileDB) -> UserProfile:
        """Convert database model to UserProfile."""
        from models.user_profile import WorkingHoursPreference, ProductivityPattern, ScheduleAdherence

        return UserProfile(
            user_id=profile_db.user_id,
            timezone=profile_db.timezone,
            working_hours=WorkingHoursPreference.model_validate_json(profile_db.working_hours),
            preferred_calendar=profile_db.preferred_calendar,
            prefer_morning_deep_work=profile_db.prefer_morning_deep_work,
            max_daily_work_hours=profile_db.max_daily_work_hours,
            min_buffer_between_tasks=profile_db.min_buffer_between_tasks,
            allow_weekend_scheduling=profile_db.allow_weekend_scheduling,
            productivity_pattern=ProductivityPattern.model_validate_json(profile_db.productivity_pattern),
            schedule_adherence=ScheduleAdherence.model_validate_json(profile_db.schedule_adherence),
            custom_preferences=json.loads(profile_db.custom_preferences) if profile_db.custom_preferences else {},
            learning_enabled=profile_db.learning_enabled,
            total_plans_generated=profile_db.total_plans_generated,
            total_feedback_received=profile_db.total_feedback_received,
            last_plan_date=profile_db.last_plan_date,
            created_at=profile_db.created_at,
            updated_at=profile_db.updated_at,
        )

    # Plan Refinement operations
    def save_plan_refinement(
        self,
        user_id: str,
        original_plan: dict,
        refinement_request: str,
        refined_plan: dict = None,
        feedback_category: str = None,
        plan_date: datetime = None
    ) -> str:
        """Save a plan refinement to track user feedback."""
        session = self.get_session()
        try:
            refinement_id = f"refinement_{datetime.utcnow().timestamp()}"

            refinement_db = PlanRefinementDB(
                id=refinement_id,
                user_id=user_id,
                original_plan=json.dumps(original_plan),
                refinement_request=refinement_request,
                refined_plan=json.dumps(refined_plan) if refined_plan else None,
                feedback_category=feedback_category,
                plan_date=plan_date or datetime.utcnow(),
                created_at=datetime.utcnow()
            )

            session.add(refinement_db)
            session.commit()
            return refinement_id
        finally:
            session.close()

    def get_plan_refinements(
        self,
        user_id: str,
        limit: int = None,
        category: str = None
    ) -> List[dict]:
        """Retrieve plan refinements for a user."""
        session = self.get_session()
        try:
            query = session.query(PlanRefinementDB).filter_by(user_id=user_id)

            if category:
                query = query.filter_by(feedback_category=category)

            query = query.order_by(PlanRefinementDB.created_at.desc())

            if limit:
                query = query.limit(limit)

            refinements_db = query.all()

            return [
                {
                    "id": r.id,
                    "user_id": r.user_id,
                    "original_plan": json.loads(r.original_plan) if r.original_plan else None,
                    "refinement_request": r.refinement_request,
                    "refined_plan": json.loads(r.refined_plan) if r.refined_plan else None,
                    "feedback_category": r.feedback_category,
                    "plan_date": r.plan_date,
                    "created_at": r.created_at
                }
                for r in refinements_db
            ]
        finally:
            session.close()

    def analyze_refinement_patterns(self, user_id: str) -> dict:
        """Analyze common patterns in user's plan refinements."""
        refinements = self.get_plan_refinements(user_id, limit=50)

        if not refinements:
            return {"total_refinements": 0, "patterns": []}

        # Categorize refinements
        categories = {}
        common_keywords = {
            "timing": ["morning", "afternoon", "evening", "time", "earlier", "later"],
            "workload": ["too much", "too many", "reduce", "less", "more", "add"],
            "preferences": ["prefer", "like", "want", "need", "better"],
            "scheduling": ["move", "shift", "reschedule", "change"],
        }

        for ref in refinements:
            request_lower = ref["refinement_request"].lower()

            # Auto-categorize if not already categorized
            if not ref.get("feedback_category"):
                for category, keywords in common_keywords.items():
                    if any(keyword in request_lower for keyword in keywords):
                        categories[category] = categories.get(category, 0) + 1
                        break
            else:
                cat = ref["feedback_category"]
                categories[cat] = categories.get(cat, 0) + 1

        # Find most common patterns
        sorted_patterns = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        return {
            "total_refinements": len(refinements),
            "patterns": [
                {"category": cat, "count": count, "percentage": round(count / len(refinements) * 100, 1)}
                for cat, count in sorted_patterns
            ],
            "recent_requests": [r["refinement_request"] for r in refinements[:5]]
        }
