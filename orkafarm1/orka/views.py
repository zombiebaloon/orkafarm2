from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.core.mail import send_mail
from .utils import cookieCart, cartData, guestOrder


# Create your views here.

def madhu(request):
    return render(request, 'madhu.html')

def error_404(request,exception):
    data = {}
    return render(request,'custom_404.html', data)

def error_500(request):
    data = {}
    return render(request, 'custom_500.html', data)

def index(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request,'index.html',context)

def aboutus(request):
    return render(request,'aboutus.html')

def contact(request):
    contact_message = ''
    error = ''
    msg = ''
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email = request.POST['email']
        s = request.POST['subject']
        message = request.POST['message']
        contact = request.POST['contact']
        contact_message = str('Contact No - ') + str(contact) + str('\n') + str('Subject - ') + str(s) + str('\n') + str('Email - ') + str(message_email) + str("\n") + str(message) 
        try:
            print('no error')
            send_mail(message_name,contact_message,message_email,['madhu.orka@gmail.com'],fail_silently=False)
            contactformemail.objects.create(email=message_email,name=message_name,message=message,subject=s,contact=contact)
            error = 'no'
            msg = message_name
        except:
            error ='yes'
    d = {'error':error,'msg':msg}
    return render(request, 'contact.html',d)

def bulkorders(request):
    contact_message = ''
    error = ''
    msg = ''
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email = request.POST['email']
        message_company = request.POST['company']
        message = request.POST['message']
        city = request.POST['city']
        zipcode = request.POST['ZipCode']
        contact = request.POST['contact']
        product = request.POST['product']
        bulkorder_message = str('Contact No - ') + str(contact) +  str('\n') + str('Email - ') + str(message_email) + str("\n") + str('Product - ') + str(product) + str('\n') + str('Company Name - ') + str(message_company) + str('\n') + str('City - ') + str(city) + str(' - ') + str(zipcode) + str('\n') + str(message)
        try:
            # print('no error')
            # bulkorder.objects.create(name=mes)
            send_mail(message_name,bulkorder_message,message_email,['madhu.orka@gmail.com'],fail_silently=False)
            print("message is working")
            bulkorder.objects.create(name=message_name,email=message_email,company_name=message_company,message=message,city=city,ZipCode=zipcode,contact=contact,product=product)
            error = 'no'
            msg = message_name
            print('no error')
        except:
            error ='yes'
    d = {'error':error,'msg':msg}
    return render(request, 'bulkorder.html',d)

def farm(request):
    return render(request,'farm.html')

def productView(request,id):
    data = cartData(request)
    products = Product.objects.get(id=id)
    cartItems = data['cartItems']
    context = {'products':products,'cartItems':cartItems}
    return render(request,'productview.html',context)

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items,"order":order,'cartItems':cartItems}
    return render(request,'cart.html',context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    

    context = {'items':items,"order":order,'cartItems':cartItems}
    return render(request, 'checkout.html',context)    

def terms(request):
    return render(request,'terms.html')

def policy(request):
    return render(request,'policy.html')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('dataaa',data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            # name = data['shipping']['name'],
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode'],
            )
    return JsonResponse('Payment complete!', safe=False)

# def Login(request):
#     return render(request,'Login.html')


