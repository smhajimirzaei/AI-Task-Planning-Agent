"""Utility helper functions."""

from datetime import datetime, time, timedelta
from typing import List, Tuple
import pytz


def parse_time_string(time_str: str) -> time:
    """
    Parse a time string to time object.

    Args:
        time_str: Time in format "HH:MM" or "HH:MM:SS"

    Returns:
        time object
    """
    try:
        return time.fromisoformat(time_str)
    except ValueError:
        # Try parsing with strptime
        for fmt in ["%H:%M", "%H:%M:%S", "%I:%M %p"]:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.time()
            except ValueError:
                continue
        raise ValueError(f"Could not parse time string: {time_str}")


def parse_date_string(date_str: str) -> datetime:
    """
    Parse a date string to datetime object.

    Args:
        date_str: Date in various formats

    Returns:
        datetime object
    """
    for fmt in [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
    ]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Could not parse date string: {date_str}")


def get_business_hours(
    start_hour: int = 9,
    end_hour: int = 17,
    timezone_str: str = "UTC"
) -> Tuple[time, time]:
    """
    Get business hours as time objects.

    Args:
        start_hour: Start hour (0-23)
        end_hour: End hour (0-23)
        timezone_str: Timezone string

    Returns:
        Tuple of (start_time, end_time)
    """
    return time(start_hour, 0), time(end_hour, 0)


def is_business_hours(
    dt: datetime,
    start_time: time,
    end_time: time,
    allow_weekends: bool = False
) -> bool:
    """
    Check if datetime falls within business hours.

    Args:
        dt: Datetime to check
        start_time: Business hours start
        end_time: Business hours end
        allow_weekends: Whether weekends are considered business hours

    Returns:
        True if within business hours
    """
    # Check weekend
    if not allow_weekends and dt.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False

    # Check time
    return start_time <= dt.time() <= end_time


def calculate_available_hours(
    start_date: datetime,
    end_date: datetime,
    working_hours_start: time,
    working_hours_end: time,
    allow_weekends: bool = False,
    exclude_dates: List[datetime] = None
) -> float:
    """
    Calculate total available working hours in a date range.

    Args:
        start_date: Start of date range
        end_date: End of date range
        working_hours_start: Daily working hours start
        working_hours_end: Daily working hours end
        allow_weekends: Include weekends
        exclude_dates: Dates to exclude (holidays, etc.)

    Returns:
        Total available hours
    """
    if exclude_dates is None:
        exclude_dates = []

    # Calculate hours per day
    start_minutes = working_hours_start.hour * 60 + working_hours_start.minute
    end_minutes = working_hours_end.hour * 60 + working_hours_end.minute
    hours_per_day = (end_minutes - start_minutes) / 60

    total_hours = 0.0
    current_date = start_date.date()
    end = end_date.date()

    while current_date <= end:
        # Skip excluded dates
        if any(current_date == ex.date() for ex in exclude_dates):
            current_date += timedelta(days=1)
            continue

        # Skip weekends if not allowed
        weekday = datetime.combine(current_date, time()).weekday()
        if not allow_weekends and weekday >= 5:
            current_date += timedelta(days=1)
            continue

        total_hours += hours_per_day
        current_date += timedelta(days=1)

    return total_hours


def format_duration(hours: float) -> str:
    """
    Format duration in hours to human-readable string.

    Args:
        hours: Duration in hours

    Returns:
        Formatted string (e.g., "2h 30m")
    """
    if hours < 0:
        return f"-{format_duration(abs(hours))}"

    h = int(hours)
    m = int((hours - h) * 60)

    if h == 0:
        return f"{m}m"
    elif m == 0:
        return f"{h}h"
    else:
        return f"{h}h {m}m"


def get_time_of_day(dt: datetime) -> str:
    """
    Get time of day category.

    Args:
        dt: Datetime to categorize

    Returns:
        "morning", "afternoon", or "evening"
    """
    hour = dt.hour

    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    else:
        return "evening"


def find_next_available_slot(
    start_time: datetime,
    duration_hours: float,
    busy_slots: List[Tuple[datetime, datetime]],
    working_hours_start: time,
    working_hours_end: time,
    allow_weekends: bool = False
) -> Tuple[datetime, datetime]:
    """
    Find the next available time slot for a task.

    Args:
        start_time: Earliest possible start time
        duration_hours: Required duration
        busy_slots: List of (start, end) tuples for busy periods
        working_hours_start: Daily working hours start
        working_hours_end: Daily working hours end
        allow_weekends: Allow weekend scheduling

    Returns:
        Tuple of (slot_start, slot_end) or (None, None) if no slot found
    """
    current_time = start_time
    max_search_days = 60  # Don't search more than 60 days ahead
    search_end = start_time + timedelta(days=max_search_days)

    # Sort busy slots
    busy_slots = sorted(busy_slots, key=lambda x: x[0])

    while current_time < search_end:
        # Ensure we're in business hours
        if not is_business_hours(current_time, working_hours_start, working_hours_end, allow_weekends):
            # Move to next business day start
            current_time = current_time.replace(
                hour=working_hours_start.hour,
                minute=working_hours_start.minute,
                second=0
            )
            if current_time.weekday() >= 5 and not allow_weekends:
                # Move to Monday
                days_ahead = 7 - current_time.weekday()
                current_time += timedelta(days=days_ahead)
            else:
                current_time += timedelta(days=1)
            continue

        # Calculate potential end time
        potential_end = current_time + timedelta(hours=duration_hours)

        # Check if slot extends beyond working hours
        if potential_end.time() > working_hours_end:
            # Move to next day
            current_time = current_time.replace(
                hour=working_hours_start.hour,
                minute=working_hours_start.minute
            ) + timedelta(days=1)
            continue

        # Check for conflicts with busy slots
        conflict = False
        for busy_start, busy_end in busy_slots:
            # Check if there's overlap
            if current_time < busy_end and potential_end > busy_start:
                conflict = True
                # Move current_time to after this busy slot
                current_time = busy_end
                break

        if not conflict:
            # Found a slot!
            return current_time, potential_end

        # Move forward a bit
        current_time += timedelta(minutes=15)

    # No slot found
    return None, None


def convert_timezone(
    dt: datetime,
    from_tz: str,
    to_tz: str
) -> datetime:
    """
    Convert datetime from one timezone to another.

    Args:
        dt: Datetime to convert
        from_tz: Source timezone
        to_tz: Target timezone

    Returns:
        Converted datetime
    """
    from_zone = pytz.timezone(from_tz)
    to_zone = pytz.timezone(to_tz)

    # Localize if naive
    if dt.tzinfo is None:
        dt = from_zone.localize(dt)

    return dt.astimezone(to_zone)
