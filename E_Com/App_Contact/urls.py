from django.urls import path
from App_Contact import views
app_name='App_Contact'

urlpatterns = [
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
]
