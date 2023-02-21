from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from Accounts.models import Account, UserProfile
from Exporter.models import Warehouse, Request, Type, WarehouseType, Order, Payment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
import razorpay
from pprint import pprint
import math


client = razorpay.Client(auth=("rzp_test_7XJSI9QBxhtFSQ", "FGTnbTqN5gpIW9MVDJx9TAQJ"))



@csrf_exempt
def ExporterLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            try:
                userprofile = UserProfile.objects.get(user=user)
            except:
                userprofile = None
            # print("USERPROFILE", userprofile)
            if userprofile:
                auth.login(request, user)
                return redirect('profile')
            else:
                userprofile = UserProfile.objects.create(user=user)
                userprofile.save()
                auth.login(request, user)
                return redirect('profile')
        else:
            messages.warning(request, 'Invalid login credentials')
            return render(request, 'Exporter/Dashboard/login.html')
    return render(request, 'Exporter/Dashboard/login.html')

@csrf_exempt
def ExporterSignup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = email.split('@')[0]

        print(email, password, confirm_password)
        user = auth.authenticate(email=email, password=password)

        print(user)   
        if user:
            return redirect('ExporterLogin')
        else:
            user = Account.objects.create_user(email=email, password=password, username=username, first_name=fname, last_name=lname)
            userprofile  = UserProfile.objects.create(user=user)
            userprofile.save()
            auth.login(request, user)


            resp = client.send_message(
            message={
                "to": {
                "email": user.email,
                },
                "template": "SF1JQ9JK2SM0AWNW5G5GF5X6FAKE",
                "data": {
                    "name": user.first_name,
                },
            }
            )

            print(resp['requestId'])

            return redirect('profile')
    return render(request, 'Exporter/Dashboard/signup.html')


@login_required(login_url='ExporterLogin')
def Exporterlogout(request):
    auth.logout(request)
    return redirect('ExporterLogin')


@login_required(login_url='ExporterLogin')
def dashboard(request):
    return render(request, 'Exporter/Dashboard/base.html')

@login_required(login_url='ExporterLogin')
@csrf_exempt
def profile(request):
    user = request.user
    userprofile = get_object_or_404(UserProfile, user=request.user)
    print(userprofile)
    if request.method == 'POST':
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        userprofile.city = request.POST.get('city')
        userprofile.state = request.POST.get('state')
        userprofile.country = request.POST.get('country')
        userprofile.address_line_1 = request.POST.get('address_line_1')
        userprofile.address_line_2 = request.POST.get('address_line_2')
        if request.FILES.get('avatar'):
            userprofile.profile_picture = request.FILES.get('avatar')
        userprofile.save()
        user.save()
        return redirect(profile)

    context = {
        'userprofile' : userprofile,
    }
    return render(request, 'Exporter/Dashboard/profile.html', context)

@login_required(login_url='ExporterLogin')
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = Account.objects.get(user=user)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password Updated Successfully')
                auth.logout(request)
                return redirect('ExporterLogin')
            else:
                messages.warning(request,"please enter valid current password")
                return redirect('profile')
        else:
            messages.warning(request, "password does not match")
            return redirect('profile')


    return redirect('profile')

@login_required(login_url='ExporterLogin')
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('ExporterLogin')

