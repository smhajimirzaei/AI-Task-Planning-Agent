"""Calendar integration service for Google Calendar and Outlook."""

import os
import pickle
from datetime import datetime, timedelta
from typing import List, Optional
from abc import ABC, abstractmethod

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from msal import ConfidentialClientApplication

from models import CalendarEvent, EventType
from config.settings import settings


class CalendarServiceBase(ABC):
    """Base class for calendar services."""

    @abstractmethod
    def get_events(self, start_date: datetime, end_date: datetime) -> List[CalendarEvent]:
        """Retrieve events from calendar."""
        pass

    @abstractmethod
    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        """Create an event on the calendar."""
        pass

    @abstractmethod
    def update_event(self, event: CalendarEvent) -> CalendarEvent:
        """Update an existing event."""
        pass

    @abstractmethod
    def delete_event(self, event_id: str) -> bool:
        """Delete an event from the calendar."""
        pass


class GoogleCalendarService(CalendarServiceBase):
    """Google Calendar integration service."""

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        """Initialize Google Calendar service."""
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Google Calendar API."""
        creds = None

        # Check for existing token
        if os.path.exists(settings.google_calendar_token):
            with open(settings.google_calendar_token, 'rb') as token:
                creds = pickle.load(token)

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(settings.google_calendar_credentials):
                    raise FileNotFoundError(
                        f"Google Calendar credentials not found at {settings.google_calendar_credentials}. "
                        "Please download credentials from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.google_calendar_credentials, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(settings.google_calendar_token, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def get_events(self, start_date: datetime, end_date: datetime) -> List[CalendarEvent]:
        """Retrieve events from Google Calendar."""
        if not self.service:
            return []

        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            calendar_events = []

            for event in events:
                calendar_event = self._convert_from_google(event)
                if calendar_event:
                    calendar_events.append(calendar_event)

            return calendar_events

        except Exception as e:
            print(f"Error fetching Google Calendar events: {e}")
            return []

    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        """Create an event on Google Calendar."""
        if not self.service:
            raise RuntimeError("Google Calendar service not initialized")

        google_event = self._convert_to_google(event)

        try:
            created = self.service.events().insert(
                calendarId='primary',
                body=google_event
            ).execute()

            event.calendar_id = created['id']
            event.synced = True
            event.last_synced = datetime.utcnow()
            event.source = 'google'

            return event

        except Exception as e:
            print(f"Error creating Google Calendar event: {e}")
            raise

    def update_event(self, event: CalendarEvent) -> CalendarEvent:
        """Update an existing event on Google Calendar."""
        if not self.service or not event.calendar_id:
            raise RuntimeError("Cannot update event without calendar_id")

        google_event = self._convert_to_google(event)

        try:
            updated = self.service.events().update(
                calendarId='primary',
                eventId=event.calendar_id,
                body=google_event
            ).execute()

            event.synced = True
            event.last_synced = datetime.utcnow()

            return event

        except Exception as e:
            print(f"Error updating Google Calendar event: {e}")
            raise

    def delete_event(self, event_id: str) -> bool:
        """Delete an event from Google Calendar."""
        if not self.service:
            return False

        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            return True

        except Exception as e:
            print(f"Error deleting Google Calendar event: {e}")
            return False

    def _convert_from_google(self, google_event: dict) -> Optional[CalendarEvent]:
        """Convert Google Calendar event to CalendarEvent."""
        try:
            start = google_event['start'].get('dateTime', google_event['start'].get('date'))
            end = google_event['end'].get('dateTime', google_event['end'].get('date'))

            is_all_day = 'date' in google_event['start']

            # Parse datetime
            if is_all_day:
                start_time = datetime.fromisoformat(start)
                end_time = datetime.fromisoformat(end)
            else:
                start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))

            return CalendarEvent(
                calendar_id=google_event['id'],
                title=google_event.get('summary', 'Untitled'),
                description=google_event.get('description'),
                start_time=start_time,
                end_time=end_time,
                event_type=EventType.MEETING,
                location=google_event.get('location'),
                is_all_day=is_all_day,
                is_recurring='recurrence' in google_event,
                organizer=google_event.get('organizer', {}).get('email'),
                attendees=[a.get('email') for a in google_event.get('attendees', [])],
                source='google',
                synced=True,
                last_synced=datetime.utcnow()
            )

        except Exception as e:
            print(f"Error converting Google event: {e}")
            return None

    def _convert_to_google(self, event: CalendarEvent) -> dict:
        """Convert CalendarEvent to Google Calendar event format."""
        google_event = {
            'summary': event.title,
            'description': event.description or '',
            'start': {
                'dateTime': event.start_time.isoformat(),
                'timeZone': settings.default_timezone,
            },
            'end': {
                'dateTime': event.end_time.isoformat(),
                'timeZone': settings.default_timezone,
            },
        }

        if event.location:
            google_event['location'] = event.location

        if event.attendees:
            google_event['attendees'] = [{'email': email} for email in event.attendees]

        return google_event


class OutlookCalendarService(CalendarServiceBase):
    """Outlook Calendar integration service via Microsoft Graph API."""

    def __init__(self):
        """Initialize Outlook Calendar service."""
        self.client_id = settings.microsoft_client_id
        self.client_secret = settings.microsoft_client_secret
        self.tenant_id = settings.microsoft_tenant_id
        self.app = None

        if self.client_id and self.client_secret and self.tenant_id:
            self.authenticate()

    def authenticate(self):
        """Authenticate with Microsoft Graph API."""
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret,
        )

    def get_events(self, start_date: datetime, end_date: datetime) -> List[CalendarEvent]:
        """Retrieve events from Outlook Calendar."""
        # Implementation for Microsoft Graph API
        # This is a placeholder - full implementation requires OAuth flow
        print("Outlook Calendar integration not yet fully implemented")
        return []

    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        """Create an event on Outlook Calendar."""
        print("Outlook Calendar integration not yet fully implemented")
        return event

    def update_event(self, event: CalendarEvent) -> CalendarEvent:
        """Update an existing event on Outlook Calendar."""
        print("Outlook Calendar integration not yet fully implemented")
        return event

    def delete_event(self, event_id: str) -> bool:
        """Delete an event from Outlook Calendar."""
        print("Outlook Calendar integration not yet fully implemented")
        return False


class CalendarService:
    """Unified calendar service that handles multiple calendar providers."""

    def __init__(self, provider: str = "google"):
        """Initialize calendar service with specified provider."""
        self.provider = provider.lower()

        if self.provider == "google":
            self.service = GoogleCalendarService()
        elif self.provider == "outlook":
            self.service = OutlookCalendarService()
        else:
            raise ValueError(f"Unsupported calendar provider: {provider}")

    def get_events(self, start_date: datetime = None, end_date: datetime = None) -> List[CalendarEvent]:
        """Retrieve events from calendar."""
        if not start_date:
            start_date = datetime.utcnow()
        if not end_date:
            end_date = start_date + timedelta(days=30)

        return self.service.get_events(start_date, end_date)

    def create_event(self, event: CalendarEvent) -> CalendarEvent:
        """Create an event on the calendar."""
        return self.service.create_event(event)

    def update_event(self, event: CalendarEvent) -> CalendarEvent:
        """Update an existing event."""
        return self.service.update_event(event)

    def delete_event(self, event_id: str) -> bool:
        """Delete an event from the calendar."""
        return self.service.delete_event(event_id)

    def get_free_slots(self, start_date: datetime, end_date: datetime,
                       duration_hours: float) -> List[tuple[datetime, datetime]]:
        """Find free time slots in the calendar."""
        events = self.get_events(start_date, end_date)

        # Sort events by start time
        events.sort(key=lambda e: e.start_time)

        free_slots = []
        current_time = start_date

        for event in events:
            # Check if there's a gap before this event
            if event.start_time > current_time:
                gap_hours = (event.start_time - current_time).total_seconds() / 3600
                if gap_hours >= duration_hours:
                    free_slots.append((current_time, event.start_time))

            # Move current time to end of this event
            current_time = max(current_time, event.end_time)

        # Check for free time after last event
        if end_date > current_time:
            gap_hours = (end_date - current_time).total_seconds() / 3600
            if gap_hours >= duration_hours:
                free_slots.append((current_time, end_date))

        return free_slots
