from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import ListAPIView
from .models import EntregadorLocalizacao, HistoricoLocalizacao
from .serializers import AtualizarLocalizacaoSerializer,DriverLocationSerializer,DriverRouteSerializer
from core.models import Entregador, Usuario
from core.custom_views import CustomTemplateView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

{
    "lat": -12.62061,
    "lng": -38.31003,
    "speed": 35,
    "heading": 180
}
{
    "lat": -12.70855,
    "lng": -38.30838,
    "speed": 35,
    "heading": 180
}

class TrackingDashboardView(CustomTemplateView):
    template_name = 'tracking/mapa_entregadores.html'

class AtualizarLocalizacaoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AtualizarLocalizacaoSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        usuario = get_object_or_404(
            Usuario,
            user=request.user
        )

        entregador = get_object_or_404(
            Entregador,
            usuario=usuario
        )

        dados = serializer.validated_data

        EntregadorLocalizacao.objects.update_or_create(
            entregador=entregador,
            defaults={
                'latitude': dados['lat'],
                'longitude': dados['lng'],
                'velocidade': dados.get('speed'),
                'heading': dados.get('heading'),
                'disponivel': dados.get('disponivel', True)
            }
        )
        HistoricoLocalizacao.objects.create(
            entregador=entregador,
            latitude=dados['lat'],
            longitude=dados['lng'],
            velocidade=dados.get('speed'),
            heading=dados.get('heading')
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "drivers_tracking",
                {
                    "type": "driver_update",
                    "data": {
                        "entregador_id": entregador.id,
                        "nome": entregador.usuario.user.get_full_name(),
                        "latitude": str(dados['lat']),
                        "longitude": str(dados['lng']),
                        "velocidade": dados.get('speed', 0),
                        "disponivel": entregador.disponivel,
                    }
                }
        )


        return Response({
            'success': True
        }, status=status.HTTP_200_OK)
    
class DriversOnlineAPIView(ListAPIView):
    serializer_class = DriverLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        limite = timezone.now() - timedelta(minutes=10)

        return EntregadorLocalizacao.objects.filter(
            disponivel=True,
            atualizado_em__gte=limite
        ).select_related(
            'entregador',
            'entregador__usuario',
            'entregador__usuario__user'
        )
        
class DriverRouteAPIView(ListAPIView):
    serializer_class = DriverRouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        entregador_id = self.kwargs['entregador_id']

        entregador = get_object_or_404(
            Entregador,
            id=entregador_id
        )

        queryset = HistoricoLocalizacao.objects.filter(
            entregador=entregador
        ).order_by('-registrado_em')[:100]

        return queryset.order_by('registrado_em')
    
class DriverTrackingView(CustomTemplateView):
    template_name = 'tracking/driver_tracking.html'

