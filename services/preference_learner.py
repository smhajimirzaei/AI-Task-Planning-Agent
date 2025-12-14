"""Preference learning service to adapt to user behavior over time."""

from datetime import datetime, time
from typing import Dict, Any, List
from collections import defaultdict

from models import Task, UserProfile, TaskStatus


class PreferenceLearner:
    """Learns and adapts user preferences based on behavior."""

    def __init__(self):
        """Initialize preference learner."""
        self.task_completion_data = []
        self.feedback_data = []

    def learn_from_task_completion(
        self,
        task: Task,
        user_profile: UserProfile
    ) -> UserProfile:
        """
        Learn from a completed task and update user profile.

        Args:
            task: Completed task
            user_profile: Current user profile

        Returns:
            Updated user profile
        """
        if not task.actual_start or not task.actual_end:
            return user_profile

        # Update schedule adherence
        user_profile.schedule_adherence.total_tasks_scheduled += 1

        if task.scheduled_end:
            # Calculate deviation
            deviation = (task.actual_end - task.scheduled_end).total_seconds() / 3600

            if abs(deviation) < 0.25:  # Within 15 minutes
                user_profile.schedule_adherence.tasks_completed_on_time += 1
            elif deviation < 0:  # Completed early
                user_profile.schedule_adherence.tasks_completed_early += 1
                user_profile.schedule_adherence.average_early_hours = (
                    (user_profile.schedule_adherence.average_early_hours *
                     (user_profile.schedule_adherence.tasks_completed_early - 1) +
                     abs(deviation)) /
                    user_profile.schedule_adherence.tasks_completed_early
                )
            else:  # Completed late
                user_profile.schedule_adherence.tasks_completed_late += 1
                user_profile.schedule_adherence.average_delay_hours = (
                    (user_profile.schedule_adherence.average_delay_hours *
                     (user_profile.schedule_adherence.tasks_completed_late - 1) +
                     deviation) /
                    user_profile.schedule_adherence.tasks_completed_late
                )

        # Learn productivity patterns
        if task.actual_start and task.actual_end:
            start_hour = task.actual_start.hour
            duration = (task.actual_end - task.actual_start).total_seconds() / 3600

            # Track when tasks are actually completed (productivity indicators)
            # If task was completed on time or early, that time slot is productive
            if task.scheduled_end and task.actual_end <= task.scheduled_end:
                self._update_productive_hours(start_hour, user_profile)

            # Update average focus span
            if task.requires_deep_focus:
                current_avg = user_profile.productivity_pattern.average_focus_span
                # Weighted average: 70% existing, 30% new data
                user_profile.productivity_pattern.average_focus_span = (
                    current_avg * 0.7 + duration * 0.3
                )

        # Update actual duration tracking
        if task.actual_duration:
            # Store for future estimation improvements
            self.task_completion_data.append({
                'estimated': task.estimated_duration,
                'actual': task.actual_duration,
                'priority': task.priority,
                'requires_deep_focus': task.requires_deep_focus,
                'tags': task.tags
            })

        user_profile.updated_at = datetime.utcnow()
        return user_profile

    def learn_from_feedback(
        self,
        feedback: str,
        plan_context: Dict[str, Any],
        user_profile: UserProfile
    ) -> UserProfile:
        """
        Learn from user feedback on generated plans.

        Args:
            feedback: User's feedback text
            plan_context: Context about the plan that was given
            user_profile: Current user profile

        Returns:
            Updated user profile
        """
        user_profile.total_feedback_received += 1

        # Parse feedback for common patterns
        feedback_lower = feedback.lower()

        # Learn time preferences
        if "morning" in feedback_lower:
            if "not" in feedback_lower or "don't" in feedback_lower:
                user_profile.prefer_morning_deep_work = False
            else:
                user_profile.prefer_morning_deep_work = True

        if "afternoon" in feedback_lower or "evening" in feedback_lower:
            if "prefer" in feedback_lower:
                user_profile.prefer_morning_deep_work = False

        # Learn about task duration preferences
        if "too long" in feedback_lower or "shorter" in feedback_lower:
            current = user_profile.productivity_pattern.preferred_task_duration
            user_profile.productivity_pattern.preferred_task_duration = max(0.5, current - 0.5)

        if "longer session" in feedback_lower or "combine" in feedback_lower:
            current = user_profile.productivity_pattern.preferred_task_duration
            user_profile.productivity_pattern.preferred_task_duration = min(4.0, current + 0.5)

        # Learn about buffer preferences
        if "more time between" in feedback_lower or "more buffer" in feedback_lower:
            user_profile.min_buffer_between_tasks = min(1.0, user_profile.min_buffer_between_tasks + 0.25)

        if "less buffer" in feedback_lower or "back to back" in feedback_lower:
            user_profile.min_buffer_between_tasks = max(0, user_profile.min_buffer_between_tasks - 0.25)

        # Store feedback for analysis
        self.feedback_data.append({
            'timestamp': datetime.utcnow(),
            'feedback': feedback,
            'context': plan_context
        })

        user_profile.updated_at = datetime.utcnow()
        return user_profile

    def _update_productive_hours(self, hour: int, user_profile: UserProfile):
        """Update the productive hours list based on successful task completion."""
        peak_hours = user_profile.productivity_pattern.peak_hours

        # Add hour if not already in peak hours
        if hour not in peak_hours:
            peak_hours.append(hour)

        # Keep only top productive hours (max 4 hours)
        # This is a simple heuristic - could be more sophisticated
        if len(peak_hours) > 4:
            # For now, just keep the most recent ones
            # In a more advanced version, we'd track frequency
            peak_hours.pop(0)

        user_profile.productivity_pattern.peak_hours = peak_hours

    def get_task_duration_estimate(
        self,
        task: Task,
        user_profile: UserProfile
    ) -> float:
        """
        Provide an adjusted duration estimate based on learned patterns.

        Args:
            task: Task to estimate
            user_profile: User profile with learned patterns

        Returns:
            Adjusted duration estimate in hours
        """
        base_estimate = task.estimated_duration

        # If we have historical data for similar tasks, adjust
        similar_tasks = [
            t for t in self.task_completion_data
            if (t['priority'] == task.priority or
                t['requires_deep_focus'] == task.requires_deep_focus or
                bool(set(t['tags']) & set(task.tags)))
        ]

        if similar_tasks:
            # Calculate average ratio of actual to estimated
            ratios = [t['actual'] / t['estimated'] for t in similar_tasks if t['estimated'] > 0]
            if ratios:
                avg_ratio = sum(ratios) / len(ratios)
                # Apply a weighted adjustment (50% base, 50% learned)
                adjusted_estimate = base_estimate * (0.5 + 0.5 * avg_ratio)
                return adjusted_estimate

        # If user tends to run late, add buffer
        if user_profile.schedule_adherence.average_delay_hours > 0:
            buffer_factor = 1 + (user_profile.schedule_adherence.average_delay_hours / 10)
            return base_estimate * min(buffer_factor, 1.5)  # Cap at 50% increase

        return base_estimate

    def suggest_optimal_time_slot(
        self,
        task: Task,
        user_profile: UserProfile
    ) -> str:
        """
        Suggest optimal time of day for a task based on learned patterns.

        Args:
            task: Task to schedule
            user_profile: User profile with productivity patterns

        Returns:
            Suggested time slot: 'morning', 'afternoon', or 'evening'
        """
        # If task requires deep focus and user prefers morning deep work
        if task.requires_deep_focus and user_profile.prefer_morning_deep_work:
            return 'morning'

        # Check peak hours
        peak_hours = user_profile.productivity_pattern.peak_hours
        if peak_hours:
            avg_peak_hour = sum(peak_hours) / len(peak_hours)
            if avg_peak_hour < 12:
                return 'morning'
            elif avg_peak_hour < 17:
                return 'afternoon'
            else:
                return 'evening'

        # Default based on task priority
        if task.priority in ['high', 'urgent']:
            return 'morning'
        else:
            return 'afternoon'

    def generate_insights_report(self, user_profile: UserProfile) -> Dict[str, Any]:
        """
        Generate insights report about learned preferences and patterns.

        Args:
            user_profile: User profile to analyze

        Returns:
            Dictionary with insights
        """
        insights = {
            'productivity_summary': {
                'peak_productive_hours': user_profile.productivity_pattern.peak_hours,
                'average_focus_duration': user_profile.productivity_pattern.average_focus_span,
                'preferred_session_length': user_profile.productivity_pattern.preferred_task_duration
            },
            'schedule_adherence': {
                'adherence_rate': user_profile.schedule_adherence.adherence_rate,
                'on_time_completion_rate': (
                    user_profile.schedule_adherence.tasks_completed_on_time /
                    max(user_profile.schedule_adherence.total_tasks_scheduled, 1) * 100
                ),
                'tends_to_run_late': user_profile.schedule_adherence.average_delay_hours > 0.5,
                'tends_to_finish_early': user_profile.schedule_adherence.average_early_hours > 0.5
            },
            'preferences': {
                'prefers_morning_deep_work': user_profile.prefer_morning_deep_work,
                'max_daily_hours': user_profile.max_daily_work_hours,
                'needs_buffer_between_tasks': user_profile.min_buffer_between_tasks,
                'weekend_work_enabled': user_profile.allow_weekend_scheduling
            },
            'learning_stats': {
                'total_plans_generated': user_profile.total_plans_generated,
                'total_feedback_received': user_profile.total_feedback_received,
                'tasks_tracked': user_profile.schedule_adherence.total_tasks_scheduled
            }
        }

        # Add recommendations
        recommendations = []

        if user_profile.schedule_adherence.average_delay_hours > 1:
            recommendations.append(
                "You tend to underestimate task duration. Consider adding 20-30% buffer to estimates."
            )

        if user_profile.schedule_adherence.adherence_rate < 50:
            recommendations.append(
                "Low schedule adherence detected. Consider reducing daily task load or increasing time estimates."
            )

        if not user_profile.productivity_pattern.peak_hours:
            recommendations.append(
                "Complete a few more tasks to learn your peak productivity hours."
            )

        insights['recommendations'] = recommendations

        return insights
