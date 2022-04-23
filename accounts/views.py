from django.shortcuts import render,redirect
from .models import*
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter

# Create your views here.
def home(request):
    orders=Order.objects.all()
    last5_orders=last_ten = Order.objects.all().order_by('-id')[:5]
    customers=Customer.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()
    delivered=orders.filter(status='delivered').count()
    pending=orders.filter(status='pending').count()
    out_delivery=orders.filter(status='out for delivery').count()

    context={'orders':orders,'last5_orders':last5_orders,'customers':customers,
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
    # print(products)
    total_products=products.count()
    context={'customers':customers,'orders':orders,'total_orders':total_orders,'products':products,'total_products':total_products}
    return render(request,'accounts/all_customers.html',context)

def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)

    orders=customer.order_set.all()
    order_count=orders.count()
    
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs

    context={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customers.html',context)

#crud operations
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        # form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context={'formset':formset}
    return render(request,"accounts/order_form.html",context)


def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)

    if request.method =='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,"accounts/order_form.html",context)


def deleteOrder(request,pk):
        order=Order.objects.get(id=pk)
        if request.method =='POST':
            order.delete()
            return redirect('home')
        context={'item':order}
        return render(request,"accounts/delete.html",context)


