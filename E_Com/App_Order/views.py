from django.contrib import messages
from App_Order.models import Cart, Order
from App_Shop.models import Product
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def add_to_cart(request,pk):
    item =get_object_or_404(Product,pk=pk)
    order_item =Cart.objects.get_or_create(item=item,user=request.user,purchased=False)
    order_qs =Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order =order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity +=1
            order_item[0].save()
            messages.info(request,"This Item Quantity was Updated.")
            return redirect("App_Shop:home")
        else:
            order.orderitems.add(order_item[0])
            messages.info(request,"This Item added to your Cart.")
            return redirect("App_Shop:home")
    else:
        order =Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request,"This Item added to your Cart.")
        return redirect("App_Shop:home")


@login_required
def cart_view(request):
    carts= Cart.objects.filter(user=request.user,purchased=False)
    orders= Order.objects.filter(user=request.user,ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request,'App_Order/cart.html',context={'carts':carts,'order':order})
    else:
        messages.warning(request,"You Don't have any Item in your Cart")
        return redirect('App_Shop:home')


@login_required
def remove_from_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order =order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item= Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.info(request,"This Item was remove from your Cart.")
            return redirect('App_Order:cart')
        else:
            messages.info(request,"This Item was not in your Cart.")
            return redirect('App_Shop:home')  
    else:
        messages.info(request,"You Don't have any active Order.")
        return redirect('App_Shop:home')

@login_required
def increase_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order =order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item= Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            if order_item.quantity>=1:
                order_item.quantity +=1
                order_item.save()
                messages.info(request,f"{item.name} Quantity has been Updated")
                return redirect('App_Order:cart')
        else:
            messages.info(request,"This Item was not in your Cart.")
            return redirect('App_Shop:home')  
    else:
        messages.info(request,"You Don't have any active Order.")
        return redirect('App_Shop:home')

@login_required
def decrease_cart(request,pk):
    item = get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order =order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item= Cart.objects.filter(item=item,user=request.user,purchased=False)[0]
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request,f"{item.name} Quantity has been Updated")
                return redirect('App_Order:cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(request,f"{item.name} was remove from your Cart.")
                return redirect('App_Shop:home')
        else:
            messages.info(request,"This Item was not in your Cart.")
            return redirect('App_Shop:home')  
    else:
        messages.info(request,"You Don't have any active Order.")
        return redirect('App_Shop:home')