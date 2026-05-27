from rest_framework import serializers
from .models import Order
from tracking.models import Entregador


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['status', 'entregador', 'created_at', 'updated_at']


class AssignOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    entregador_id = serializers.IntegerField()