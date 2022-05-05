from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User,Group
from .forms import CustomerForm, OrderForm,CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users
# Create your views here.
@unauthenticated_user
def registerPage(request):
    
    form=CreateUserForm()

    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            
            group=Group.objects.get(name='customer')
            user.groups.add(group)

            # # Customer.objects.create(
            #     user=user,
            #     name=user.username,)

            messages.success(request,'account was created for'+username)
            return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        user = authenticate(request,username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('profile_settings')
    return render(request,'accounts/login.html')

       
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    orders=Order.objects.all()
    last5_orders= Order.objects.all().order_by('-id')[:5]
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

@login_required(login_url='login')
def products(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'accounts/products.html',context)

# update products
#createor add new products
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer_info(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_orders=orders.count()
    products=Product.objects.all()
    # print(products)
    total_products=products.count()
    context={'customers':customers,'orders':orders,'total_orders':total_orders,'products':products,'total_products':total_products}
    return render(request,'accounts/all_customers.html',context)

@login_required(login_url='login')
def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)

    orders=customer.order_set.all()
    order_count=orders.count()
    
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs

    context={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customers.html',context)

#crud operations
@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])

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
            return redirect('profile')
    context={'formset':formset}
    return render(request,"accounts/order_form.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

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

@login_required(login_url='login')
def deleteOrder(request,pk):
        order=Order.objects.get(id=pk)
        if request.method =='POST':
            order.delete()
            return redirect('profile')
        context={'item':order}
        return render(request,"accounts/delete.html",context)

@login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def profile(request):
    # profile=User.objects.get(id=pk)
    # customer=Customer.objects.get(id=pk)
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    delivered=orders.filter(status='delivered').count()
    pending=orders.filter(status='pending').count()
    out_delivery=orders.filter(status='out for delivery').count()

    
    print(orders)

    context={'orders':orders,'total_orders':total_orders,
    "delivered":delivered,"pending":pending,
    'out_delivery':out_delivery}
    return render(request,"accounts/profile.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def profile_settings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method =='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context={'form':form}
    return render(request,"accounts/profile_settings.html",context)