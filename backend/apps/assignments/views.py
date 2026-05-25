from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Assignment, Submission, Grade
from .serializers import AssignmentSerializer, SubmissionSerializer, GradeSerializer


class AssignmentListView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["school_class", "subject", "assignment_type", "is_graded"]

    def get_queryset(self):  # type: ignore[override]
        user = self.request.user
        if hasattr(user, "student_profile") and user.student_profile.school_class:
            return Assignment.objects.filter(school_class=user.student_profile.school_class)
        elif hasattr(user, "teacher_profile"):
            return Assignment.objects.filter(assigned_by=user)
        return Assignment.objects.all()

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(assigned_by=self.request.user)


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubmissionListView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        assignment_id = self.kwargs.get("assignment_id")
        user = self.request.user
        if assignment_id:
            qs = Submission.objects.filter(assignment_id=assignment_id)
            if user.role == "student":
                qs = qs.filter(student=user)
            return qs
        return Submission.objects.filter(student=user)

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(
            student=self.request.user,
            assignment_id=self.kwargs.get("assignment_id"),
        )


class GradeListView(generics.ListCreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subject", "student", "is_final"]

    def get_queryset(self):  # type: ignore[override]
        user = self.request.user
        if user.role == "student":
            return Grade.objects.filter(student=user)
        elif user.role == "teacher":
            return Grade.objects.filter(teacher=user)
        return Grade.objects.all()

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(teacher=self.request.user)
