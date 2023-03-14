from django.db import models
from Accounts.models import Account
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .constants import PaymentStatus, DeliveryStatus, RequestStatus, generate_request_number, generate_order_number
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import requests
import json



class Type(models.Model):
    type_name = models.CharField(max_length=100, unique=True ,default=False, choices=[
        ('Bambusa guvi', 'Bambusa guvi'),
        ('Bambusa bambua', 'Bambusa bambua'),
        ('Bambusa burmanica', 'Bambusa burmanica'),
        ('Bambusa vulgaris', 'Bambusa vulgaris'),
        ('Bambusa tulda', 'Bambusa tulda'),
    ])

    def __str__(self):
        return self.type_name

    def get_all_types():
        return Type.objects.all()

    def get_type_by_name(type_name):
        try:
            return Type.objects.get(type_name=type_name)
        except Type.DoesNotExist:
            return None


class Warehouse(models.Model):
    w_name = models.CharField(max_length=50)
    address = models.TextField(unique=True, blank=False, null=False)
    city = models.CharField(max_length=20, blank=False)
    state = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=20, blank=False)
    

    def __str__(self):
        return self.country

    def get_all_warehouses():
        return Warehouse.objects.all()

    def get_warehouse_by_id(id):
        try:
            return Warehouse.objects.get(id=id)
        except Warehouse.DoesNotExist:
            return None


    def get_warehouse_by_name(w_name):
        try:
            return Warehouse.objects.get(w_name=w_name)
        except Warehouse.DoesNotExist:
            return None

    def get_warehouse_by_address(address):
        try:
            return Warehouse.objects.get(address=address)
        except Warehouse.DoesNotExist:
            return None




class WarehouseType(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    price_per_unit = models.IntegerField(blank=False, default=50)
    stock_capacity = models.IntegerField(blank=False, default=500)

    def __str__(self):
        return self.warehouse.w_name + ' ' + self.type.type_name

    def get_all_warehouse_types():
        return WarehouseType.objects.all()

    def get_warehouse_type_by_warehouse(warehouse):
        return WarehouseType.objects.filter(warehouse=warehouse)

    def get_warehouse_type_by_type(type):
        return WarehouseType.objects.filter(type=type)


class Request(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=False)
    request_number = models.CharField(max_length=30, default=generate_request_number, unique=True)
    type_name = models.CharField(max_length=100, default=False)
    warehouse = models.CharField(max_length=100, default=False)
    quantity = models.PositiveIntegerField()
    request_type = models.CharField(max_length=20, choices=[
        ('Export', 'Export'),
        ('Import', 'Import')
    ])
    pickup_date = models.DateField(blank=False, null=True)
    pickup_status = models.CharField(max_length=20, null=True, default=PaymentStatus.PENDING)
    is_verfied = models.CharField(max_length=20, default=RequestStatus.PENDING)

    delivery_status = models.CharField(max_length=20,null=True, default=DeliveryStatus.PENDING)
    cname = models.CharField(max_length=50, blank=False, default=False)
    cemail = models.EmailField(max_length=50, blank=False, default=False)
    cphone = models.CharField(max_length=50, blank=False, default=False)
    caddress = models.TextField(blank=False, default=False)
    city = models.CharField(max_length=20, blank=False, default=False)
    state = models.CharField(max_length=20, blank=False, default=False)
    country = models.CharField(max_length=20, blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request_number





class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=False)
    contact_id = models.CharField(max_length=50, blank=True, null=True)
    request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='order')
    order_number = models.CharField(max_length=30, default=generate_order_number, unique=True)
    type_name = models.CharField(max_length=100, default=False)
    warehouse = models.CharField(max_length=100, default=False)
    quantity = models.PositiveIntegerField()
    order_type = models.CharField(max_length=20, choices=[
        ('Export', 'Export'),
        ('Import', 'Import')
    ])
    pickup_date = models.DateField(blank=False, null=True)
    pickup_status = models.CharField(max_length=20, null=True, default='PENDING')
    delivery_status = models.CharField(max_length=20,null=True, default=DeliveryStatus.PENDING)
    contact_id = models.CharField(max_length=50, blank=True, default=None, null=True)
    order_total = models.PositiveIntegerField(blank=True, default=500)
    cname = models.CharField(max_length=50, blank=False, default=False)
    cemail = models.EmailField(max_length=50, blank=False, default=False)
    cphone = models.CharField(max_length=50, blank=False, default=False)
    caddress = models.TextField(blank=False, default=False)
    city = models.CharField(max_length=20, blank=False, default=False)
    state = models.CharField(max_length=20, blank=False, default=False)
    country = models.CharField(max_length=20, blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, null=True, default=PaymentStatus.PENDING)
    reserved_until = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return self.order_number


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True)
    payment_link = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default=PaymentStatus.PENDING)
    amount = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=10, default='INR', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.order_number




