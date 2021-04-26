from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=264,blank=False)
    email = models.EmailField(max_length=264,blank=False)
    phone = models.IntegerField(blank=False)
    message = models.TextField(max_length=1000,blank=False)

    def __str__(self):
        return self.name +" sent a message"
