from datetime import timedelta

from django.utils import timezone

from apps.assignments.models import Assignment


class TestAssignmentIsOverdue:
    def test_is_overdue_when_due_date_in_past(self) -> None:
        a = Assignment(due_date=timezone.now() - timedelta(days=1))
        assert a.is_overdue is True

    def test_not_overdue_when_due_date_in_future(self) -> None:
        a = Assignment(due_date=timezone.now() + timedelta(days=1))
        assert a.is_overdue is False
