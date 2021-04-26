from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('App_Login.urls')),
    path('', include('App_Shop.urls')),
    path('shop/', include('App_Order.urls')),
    path('payment/', include('App_Payment.urls')),
    path('contact/', include('App_Contact.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)