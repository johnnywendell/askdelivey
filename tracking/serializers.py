from rest_framework import serializers
from .models import EntregadorLocalizacao, HistoricoLocalizacao


class AtualizarLocalizacaoSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    speed = serializers.FloatField(required=False)
    heading = serializers.FloatField(required=False)
    disponivel = serializers.BooleanField(required=False, default=True)
    
class DriverLocationSerializer(serializers.ModelSerializer):
    entregador_id = serializers.IntegerField(source='entregador.id')
    nome = serializers.CharField(source='entregador.usuario.user.get_full_name')

    class Meta:
        model = EntregadorLocalizacao
        fields = [
            'entregador_id',
            'nome',
            'latitude',
            'longitude',
            'velocidade',
            'heading',
            'disponivel',
            'atualizado_em'
        ]
        
class DriverRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoLocalizacao
        fields = [
            'latitude',
            'longitude',
            'velocidade',
            'heading',
            'registrado_em'
        ]
