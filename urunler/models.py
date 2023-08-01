from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Product(models.Model):
    owner = models.ForeignKey(User, verbose_name=("Satıcı"), on_delete=models.CASCADE)
    name = models.CharField(("Ürün İsmi"), max_length=100)
    content = models.TextField(("Ürün Açıklaması"))
    price = models.IntegerField(("Ürün Fiyatı"))
    image = models.ImageField(("Ürün Resmi"), upload_to='products/')
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.replace('ı','i'))
        super(Product,self).save(*args, **kwargs)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = 'Ürünler'
        verbose_name = 'Ürün'



class ShopCard(models.Model):
    owner = models.ForeignKey(User, verbose_name=("Ekleyen"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=("Eklenen Ürün"), on_delete=models.CASCADE)
    count = models.IntegerField(default=1,verbose_name='Adet')
    totalPrice = models.IntegerField(verbose_name='Toplam Fiyat')
    isPayment = models.BooleanField(default=False, verbose_name='Ödendi mi?')
    created_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'Sepetteki Ürünler'
        verbose_name = 'Sepet'