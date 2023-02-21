from celery import shared_task


@shared_task(bind=True)
def check_payment(self):
    from .models import Order, Request
    from django.utils import timezone
    from datetime import timedelta

    orders = Order.objects.filter(payment_status='pending')
    if orders:
        for order in orders:
            if timezone.now() > order.reserved_until:
                order.payment_status = 'failed'
                order.save()
                release_stock.apply_async(args=[order.order_number])
                print('Order cancelled')
    else:
        # handle the error, for example by logging or returning a message
        print("No orders match the query")            

@shared_task(bind=True)
def release_stock(self, order_number):
    from .models import Order, WarehouseType, Type, Warehouse
    order = Order.objects.get(order_number=order_number)
    warehouse_type = WarehouseType.objects.get(warehouse=Warehouse.objects.get(w_name=order.warehouse), type=Type.objects.get(type_name=order.type_name))
    warehouse_type.stock_capacity += order.quantity
    warehouse_type.save()
    order.delete()


    