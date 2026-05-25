from django.core.management.base import BaseCommand
from apps.edupage_sync.service import EdupageSyncService
from apps.edupage_sync.models import EdupageSyncJob


class Command(BaseCommand):
    help = "Trigger a full EduPage sync"

    def add_arguments(self, parser):  # type: ignore[override]
        parser.add_argument("--types", nargs="+", default=["timetable", "users", "grades", "homework"])

    def handle(self, *args, **options):  # type: ignore[override]
        self.stdout.write("Starting EduPage sync...")
        job = EdupageSyncJob.objects.create(sync_types=options["types"])
        service = EdupageSyncService()
        results = service.sync_all(job_id=job.pk)
        self.stdout.write(self.style.SUCCESS(f"Sync complete: {results}"))
