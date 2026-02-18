from pathlib import Path

from celery import shared_task
from django.contrib.auth import get_user_model

from trades.services.ingestion_service import ingest_tradebook

User = get_user_model()


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def process_tradebook(self, user_id, file_path, broker):
    """
    Background task wrapper for ingestion.
    """
    user = User.objects.get(id=user_id)
    path = Path(file_path)

    try:
        with path.open(file_path, "r", encoding="utf-8") as f:
            ingest_tradebook(user=user, file=f, broker=broker)

    finally:
        if path.exists():
            path.unlink()