@receiver(post_save, sender=Request)
def create_order_for_verified_request(sender, instance, created, **kwargs):
    if not created and instance.is_verfied == 'success':

        try:
            warehouse_type = WarehouseType.objects.get(
                warehouse=Warehouse.objects.get(w_name=instance.warehouse),
                type=Type.objects.get(type_name=instance.type_name)
            )
        except WarehouseType.DoesNotExist:       
            warehouse_type = WarehouseType.objects.create(warehouse=Warehouse.objects.get(w_name=instance.warehouse),
            type=Type.objects.get(type_name=instance.type_name), stock_capacity=500, price_per_unit=50)
            warehouse_type.save()

        print(warehouse_type, '################')
        tax = 0.18  # 18% tax
        quantity = instance.quantity
        price_per_unit = warehouse_type.price_per_unit
        order_total = (quantity * price_per_unit) + tax

        if instance.request_type == 'Import':
            warehouse_type.stock_capacity -= instance.quantity
            warehouse_type.save()
            order = Order.objects.create(
            request=instance,
            user = instance.user,
            type_name=instance.type_name,
            warehouse=instance.warehouse,
            quantity=instance.quantity,
            order_type=instance.request_type,
            order_total=order_total,
            pickup_date=instance.pickup_date,
            pickup_status=instance.pickup_status,
            delivery_status=instance.delivery_status,
            cname=instance.cname,
            cemail=instance.cemail,
            cphone=instance.cphone,
            caddress=instance.caddress,
            city=instance.city,
            state=instance.state,
            country=instance.country,
            reserved_until=timezone.now() + timedelta(hours=24)
            )
            payment = Payment.objects.create(
                user = instance.user,   
                order= order,
                status = PaymentStatus.PENDING,
                amount=order_total,
                currency='INR',
            )
            payment.save()
        elif instance.request_type == 'Export':
            warehouse_type.stock_capacity += instance.quantity
            warehouse_type.save()

            
            order = Order.objects.create(
                request=instance,
                user = instance.user,
                type_name=instance.type_name,
                warehouse=instance.warehouse,
                quantity=instance.quantity,
                order_type=instance.request_type,
                order_total=order_total,
                pickup_date=instance.pickup_date,
                pickup_status=instance.pickup_status,
                delivery_status=instance.delivery_status,
                cname=instance.cname,
                cemail=instance.cemail,
                cphone=instance.cphone,
                caddress=instance.caddress,
                city=instance.city,
                state=instance.state,
                country=instance.country,
                reserved_until=timezone.now() + timedelta(hours=24),
            )

            print(order.cname)
            
            url = "https://api.razorpay.com/v1/contacts"
            data = {
            "name": order.cname,
            "email": order.cemail,
            "contact": order.cemail,
            "type":"customer",
            "reference_id":"Acme Contact ID 12345",
            "notes":{
                "notes_key_1":"Tea, Earl Grey, Hot",
                "notes_key_2":"Tea, Earl Grey… decaf."
            }
            }
            headers = {
                "Content-Type": "application/json"
            }
            auth = ("rzp_test_7XJSI9QBxhtFSQ", "FGTnbTqN5gpIW9MVDJx9TAQJ")
            response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)

            print(response.status_code)
            print(response.json())
            contact_id = response.json().get("id")
            print(contact_id)
            order.contact_id = contact_id
            order.save()

            payment = Payment.objects.create(
                user = instance.user,   
                order= order,
                status = PaymentStatus.PENDING,
                amount=order_total,
                currency='INR',
            )
            payment.save()