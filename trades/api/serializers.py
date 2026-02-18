from rest_framework import serializers


class TradeUploadSerializer(serializers.Serializer):
    broker = serializers.CharField()
    file = serializers.FileField()

    def validate_broker(self, value: str):
        value = value.lower()

        allowed = ["zerodha"]

        if value not in allowed:
            raise serializers.ValidationError("Unsupported broker")

        return value
