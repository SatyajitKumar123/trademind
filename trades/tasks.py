from pathlib import Path

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from trades.models import UploadJob
from trades.services.ingestion_service import ingest_tradebook

User = get_user_model()


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def process_tradebook(self, job_id, user_id, file_path, broker):
    """
    Background task wrapper for ingestion.
    """
    user = User.objects.get(id=user_id)
    job = UploadJob.objects.get(id=job_id)

    job.status = UploadJob.Status.PROCESSING
    job.started_at = timezone.now()
    job.save(update_fields=["status", "started_at"])

    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as f:
            count = ingest_tradebook(user=user, file=f, broker=broker)

        # Mark success
        job.status = UploadJob.Status.DONE
        job.realized_trades_count = count
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "realized_trades_count", "completed_at"])

    except Exception as exc:
        # Mark failure
        job.status = (UploadJob.Status.FAILED,)
        job.error_message = str(exc)
        job.completed_at = timezone.now()
        job.save(update_fields=["status", "error_message", "completed_at"])
        raise

    finally:
        if path.exists():
            path.unlink()
