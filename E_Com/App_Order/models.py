from django.db import models

from django.conf import settings
from django.db.models.enums import Choices

from App_Shop.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    purchased =models.BooleanField(default=False)
    created =models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        total =self.item.price * self.quantity
        float_total =format(total,'0.2f')
        return float_total


class Order(models.Model):
    orderitems =models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered =models.BooleanField(default=False)
    created =models.DateTimeField(auto_now_add=True)
    status_name=(
        ("Order confirmed","Order confirmed"),
        ("Picked by courier","Picked by courier"),
        ("On the way","On the way"),
        ("Delivered","Delivered"),
        ("Processing Your Order","Processing Your Order")
    )
    status =models.CharField(choices=status_name,default="Processing Your Order",max_length=50)
    paymentId =models.CharField(max_length=264,blank=True,null=True)
    orderId =models.CharField(max_length=264,blank=True,null=True)

    def get_totals(self):
        total =0
        for order_item in self.orderitems.all():
            total +=float(order_item.get_total())
        return total