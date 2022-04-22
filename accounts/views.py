from django.shortcuts import render
from django.http import HttpResponse
from .models import*
# Create your views here.
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()
    delivered=orders.filter(status='delivered').count()
    pending=orders.filter(status='pending').count()
    out_delivery=orders.filter(status='out for delivery').count()

    context={'orders':orders,'customers':customers,
    'total_customers':total_customers,'total_orders':total_orders,
    "delivered":delivered,"pending":pending,'out_delivery':out_delivery}

    return render(request,'accounts/dashboard.html',context)


def products(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)

def customer_info(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_orders=orders.count()
    products=Product.objects.all()
    print(products)
    total_products=products.count()
    context={'customers':customers,'orders':orders,'total_orders':total_orders,'products':products,'total_products':total_products}
    return render(request,'accounts/all_customers.html',context)

def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)

    orders=customer.order_set.all()
    order_count=orders.count()
    
    # products=Product.order_set.all()

    context={'customer':customer,'orders':orders,'order_count':order_count}
    return render(request,'accounts/customers.html',context)
   
