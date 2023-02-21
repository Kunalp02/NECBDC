from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from .models import Account
from trycourier import Courier


client = Courier(auth_token="pk_prod_TG1GS5TYWYMN47QGJZGXG1YBXQJM")



def loginUser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'index.html')    
        else:
            messages.warning(request, 'Invalid login credentials')
            return render(request, 'Accounts/loginUser.html')
    return render(request, 'Accounts/loginUser.html')


def signupUser(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        passwd = request.POST['password']
        email = request.POST['email']
        username = email.split('@')[0]
        print(fname, username, passwd, lname)
        try:
            user = Account.objects.create_user(first_name=fname, last_name=lname, email=email, username=username, password=passwd)
            user.save()

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

        except:
            messages.warning(request, 'Email already exists')
            return redirect('signupUser')

        return redirect('loginUser')
    
    return render(request, 'Accounts/signupUser.html')


def logOut(request):
    if request.user is not None:
        auth.logout(request)
        return redirect('index')