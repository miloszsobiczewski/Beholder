from rest_framework import viewsets
from rest_framework import serializers

from moneyball.models import MoneyBall


class MoneyBallSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyBall
        fields = ("json_file", "result")


class MoneyBallViewSet(viewsets.ModelViewSet):
    queryset = MoneyBall.objects.all().order_by("-timestamp")
    serializer_class = MoneyBallSerializer
