from rest_framework import serializers


class MyInfoDataSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)

    class Meta:
        fields = ["code", "state"]
