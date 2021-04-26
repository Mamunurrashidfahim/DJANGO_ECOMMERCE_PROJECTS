from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from App_Contact.models import Contact
from App_Contact.forms import ContactForm
from django.contrib import messages
from django.urls import reverse

def contact(request):
    form =ContactForm()
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Message sent Successfully!!")
            return HttpResponseRedirect(reverse('App_Shop:home'))
    return render(request,'App_Contact/us.html',context={'form':form})


def about(request):

    return render(request,'App_Contact/about.html',context={})