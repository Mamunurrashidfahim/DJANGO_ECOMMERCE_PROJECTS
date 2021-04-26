from App_Payment import views
from django.urls import path


app_name="App_Payment"

urlpatterns = [
    path('cheakout/',views.cheakout,name='cheakout'),
    path('pay/',views.payment,name='payment'),
    path('status/',views.complate,name='complate'),
    path('orders/',views.order_view,name='orders'),
    path('purchase/<val_id>/<tran_id>/',views.purchase,name='purchase'),
]
