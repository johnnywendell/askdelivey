from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404,render, redirect

from core.models import Usuario
from .models import Order
from tracking.models import Entregador
from .serializers import OrderSerializer
from core.custom_views import CustomTemplateView, CreateView, ListView,CustomView, CustomDetailView
from .forms import OrderForm
from django.db import transaction
from django.urls import reverse_lazy,reverse
from django.db.models import Q

############# api views #############
class OrdersDashboardView(CustomTemplateView):
    template_name = "orders/dashboard.html"
    permission_codename = [
        'core.entregador',
    ]
class CreateOrderAPIView(APIView):

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response({
            "success": True,
            "order_id": order.id
        }, status=status.HTTP_201_CREATED)
    
class OrderListAPIView(ListAPIView):

    serializer_class = OrderSerializer
    def get_queryset(self):
        entregador = getattr(self.request.user.perfil,'entregador', None)

        return Order.objects.select_related(
            'entregador',
            'cliente',
            'restaurante'
        ).filter(
            Q(entregador__isnull=True)|
            Q(entregador=entregador) & ~Q(status=Order.Status.DELIVERED)
        ).order_by('-created_at')

class AcceptOrderAPIView(APIView):
    @transaction.atomic
    def post(self, request, pk):
        order = Order.objects.select_for_update().get(pk=pk)

        # verifica se já foi aceito
        if order.entregador is not None:
            return Response({
                'success': False,
                'message': 'Pedido já foi aceito'
            }, status=status.HTTP_400_BAD_REQUEST)

        # busca entregador logado
        usuario = get_object_or_404(
            Usuario,
            user=request.user
        )
        entregador = get_object_or_404(
            Entregador,
            usuario=usuario
        )
        # valida status
        if order.status not in ['approved', 'created']:
            return Response({
                'success': False,
                'message': 'Pedido não disponível'
            }, status=status.HTTP_400_BAD_REQUEST)

        order.entregador = entregador
        order.status = Order.Status.ACCEPTED
        order.save()
        return Response({
            'success': True,
            'message': 'Pedido aceito com sucesso'
        }) 

############### views django ###############

class OrderListView(CustomView, ListView):
    model = Order
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    permission_codename = [
        'core.restaurante',
        'core.entregador',
        'core.cliente',
    ]
    def get_queryset(self):
        user = self.request.user
        
        queryset = Order.objects.select_related(
            'restaurante',
            'entregador',
            'cliente'
        ).all().order_by('-id')
        if user.is_superuser:
            return queryset
        if hasattr(user, 'perfil'):
            tipo = user.perfil.tipo
            # CLIENTE
            if tipo == 'CLIENTE':
                queryset = queryset.filter(
                    cliente=user.perfil.cliente
                )
            # RESTAURANTE
            elif tipo == 'RESTAURANTE':
                queryset = queryset.filter(
                    restaurante=user.perfil.restaurante
                )
            # ENTREGADOR
            elif tipo == 'ENTREGADOR':
                queryset = queryset.filter(
                    entregador=user.perfil.entregador
                )
        else:
            queryset = queryset.none()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(customer_name__icontains=search) |
                Q(restaurante__nome__icontains=search) |
                Q(cliente__nome__icontains=search)
            )
        return queryset

    # 🎯 badge de status
    def get_status_badge(self, status):

        badges = {
            'created': 'secondary',
            'approved': 'info',
            'accepted': 'primary',
            'picking': 'warning',
            'in_transit': 'dark',
            'delivered': 'success',
            'canceled': 'danger',
        }

        return badges.get(status, 'secondary')

    # 🔗 URLs futuras (detail/update)
    def get_urls(self, order):

        return {
            'detail': reverse('orders:order_detail', kwargs={'public_id': order.public_id}) if hasattr(order, 'pk') else '#',
            'update': reverse('orders:order_update', kwargs={'public_id': order.public_id}) if hasattr(order, 'pk') else '#',
        }

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        orders = context['orders']

        for order in orders:
            order.urls = self.get_urls(order)
            order.badge = self.get_status_badge(order.status)

        context['page_title'] = 'Pedidos'
        context['search'] = self.request.GET.get('search', '')

        return context
    
class OrderCreateView(CustomView):
    permission_codename = [
        'core.restaurante',
        'core.cliente',
    ]
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:orders_list')

    def get(self, request, *args, **kwargs):

        context = {
            'order_form': OrderForm(),
            'is_update': False,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        order_form = OrderForm(request.POST)

        print("POST:", request.POST)
        print("ORDER VALID:", order_form.is_valid())
        print("ORDER ERRORS:", order_form.errors)

        if order_form.is_valid():

            order = order_form.save(commit=False)

            # regra: se já criar como restaurante/admin → pode nascer approved
            if order.status == Order.Status.CREATED and order.restaurante:
                order.status = Order.Status.APPROVED

            order.save()

            return redirect(self.success_url)

        context = {
            'order_form': order_form,
            'is_update': False,
        }

        return render(request, self.template_name, context)

class OrderUpdateView(CustomView):
    permission_codename = [
        'core.restaurante',
    ]
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:orders_list')
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'

    def get_object(self):
        return get_object_or_404(
            Order.objects.select_related(
                'restaurante',
                'entregador',
                'cliente'
            ),
            public_id=self.kwargs['public_id']
        )

    def get(self, request, *args, **kwargs):

        order = self.get_object()

        context = {
            'order_form': OrderForm(instance=order),
            'object': order,
            'is_update': True,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):

        order = self.get_object()

        order_form = OrderForm(
            request.POST,
            instance=order
        )

        if order_form.is_valid():

            order = order_form.save(commit=False)

            order.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {
            'order_form': order_form,
            'object': order,
            'is_update': True,
        })
    
class OrderDetailView(CustomDetailView):
    permission_codename = [
        'core.restaurante',
        'core.entregador',
        'core.cliente',
    ]
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'object'
    slug_field = 'public_id'
    slug_url_kwarg = 'public_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    

