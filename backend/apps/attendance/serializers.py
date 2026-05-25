from rest_framework import serializers
from .models import AttendanceRecord, AbsenceJustification


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = (
            "id", "student", "student_name", "date", "period", "subject",
            "subject_name", "status", "note", "recorded_by", "created_at",
        )
        read_only_fields = ("recorded_by", "created_at")


class AbsenceJustificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceJustification
        fields = "__all__"
        read_only_fields = ("submitted_by", "submitted_at", "reviewed_by", "approved")
