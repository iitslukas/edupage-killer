from rest_framework import serializers
from .models import Subject, Room, Period, TimetableEntry, SubstitutionEntry


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name", "short_name", "color")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "capacity", "building", "floor")


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ("id", "number", "start_time", "end_time", "name")


class TimetableEntrySerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    teacher_name = serializers.CharField(source="teacher.full_name", read_only=True)
    room_name = serializers.CharField(source="room.name", read_only=True)
    period_info = PeriodSerializer(source="period", read_only=True)

    class Meta:
        model = TimetableEntry
        fields = (
            "id", "subject", "teacher", "teacher_name", "school_class",
            "room", "room_name", "period", "period_info", "day",
            "week_type", "valid_from", "valid_until",
        )


class SubstitutionEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstitutionEntry
        fields = "__all__"
