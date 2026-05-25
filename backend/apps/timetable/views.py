from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Subject, Room, Period, TimetableEntry, SubstitutionEntry
from .serializers import (
    SubjectSerializer, RoomSerializer, PeriodSerializer,
    TimetableEntrySerializer, SubstitutionEntrySerializer,
)


class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all().order_by("name")
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by("name")
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class PeriodListView(generics.ListCreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = [permissions.IsAuthenticated]


class TimetableEntryListView(generics.ListCreateAPIView):
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["school_class", "teacher", "day", "subject"]

    def get_queryset(self):  # type: ignore[override]
        return TimetableEntry.objects.select_related(
            "subject", "teacher", "room", "period", "school_class"
        ).all()


class MyTimetableView(generics.ListAPIView):
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        user = self.request.user
        if hasattr(user, "student_profile") and user.student_profile.school_class:
            return TimetableEntry.objects.select_related(
                "subject", "teacher", "room", "period"
            ).filter(school_class=user.student_profile.school_class)
        elif hasattr(user, "teacher_profile"):
            return TimetableEntry.objects.select_related(
                "subject", "teacher", "room", "period"
            ).filter(teacher=user)
        return TimetableEntry.objects.none()


class SubstitutionListView(generics.ListCreateAPIView):
    serializer_class = SubstitutionEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["date", "school_class"]

    def get_queryset(self):  # type: ignore[override]
        return SubstitutionEntry.objects.filter(date__gte=timezone.now().date()).order_by("date")
