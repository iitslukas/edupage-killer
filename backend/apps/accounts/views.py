from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, SchoolClass, StudentProfile, TeacherProfile, ParentProfile
from .serializers import (
    UserListSerializer,
    SchoolClassSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
    ParentProfileSerializer,
)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["role"]
    search_fields = ["email", "first_name", "last_name"]

    def get_queryset(self):  # type: ignore[override]
        return User.objects.all().order_by("last_name", "first_name")


class SchoolClassListView(generics.ListCreateAPIView):
    queryset = SchoolClass.objects.all().order_by("grade", "section")
    serializer_class = SchoolClassSerializer
    permission_classes = [permissions.IsAuthenticated]


class SchoolClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentProfileListView(generics.ListAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["school_class"]

    def get_queryset(self):  # type: ignore[override]
        return StudentProfile.objects.select_related("user", "school_class").all()


class TeacherProfileListView(generics.ListAPIView):
    queryset = TeacherProfile.objects.select_related("user").all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> User:  # type: ignore[override]
        return self.request.user  # type: ignore[return-value]
