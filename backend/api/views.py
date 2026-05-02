from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
import uuid

from .models import Product, Transaction, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def purchase(request):
    """
    Challenge 01: High-Concurrency Management
    POST /api/purchase/
    Handles concurrent purchase requests with atomic stock management
    """
    try:
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response(
                {'error': 'product_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity <= 0:
            return Response(
                {'error': 'quantity must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use transaction.atomic for concurrency safety
        with transaction.atomic():
            # Use select_for_update to lock the product row
            product = Product.objects.select_for_update().get(id=product_id)
            
            if product.stock < quantity:
                return Response(
                    {
                        'error': f'Insufficient stock. Available: {product.stock}',
                        'available_stock': product.stock
                    },
                    status=status.HTTP_409_CONFLICT
                )

            # Deduct stock
            product.stock -= quantity
            product.save()

            # Record transaction
            trans = Transaction.objects.create(
                product=product,
                quantity=quantity,
                amount=product.price * quantity
            )

        return Response({
            'message': 'Purchase successful',
            'transaction_id': trans.id,
            'product_id': product.id,
            'quantity': quantity,
            'amount': float(trans.amount),
            'remaining_stock': product.stock
        }, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def analytics(request):
    """
    Challenge 02: Big Data Aggregation & Query Optimization
    GET /api/analytics/
    Returns daily revenue for 30 days and top 5 products
    Optimized with database-level aggregations and indexing
    """
    try:
        # Get daily revenue for the last 30 days
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)

        # Optimized query using database aggregation
        daily_revenue = Transaction.objects.filter(
            date__gte=thirty_days_ago
        ).values('date').annotate(
            revenue=Sum(F('amount'), output_field=None)
        ).order_by('date')

        # Get top 5 products by revenue
        top_products = Transaction.objects.filter(
            date__gte=thirty_days_ago
        ).values('product__name', 'product__id').annotate(
            total_revenue=Sum(F('amount'), output_field=None),
            total_quantity=Sum(F('quantity'), output_field=None)
        ).order_by('-total_revenue')[:5]

        return Response({
            'daily_revenue': [
                {
                    'date': str(item['date']),
                    'revenue': float(item['revenue'])
                }
                for item in daily_revenue
            ],
            'top_products': [
                {
                    'product_id': item['product__id'],
                    'product_name': item['product__name'],
                    'revenue': float(item['total_revenue']),
                    'quantity_sold': item['total_quantity']
                }
                for item in top_products
            ],
            'period': f'{thirty_days_ago} to {today}'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def products_list(request):
    """
    GET /api/products/
    Returns list of all products with current stock
    """
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def checkout(request):
    """
    Challenge 03: Mini POS System - Transaction Integrity
    POST /api/checkout/
    Processes checkout with atomic transaction - entire order or nothing
    """
    try:
        cart_items = request.data.get('items', [])
        total_amount = request.data.get('total_amount', 0)

        if not cart_items:
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use transaction.atomic for complete rollback on any error
        with transaction.atomic():
            # Create order
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            order = Order.objects.create(
                order_number=order_number,
                total_amount=total_amount,
                status='pending'
            )

            # Process each cart item
            for item in cart_items:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                unit_price = item.get('unit_price')

                if not product_id or not quantity or not unit_price:
                    raise ValueError('Invalid item data')

                # Lock product and check stock
                product = Product.objects.select_for_update().get(id=product_id)
                
                if product.stock < quantity:
                    raise ValueError(
                        f'Insufficient stock for {product.name}. '
                        f'Available: {product.stock}'
                    )

                # Deduct stock
                product.stock -= quantity
                product.save()

                # Create order item
                subtotal = quantity * float(unit_price)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    subtotal=subtotal
                )

                # Record transaction
                Transaction.objects.create(
                    product=product,
                    quantity=quantity,
                    amount=subtotal
                )

            # Mark order as completed
            order.status = 'completed'
            order.save()

        return Response({
            'message': 'Checkout successful',
            'order_id': order.id,
            'order_number': order.order_number,
            'total_amount': float(order.total_amount),
            'items_count': len(cart_items),
            'status': order.status
        }, status=status.HTTP_201_CREATED)

    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
