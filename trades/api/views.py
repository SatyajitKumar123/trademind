from io import TextIOWrapper

from django.db import IntegrityError
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from trades.models import UploadedTradeFile
from trades.services.file_hashing import compute_file_hash
from trades.services.ingestion_service import ingest_tradebook


class TradeUploadAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        broker = request.data.get("broker")

        if not file or not broker:
            return Response(
                {"detail": "file and broker are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_hash = compute_file_hash(file)

        try:
            UploadedTradeFile.objects.create(
                user=request.user,
                original_name=file.name,
                file_hash=file_hash,
            )
        except IntegrityError:
            return Response(
                {"detail": "duplicate file upload prevented"},
                status=status.HTTP_409_CONFLICT,
            )

        text_file = TextIOWrapper(file.file, encoding="utf-8")

        realized = ingest_tradebook(
            user=request.user,
            file=text_file,
            broker=broker,
        )

        return Response(
            {"realized_trades": realized},
            status=status.HTTP_201_CREATED,
        )
