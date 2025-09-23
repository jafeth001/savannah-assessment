import africastalking
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from savannah import settings
from shop.models import Customer, Category, Product, Order, OrderItem
from shop.serializer import CustomerSerializer, CategorySerializer, ProductSerializer, OrderSerializer, \
    OrderItemSerializer


class CustomerList(APIView):
    @staticmethod
    def post(request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if customer exists
        if Customer.objects.filter(email=email).exists():
            return Response({'error': 'Customer already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class CustomerDetail(APIView):
    @staticmethod
    def get(request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    @staticmethod
    def post(request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    @staticmethod
    def get(request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist'}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(APIView):
    @staticmethod
    def post(request):
        try:
            category = request.data.get('category')
            if not category:
                raise ValueError('Category cannot be empty')
            if not Category.objects.filter(pk=category).exists():
                raise ValueError('Category does not exist')
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    @staticmethod
    def get(request, pk):
        try:
            product = Product.objects.select_related('category').get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        try:
            category_id = request.data.get('category')
            if category_id and not Category.objects.filter(pk=category_id).exists():
                return Response({'error': 'Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    @staticmethod
    def post(request):
        try:
            customer_id = request.data.get('customer')
            if not customer_id:
                return Response({'error': 'Customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not Customer.objects.filter(pk=customer_id).exists():
                return Response({'error': 'Customer does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        orders = Order.objects.select_related('customer').all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetail(APIView):
    @staticmethod
    def get(request, pk):
        try:
            order = Order.objects.select_related('customer').get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @staticmethod
    def delete(request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderItemList(APIView):

    @staticmethod
    def post(request):
        try:
            serializer = OrderItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order_item = serializer.save()

            # Fetch related order + customer
            order = order_item.order
            customer = order.customer

            # Send styled HTML email to admin
            subject = f"New Order Item Added to Order #{order.id}"

            # Prepare context for email template
            context = {
                "order": order,
                "order_item": order_item,
                "customer": customer.email
            }

            try:
                html_message = render_to_string("emails/order_item_notification.html", context)
            except Exception:
                # Fallback if template doesn't exist
                html_message = None

            plain_message = (
                f"A new item ({order_item.product.name}) "
                f"was added to Order #{order.id} by {customer.email}"
            )

            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )

            africastalking.initialize(
                username=settings.AFRICASTALKING_USERNAME,
                api_key=settings.AFRICASTALKING_API_KEY
            )
            sms = africastalking.SMS
            message = f"Hello {customer.first_name}, your order #{order.id} has a new item: {order_item.product.name}"
            response = sms.send(message, [customer.phone])
            print("SMS response:", response)


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    @staticmethod
    def delete(request, pk):
        try:
            order_item = OrderItem.objects.get(pk=pk)
            order_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({'error': 'Order item does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
