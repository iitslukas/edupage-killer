from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # REST auth
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/social/", include("allauth.socialaccount.urls")),
    # App REST APIs
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/timetable/", include("apps.timetable.urls")),
    path("api/attendance/", include("apps.attendance.urls")),
    path("api/materials/", include("apps.materials.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/assignments/", include("apps.assignments.urls")),
    path("api/notes/", include("apps.notes.urls")),
    path("api/edupage-sync/", include("apps.edupage_sync.urls")),
    # GraphQL
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
