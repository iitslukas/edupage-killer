from rest_framework import generics, permissions
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import Note
from .serializers import NoteSerializer


class NoteListView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subject", "visibility", "lesson_date"]

    def get_queryset(self):  # type: ignore[override]
        user = self.request.user
        school_class = getattr(getattr(user, "student_profile", None), "school_class", None)
        class_filter = Q(visibility="class", school_class=school_class) if school_class else Q()
        return Note.objects.filter(
            Q(author=user)
            | Q(visibility="school")
            | class_filter
            | Q(shared_with=user)
        ).distinct().order_by("-updated_at")

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(author=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Note.objects.filter(
            Q(author=self.request.user) | Q(shared_with=self.request.user)
        )
