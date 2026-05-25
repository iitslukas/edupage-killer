from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EdupageSyncJob
from .serializers import EdupageSyncJobSerializer
from .tasks import run_edupage_sync


class SyncJobListView(generics.ListAPIView):
    serializer_class = EdupageSyncJobSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):  # type: ignore[override]
        return EdupageSyncJob.objects.all()[:50]


class TriggerSyncView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):  # type: ignore[override]
        job = EdupageSyncJob.objects.create(
            triggered_by=request.user,
            sync_types=["timetable", "users", "grades", "homework"],
        )
        run_edupage_sync.delay(job.pk)
        return Response({"job_id": job.pk, "status": "queued"}, status=status.HTTP_202_ACCEPTED)
