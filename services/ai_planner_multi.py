"""Multi-provider AI Planning Agent supporting Claude, OpenAI, and Google Gemini."""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum

from models import Task, CalendarEvent, UserProfile, TaskStatus


class AIProvider(str, Enum):
    """Supported AI providers."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"


class TaskPlan(dict):
    """Represents a generated task plan."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduled_tasks: List[Dict[str, Any]] = self.get('scheduled_tasks', [])
        self.reasoning: str = self.get('reasoning', '')
        self.warnings: List[str] = self.get('warnings', [])
        self.suggestions: List[str] = self.get('suggestions', [])


class AIPlannerService:
    """AI-powered planning service supporting multiple providers."""

    def __init__(self, provider: str = "anthropic", api_key: str = None, model_name: str = None):
        """
        Initialize AI planner with specified provider.

        Args:
            provider: AI provider ("anthropic", "openai", or "google")
            api_key: API key for the provider
            model_name: Model name (provider-specific)
        """
        self.provider = AIProvider(provider.lower())
        self.api_key = api_key
        self.conversation_history = []

        # Initialize the appropriate client
        if self.provider == AIProvider.ANTHROPIC:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            self.model = model_name or "claude-sonnet-4-5-20250929"

        elif self.provider == AIProvider.OPENAI:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = model_name or "gpt-4o"

        elif self.provider == AIProvider.GOOGLE:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model_name or "gemini-2.0-flash-exp")
            self.model = model_name or "gemini-2.0-flash-exp"

    def generate_plan(
        self,
        tasks: List[Task],
        calendar_events: List[CalendarEvent],
        user_profile: UserProfile,
        context: Optional[str] = None
    ) -> TaskPlan:
        """
        Generate an optimal task schedule plan using the configured AI provider.

        Args:
            tasks: List of tasks to schedule
            calendar_events: Existing calendar events
            user_profile: User preferences and learned patterns
            context: Additional context or constraints

        Returns:
            TaskPlan containing scheduled tasks and reasoning
        """
        # Build the planning prompt
        prompt = self._build_planning_prompt(tasks, calendar_events, user_profile, context)

        # Call the appropriate AI provider
        try:
            if self.provider == AIProvider.ANTHROPIC:
                plan_text = self._call_anthropic(prompt)
            elif self.provider == AIProvider.OPENAI:
                plan_text = self._call_openai(prompt)
            elif self.provider == AIProvider.GOOGLE:
                plan_text = self._call_google(prompt)

            # Parse the plan
            plan = self._parse_plan_response(plan_text)

            # Store conversation for iterative refinement
            self.conversation_history.append({
                "role": "user",
                "content": prompt
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": plan_text
            })

            return plan

        except Exception as e:
            print(f"Error generating plan with {self.provider}: {e}")
            raise

    def refine_plan(
        self,
        feedback: str,
        previous_plan: TaskPlan
    ) -> TaskPlan:
        """
        Refine an existing plan based on user feedback.

        Args:
            feedback: User's feedback on the plan
            previous_plan: The previously generated plan

        Returns:
            Refined TaskPlan
        """
        refinement_prompt = f"""
Based on my previous plan, please refine it with the following feedback:

{feedback}

Please provide an updated plan that incorporates this feedback while maintaining the same JSON structure.
"""

        try:
            # Call the appropriate AI provider with conversation history
            if self.provider == AIProvider.ANTHROPIC:
                plan_text = self._call_anthropic(refinement_prompt, use_history=True)
            elif self.provider == AIProvider.OPENAI:
                plan_text = self._call_openai(refinement_prompt, use_history=True)
            elif self.provider == AIProvider.GOOGLE:
                plan_text = self._call_google(refinement_prompt, use_history=True)

            refined_plan = self._parse_plan_response(plan_text)

            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": refinement_prompt
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": plan_text
            })

            return refined_plan

        except Exception as e:
            print(f"Error refining plan: {e}")
            raise

    def chat(self, message: str) -> str:
        """
        Simple chat interface with the AI.

        Args:
            message: User message

        Returns:
            AI response
        """
        try:
            if self.provider == AIProvider.ANTHROPIC:
                return self._call_anthropic(message, use_history=True)
            elif self.provider == AIProvider.OPENAI:
                return self._call_openai(message, use_history=True)
            elif self.provider == AIProvider.GOOGLE:
                return self._call_google(message, use_history=True)
        except Exception as e:
            return f"Error: {str(e)}"

    def _call_anthropic(self, prompt: str, use_history: bool = False) -> str:
        """Call Anthropic Claude API."""
        messages = []
        if use_history:
            messages = self.conversation_history.copy()
        messages.append({"role": "user", "content": prompt})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0.7,
            messages=messages
        )
        return response.content[0].text

    def _call_openai(self, prompt: str, use_history: bool = False) -> str:
        """Call OpenAI API."""
        messages = []
        if use_history:
            # Convert history to OpenAI format
            for msg in self.conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=4096
        )
        return response.choices[0].message.content

    def _call_google(self, prompt: str, use_history: bool = False) -> str:
        """Call Google Gemini API."""
        if use_history and self.conversation_history:
            # Build conversation context
            conversation = []
            for msg in self.conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                conversation.append({
                    "role": role,
                    "parts": [msg["content"]]
                })
            conversation.append({
                "role": "user",
                "parts": [prompt]
            })

            # Create chat session
            chat = self.client.start_chat(history=conversation[:-1])
            response = chat.send_message(prompt)
        else:
            response = self.client.generate_content(prompt)

        return response.text

    def _build_planning_prompt(
        self,
        tasks: List[Task],
        calendar_events: List[CalendarEvent],
        user_profile: UserProfile,
        context: Optional[str]
    ) -> str:
        """Build the comprehensive planning prompt."""

        # Format tasks
        tasks_info = []
        for task in tasks:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "estimated_duration": task.estimated_duration,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "preferred_time_of_day": task.preferred_time_of_day,
                "requires_deep_focus": task.requires_deep_focus,
                "can_split": task.can_split,
                "min_session_duration": task.min_session_duration,
                "dependencies": task.dependencies,
                "tags": task.tags
            }
            tasks_info.append(task_dict)

        # Format calendar events
        events_info = []
        for event in calendar_events:
            event_dict = {
                "title": event.title,
                "start_time": event.start_time.isoformat(),
                "end_time": event.end_time.isoformat(),
                "type": event.event_type,
                "is_all_day": event.is_all_day
            }
            events_info.append(event_dict)

        # Format user preferences
        preferences_info = {
            "timezone": user_profile.timezone,
            "working_hours": {
                "start": user_profile.working_hours.start_time.strftime("%H:%M"),
                "end": user_profile.working_hours.end_time.strftime("%H:%M"),
                "break_duration": user_profile.working_hours.break_duration,
                "break_start": user_profile.working_hours.break_start.strftime("%H:%M") if user_profile.working_hours.break_start else None
            },
            "prefer_morning_deep_work": user_profile.prefer_morning_deep_work,
            "max_daily_work_hours": user_profile.max_daily_work_hours,
            "min_buffer_between_tasks": user_profile.min_buffer_between_tasks,
            "allow_weekend_scheduling": user_profile.allow_weekend_scheduling,
            "productivity_pattern": {
                "peak_hours": user_profile.productivity_pattern.peak_hours,
                "low_energy_hours": user_profile.productivity_pattern.low_energy_hours,
                "preferred_task_duration": user_profile.productivity_pattern.preferred_task_duration,
                "average_focus_span": user_profile.productivity_pattern.average_focus_span
            },
            "schedule_adherence": {
                "adherence_rate": user_profile.schedule_adherence.adherence_rate,
                "average_delay_hours": user_profile.schedule_adherence.average_delay_hours
            }
        }

        prompt = f"""You are an expert AI task planning assistant. Your goal is to create an optimal, realistic schedule for the user's tasks based on their calendar, preferences, and learned working patterns.

# TASKS TO SCHEDULE
{json.dumps(tasks_info, indent=2)}

# EXISTING CALENDAR EVENTS
{json.dumps(events_info, indent=2)}

# USER PREFERENCES AND PATTERNS
{json.dumps(preferences_info, indent=2)}

{f"# ADDITIONAL CONTEXT\n{context}\n" if context else ""}

# YOUR TASK
Create an optimal schedule that:
1. Respects all deadlines and priorities
2. Works around existing calendar events
3. Honors user preferences (working hours, deep work times, etc.)
4. Considers learned productivity patterns
5. Accounts for task dependencies
6. Provides realistic time buffers between tasks
7. Allows for breaks and context switching
8. Splits tasks appropriately if they're too long or user prefers it

# IMPORTANT SCHEDULING PRINCIPLES
- High-priority and deadline-critical tasks should be scheduled first
- Deep focus tasks should go in peak productivity hours (morning if prefer_morning_deep_work is true)
- Respect the user's average focus span - don't schedule tasks longer than this without breaks
- If a task can be split and is longer than preferred_task_duration, split it
- Always include min_buffer_between_tasks between consecutive tasks
- Never schedule during existing calendar events
- Stay within working hours unless absolutely necessary for deadlines
- Consider task dependencies - dependent tasks must be scheduled in order

# OUTPUT FORMAT
Provide your response in the following JSON format:

{{
  "reasoning": "Explain your overall scheduling strategy and key decisions",
  "warnings": ["List any concerns, deadline conflicts, or scheduling challenges"],
  "suggestions": ["Suggest improvements to task estimates, priorities, or preferences"],
  "scheduled_tasks": [
    {{
      "task_id": "task_xyz",
      "title": "Task title",
      "scheduled_start": "2025-12-14T09:00:00",
      "scheduled_end": "2025-12-14T11:00:00",
      "duration_hours": 2.0,
      "rationale": "Why scheduled at this time",
      "split_session": 1,
      "total_sessions": 1
    }}
  ]
}}

Make the schedule realistic and achievable. Consider the user's historical adherence rate and adjust accordingly.
"""

        return prompt

    def _parse_plan_response(self, response_text: str) -> TaskPlan:
        """Parse AI response into a structured TaskPlan."""
        try:
            # Try to extract JSON from the response
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text

            # Parse JSON
            plan_data = json.loads(json_text)
            return TaskPlan(plan_data)

        except json.JSONDecodeError as e:
            print(f"Error parsing plan JSON: {e}")
            print(f"Response text: {response_text}")
            # Return a basic plan structure
            return TaskPlan({
                "reasoning": "Failed to parse plan",
                "warnings": ["Could not parse AI response"],
                "suggestions": [],
                "scheduled_tasks": []
            })

    def analyze_deviation(
        self,
        task: Task,
        scheduled_time: datetime,
        actual_completion_time: datetime,
        user_profile: UserProfile
    ) -> Dict[str, Any]:
        """
        Analyze why a task deviated from schedule and learn from it.

        Args:
            task: The completed task
            scheduled_time: When it was scheduled to complete
            actual_completion_time: When it actually completed
            user_profile: User profile for learning

        Returns:
            Analysis with insights and learning updates
        """
        deviation_hours = (actual_completion_time - scheduled_time).total_seconds() / 3600

        prompt = f"""Analyze this task completion deviation to learn the user's working patterns:

TASK: {task.title}
Estimated Duration: {task.estimated_duration} hours
Scheduled Completion: {scheduled_time.isoformat()}
Actual Completion: {actual_completion_time.isoformat()}
Deviation: {deviation_hours:.2f} hours {"early" if deviation_hours < 0 else "late"}

Task Details:
- Priority: {task.priority}
- Required Deep Focus: {task.requires_deep_focus}
- Scheduled Time of Day: {scheduled_time.strftime("%H:%M")}
- Tags: {", ".join(task.tags)}

Current User Profile:
- Peak Hours: {user_profile.productivity_pattern.peak_hours}
- Adherence Rate: {user_profile.schedule_adherence.adherence_rate:.1f}%
- Average Delay: {user_profile.schedule_adherence.average_delay_hours:.2f} hours

Analyze:
1. Why might this deviation have occurred?
2. What does this tell us about the user's working patterns?
3. Should we update any preferences or patterns?
4. What adjustments should we make to future planning?

Provide insights in JSON format:
{{
  "deviation_reason": "Your analysis of why this happened",
  "pattern_insights": ["List of insights about user behavior"],
  "recommended_adjustments": {{
    "update_peak_hours": [9, 10, 11],
    "update_preferred_duration": 2.5,
    "other_updates": {{}}
  }},
  "future_planning_notes": "How to adjust future plans"
}}
"""

        try:
            if self.provider == AIProvider.ANTHROPIC:
                analysis_text = self._call_anthropic(prompt)
            elif self.provider == AIProvider.OPENAI:
                analysis_text = self._call_openai(prompt)
            elif self.provider == AIProvider.GOOGLE:
                analysis_text = self._call_google(prompt)

            # Parse the analysis
            if "```json" in analysis_text:
                json_start = analysis_text.find("```json") + 7
                json_end = analysis_text.find("```", json_start)
                json_text = analysis_text[json_start:json_end].strip()
            else:
                json_text = analysis_text

            analysis = json.loads(json_text)
            return analysis

        except Exception as e:
            print(f"Error analyzing deviation: {e}")
            return {
                "deviation_reason": "Analysis failed",
                "pattern_insights": [],
                "recommended_adjustments": {},
                "future_planning_notes": ""
            }

    def reset_conversation(self):
        """Reset conversation history for a new planning session."""
        self.conversation_history = []
