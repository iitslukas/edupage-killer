from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import AttendanceRecord, AbsenceJustification
from .serializers import AttendanceRecordSerializer, AbsenceJustificationSerializer


class AttendanceRecordListView(generics.ListCreateAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["student", "date", "subject", "status"]

    def get_queryset(self):  # type: ignore[override]
        return AttendanceRecord.objects.select_related("student", "subject", "period").all()

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(recorded_by=self.request.user)


class MyAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return AttendanceRecord.objects.filter(student=self.request.user).order_by("-date")


class ClassAttendanceTodayView(generics.ListAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        class_id = self.kwargs["class_id"]
        return AttendanceRecord.objects.filter(
            timetable_entry__school_class_id=class_id,
            date=timezone.now().date(),
        ).select_related("student", "subject", "period")


class AbsenceJustificationView(generics.CreateAPIView):
    serializer_class = AbsenceJustificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(submitted_by=self.request.user)
