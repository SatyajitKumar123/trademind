import tempfile
from pathlib import Path

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trades.models import UploadedTradeFile, UploadJob
from trades.services.file_hashing import compute_file_hash
from trades.tasks import process_tradebook

from .job_serializers import UploadJobSerializer
from .serializers import TradeUploadSerializer


class TradeUploadAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = TradeUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]
        broker = serializer.validated_data["broker"]

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

        job = UploadJob.objects.create(
            user=request.user,
            file_name=file.name,
            status=UploadJob.Status.PENDING,
        )

        # Save file to a temporary location
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        for chunk in file.chunks():
            tmp.write(chunk)

        file_path = Path(tmp.name)

        # Queue background job
        process_tradebook.delay(
            job_id=job.id,
            user_id=request.user.id,
            file_path=str(file_path),
            broker=broker,
        )

        return Response(
            {
                "job_id": job.id,
                "status": job.status,
                "detail": "Upload accepted. Processing in background.",
            },
            status=status.HTTP_202_ACCEPTED,
        )


class UploadJobDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        job = get_object_or_404(
            UploadJob,
            id=job_id,
            user=request.user,
        )

        serializer = UploadJobSerializer(job)
        return Response(serializer.data)
