from django.views.generic import DetailView
from App_Shop.models import Product
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from math import ceil
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.

def home(request):
    allProds=[]
    catprods= Product.objects.values('category')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
        params={'allProds':allProds }
    return render(request,'App_Shop/home.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.detail_text.lower() or query in item.name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search','')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    if len(allProds) == 0 or len(query)<4:
        messages.warning(request,"Please make sure to enter relevant search query")
    return render(request,'App_Shop/home.html', params)


class ProductDetail(LoginRequiredMixin,DetailView):
    model = Product
    template_name='App_Shop/product_detail.html'
  