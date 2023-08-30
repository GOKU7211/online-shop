from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart, Cart_item
from shop.models import Product


# Create your views here.

def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=cart_id(request)
        )

        cart.save(),
    try:
        cart_item=Cart_item.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except Cart_item.DoesNotExist:
        cart_item=Cart_item.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )

        cart_item.save()
    return redirect('cart:cart_detail')

def cart_detail(request,total=0,counter=0,cart_item=None):
    try:

        cart=Cart.objects.get(cart_id=cart_id(request))
        cart_item=Cart_item.objects.filter(cart=cart,active=True)

        for cart_items in cart_item:
            total +=(cart_items.product.price*cart_items.quantity)
            counter += cart_items.quantity
    except ObjectDoesNotExist:
        pass
    return  render(request,'cart.html',dict(cart_item=cart_item,total=total,counter=counter))


def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cart_item.objects.get(product=product,cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')

def full_remove(request,product_id):
    cart = Cart.objects.get(cart_id=cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart_item.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect('cart:cart_detail')