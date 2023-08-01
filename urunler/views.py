from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def index(request):
    products = Product.objects.all()
    if request.method == "POST":
        if request.user.is_authenticated:
            productId = request.POST.get('productId')
            count = request.POST.get('count')
            product = Product.objects.get(id = productId)
            if ShopCard.objects.filter(owner = request.user,product=product,isPayment=False).exists():
                shop = ShopCard.objects.get(owner = request.user,product=product,isPayment = False)
                shop.count += int(count)
                shop.totalPrice = product.price*shop.count
                shop.save()
            else:
                shop = ShopCard.objects.create(
                    owner = request.user,
                    product = product,
                    count = int(count),
                    totalPrice=product.price*int(count),
                )
                shop.save()
            return redirect('index')
    context = {
        'products':products
    }
    return render(request,'index.html',context)


def detail(request,pk):
    product = Product.objects.get(slug=pk)
    context = {
        'product':product
    }
    return render(request,'detail.html',context)



def cards(request):
    shopcards = ShopCard.objects.filter(owner = request.user,isPayment = False)
    toplam = 0
    for i in shopcards:
        toplam += i.totalPrice
        
    if request.method == 'POST':
        if 'delete' in request.POST:
            cardId = request.POST.get('cardId')
            card = ShopCard.objects.get(id = cardId)
            card.delete()
            return redirect('cards')
    context = {
        'shopcards':shopcards,
        'toplam':toplam,
    }
    return render(request,'shopcards.html',context)