@login_required(login_url='ExporterLogin')
def export_request(request):
    if request.method == 'POST':
        user = request.user
        warehouse = request.POST.get('warehouse')
        type_name = request.POST.get('type_name')
        quantity = request.POST.get('quantity')
        cname = request.POST.get('cname')
        cemail = request.POST.get('cemail')
        phone = request.POST.get('cphone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        caddress = request.POST.get('caddress')
        pickup_date = request.POST.get('pickup_date')
        request_type = 'Export'
        print(user, warehouse, type_name, quantity,cname, cemail, city, state, country, pickup_date)

        p_date = datetime.datetime.strptime(pickup_date, '%Y-%m-%d').date()
        today = datetime.date.today()
        
        if p_date <= today:
            error_message = "Pick-up date must be after today's date."
            messages.warning(request, error_message)
            return redirect('export_request')
        

        req = Request(user=user, cname=cname, cemail=cemail, type_name=type_name, quantity=quantity, warehouse=warehouse, city=city, state=state, country=country, caddress=caddress, cphone=phone, pickup_date=pickup_date, request_type=request_type)
        req.save()
        messages.success(request, 'Request Added Successfully')
        return redirect('request_status')
    else:
        context = {
            'warehouses' : Warehouse.objects.all(),
            'types' : Type.objects.all(),
        }
        return render(request, 'Exporter/Dashboard/export_request.html', context)
    
    return render(request, 'Exporter/Dashboard/export_request.html')

def request_status(request):
    if request.user is not None:
        requests = Request.objects.filter(user=request.user)
        print(requests)
        context = {
            'requests' : requests,
        }
        return render(request, 'Exporter/Dashboard/request_status.html', context)
    else:
        return render(request, 'Exporter/Dashboard/request_status.html')



def get_types(request):
    warehouse_id = request.GET.get('warehouse_id')
    warehouse = Warehouse.objects.get(id=warehouse_id)
    warehouse_types = WarehouseType.objects.filter(warehouse=warehouse)
    types_data = []
    for warehouse_type in warehouse_types:
        types_data.append({
        'id': warehouse_type.type.id,
        'type_name': warehouse_type.type.type_name,
        'type_available' : warehouse_type.stock_capacity,
    })
    print(types_data)
    return JsonResponse(types_data, safe=False)



def import_supply(request):
    warehouses = Warehouse.objects.exclude(country='India')
    print(warehouses)
    if request.method == 'POST':
        user = request.user
        wh = request.POST.get('warehouse')
        warehouse = Warehouse.get_warehouse_by_id(wh)
        type_name = request.POST.get('type_name')
        quantity = request.POST.get('quantity')
        cname = request.POST.get('cname')
        cemail = request.POST.get('cemail')
        phone = request.POST.get('cphone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        caddress = request.POST.get('caddress')
        pickup_date = request.POST.get('pickup_date')
        request_type = 'Import'
        # print('######', user, warehouse, type_name, quantity,cname, cemail, city, state, country, pickup_date)
        
        req = Request(user=user, cname=cname, cemail=cemail, type_name=type_name, quantity=quantity, warehouse=warehouse.w_name, city=city, state=state, country=country, caddress=caddress, cphone=phone, request_type=request_type)
        req.save()
        messages.success(request, 'Request Added Successfully')
        return redirect('request_status')
    else:
        context = {
            'warehouses' : warehouses,
        }
        return render(request, 'Exporter/Dashboard/import_supply.html', context)




def stocks(request):
    warehouses = Warehouse.objects.all()
    context = {
        'warehouses' : warehouses,
    }
    return render(request, 'Exporter/Dashboard/stocks.html', context)


def orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders' : orders,
    }
    return render(request, 'Exporter/Dashboard/orders.html', context)

def payments(request):
    payments = Payment.objects.filter(user=request.user)    
    for payment in payments:
        if not payment.payment_id == '':
            payment_status = client.payment_link.fetch(payment_link_id=payment.payment_id)
            payment.status = payment_status['status']
            payment.save()
    context = {
        'payments' : payments,
    }
    return render(request, 'Exporter/Dashboard/payments.html', context)


def send_payment_link(request, order_number):
    order = Order.objects.get(order_number=order_number)
    payment = Payment.objects.get(user=request.user, order=order)
    payment_link = client.payment_link.create({
    "amount": math.ceil((order.order_total)*100),
    "currency": "INR",
    "accept_partial": False,
    "description": "Testing",
    "customer": {
        "name": order.cname,
        "email": order.cemail,
    },
    "notify": {
        "email": True,
    },
    "reminder_enable": True,
    "notes": {
        "delivery": "Deliver to the receptionist"
    },
    "callback_url": "http://127.0.0.1:8000/exporter/dashboard/payments/",
    "callback_method": "get"
    })

    pprint(payment_link)

    payment_id = payment_link["id"]
    payment_link = payment_link["short_url"]
    payment.payment_id = payment_id
    payment.payment_link = payment_link
    payment.amount =  int(math.ceil((order.order_total)))   
    payment.save()
    # Print the short URL
    print("Payment link short URL:", payment_link)
    return redirect('payments')

def send_payout_link(request, order_number):
    order = Order.objects.get(order_number=order_number)
    return redirect('payments')


def invoice(request, order_number):
    try:
        order = Order.objects.get(user=request.user, order_number=order_number)
        wh = Warehouse.objects.get(w_name=order.warehouse)
        context = {
            'order' : order,
            'wh' : wh,
        }
        return render(request, 'Exporter/Dashboard/invoice.html', context)
    except:
        pass
    return render(request, 'Exporter/Dashboard/invoice.html')

