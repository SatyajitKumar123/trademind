import csv
from typing import IO

from django.db import transaction

from trades.adapters.registry import BROKER_ADAPTERS
from trades.models import Trade


class CSVIngestionError(Exception):
    pass


def ingest_trades_csv(file: IO[str], broker: str) -> int:
    if broker not in BROKER_ADAPTERS:
        raise CSVIngestionError(f"Unsupported broker: {broker}")

    adapter = BROKER_ADAPTERS[broker]
    reader = csv.DictReader(file)

    trades = []

    for row_number, row in enumerate(reader, start=2):
        try:
            dto = adapter.normalize(row)
            trades.append(
                Trade(
                    symbol=dto.symbol,
                    side=dto.side,
                    quantity=dto.quantity,
                    price=dto.price,
                    executed_at=dto.executed_at,
                )
            )
        except Exception as exc:
            raise CSVIngestionError(f"Row {row_number} invalid: {exc}") from exc

    with transaction.atomic():
        Trade.objects.bulk_create(trades)

    return len(trades)
