from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Material, MaterialComment
from .serializers import MaterialSerializer, MaterialCommentSerializer


class MaterialListView(generics.ListCreateAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["subject", "school_class", "material_type", "lesson_date"]

    def get_queryset(self):  # type: ignore[override]
        user = self.request.user
        return Material.objects.filter(
            Q(visibility="class", school_class__students__user=user)
            | Q(visibility="public")
            | Q(uploaded_by=user)
            | Q(shared_with=user)
        ).distinct().order_by("-created_at")

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(uploaded_by=self.request.user)


class MaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # type: ignore[override]
        return Material.objects.all()


class MaterialCommentView(generics.CreateAPIView):
    serializer_class = MaterialCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):  # type: ignore[override]
        serializer.save(
            author=self.request.user,
            material_id=self.kwargs["material_id"],
        )
