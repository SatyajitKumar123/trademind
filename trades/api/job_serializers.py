from rest_framework import serializers

from trades.models import UploadJob


class UploadJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadJob
        fields = [
            "id",
            "file_name",
            "status",
            "realized_trades_count",
            "error_message",
            "created_at",
            "started_at",
            "completed_at",
        ]
        read_only_fields = fields
