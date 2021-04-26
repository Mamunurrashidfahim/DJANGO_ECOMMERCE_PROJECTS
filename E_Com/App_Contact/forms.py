from django import forms

from App_Contact.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields =['name','email','phone','message']
