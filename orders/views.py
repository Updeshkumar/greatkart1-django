import email
from django.shortcuts import render, redirect
from time import strftime
from accounts.models import Account
from carts.models import CartItem
import orders
from .forms import OrderForm
import datetime
from .models import OrderProduct, Orders, Payment,  OrderProduct
from django.http import HttpResponse, JsonResponse
from store.models import Product
import string
import random
import json
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string 
from django.conf import settings





# varification email

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail


def payments(request):
    body = json.loads(request.body)
    print(body)
    order = Orders.objects.get(user=request.user, is_order=False, order_number=body['orderID'])
    #store transations details inside model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    ) 
    payment.save()
    order.payment = payment
    order.is_order = True
    order.save()
    
    # Move the card items products table
    cart_items = CartItem.objects.filter(user = request.user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product.id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
        
    
        # Reduce the quantity of sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    CartItem.objects.filter(user = request.user).delete() 
    
    # send order recive email for customer
    mail_subject = 'Thank you for your Order'
    message = render_to_string('orders/order_recived_email.html', {
        'user': request.user,
        'order': order,
       
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    # Send order number and transaction id back to sendData method by json response
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
        
    }
    return JsonResponse(data)
    # return render(request, 'orders/payments.html')





def place_order(request, total=0, quantity=0):
    context = {}
    current_user = request.user

    #if the cart_count is less then equal to 0 then return redirect back to shop

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax


    if request.method == "POST":
            context = {}
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)

            current_date = d.strftime("%Y%m%d") #20220919
            N = 8
    
            res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
            order_num = str(current_date) + str(res)
            print(order_num)
        
            Orders(
                user = current_user,
                order_number = order_num,
                first_name = request.POST['first_name'],
                last_name = request.POST['Last_name'],
                email = request.POST['email'],
                phone = request.POST['phonenumber'],
                address_line_1 =  request.POST['address_line_1'],
                address_line_2 = request.POST['address_line_2'],
                country = request.POST['country'],
                state = request.POST['state'],
                city = request.POST['city'],
                order_note = request.POST['order_note'],
                order_total = grand_total,
                tax = tax,
                ip = request.META['REMOTE_ADDR']
            ).save()
            orderdetail = Orders.objects.filter(user=current_user)
            # #orderdetail.user = request.orderdetail
            # if len(orderdetail)>0:
            #     print(orderdetail)
            orderdetail = Orders.objects.get(user=current_user, is_order=False, order_number = order_num)
            print(orderdetail)
            context = {
                'order': orderdetail,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
               'grand_total': grand_total,

            }
            print(context)
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')
    
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Orders.objects.get(order_number=order_number, is_order = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)
        
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity
        
        
        payment = Payment.objects.get(payment_id = transID)
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
    
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Orders.DoesNotExist):
        return redirect('home')

        

    