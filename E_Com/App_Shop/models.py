from django.db import models

class Product(models.Model):
    image =models.ImageField(upload_to='Products')
    name =models.CharField(max_length=264)
    category =models.CharField(max_length=50,default="")
    preview_text =models.TextField(max_length=200,verbose_name='Preview Text')
    detail_text =models.TextField(max_length=1000,verbose_name='Discription')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering =['-created']
