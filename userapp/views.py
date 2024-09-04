from django.shortcuts import render,redirect
from .models import Book
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required
from accounts.models import loginTable
from django.db.models import Q
from .models import Cart,CartItem
from django.db import transaction
import stripe
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
# Create your views here.

def listview(request):
    books = Book.objects.all()
    paginator = Paginator(books,4)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)
    return render(request,'user/userlistview.html',{'books':books,'page':page})

def detailsView(request,book_id):
    book = Book.objects.get(id=book_id)
    return render(request,'user/userdetailsview.html',{'book':book})


def searchBooks(request):
    query = None
    books = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books = []
    return render(request,'user/usersearch.html',{'books':books,'query':query})


def add_to_cart(request,book_id):
    book = Book.objects.get(id=book_id)
    login_user = loginTable.objects.get(username=request.user.username)
    if book.quantity>0:
        #create cart for the specific user
        cart, created = Cart.objects.get_or_create(user=login_user)
        #for cart item
        cart_item,item_created = CartItem.objects.get_or_create(cart=cart,book=book)

        if not item_created:
            cart_item.quantity+=1
            cart_item.save()
    return redirect('viewcartuser')


@login_required
def view_cart_user(request):
    with transaction.atomic():
        login_user, created = loginTable.objects.get_or_create(
        username=request.user.username,
        defaults={
            'password': request.user.password,
            'cpassword': request.user.password,
            'type': 'user'
        }
        )
        cart,created = Cart.objects.get_or_create(user=login_user)
    # This line fetches all CartItem objects associated with the specific cart instance and stores them in the cart_items variable.
    #this line retrieve all items related to a specific cart
    cart_items = cart.cartitem_set.all()
    #retrieves all items from cartitem regardless of which cart they belong to
    cart_item = CartItem.objects.all()
    total_price = sum(item.quantity * item.book.price  for item in cart_items)
    total_items = cart_items.count()

    return render(request,'user/usercart.html',{'cart_items':cart_items,'cart_item':cart_item,'total_price':total_price,'total_items':total_items})


def view_cart_admin(request):
    try:
        # Fetch the current user from the loginTable
        login_user = loginTable.objects.get(username=request.user.username)
        
        
        # Use the fetched user to get or create a cart
        cart, created = Cart.objects.get_or_create(user=login_user)
        
    except loginTable.DoesNotExist:
        messages.error(request, "User entry not found in loginTable.")
        return redirect('login')  # Redirect to login or another appropriate page

    # This line fetches all CartItem objects associated with the specific cart instance and stores them in the cart_items variable.
    #this line retrieve all items related to a specific cart
    cart_items = cart.cartitem_set.all()
    #retrieves all items from cartitem regardless of which cart they belong to
    cart_item = CartItem.objects.all()
    total_price = sum(item.quantity * item.book.price  for item in cart_items)
    total_items = cart_items.count()

    return render(request,'admin_file/admincart.html',{'cart_items':cart_items,'cart_item':cart_item,'total_price':total_price,'total_items':total_items})

def increase_quantity(request,item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity< cart_item.book.quantity:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('viewcartuser')

def decrease_quantity(request,item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity> 1:
        cart_item.quantity-=1
        cart_item.save()
    return redirect('viewcartuser')

def remove_from_cart(request,item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass
    return redirect('viewcartuser')

def create_checkout_session(request):
    cart_items = CartItem.objects.all()
    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.method == 'POST':
            line_items = []
            for item in cart_items:
                if item.book:
                    line_item = {
                        'price_data': {
                            'currency': 'INR',
                            'unit_amount': int(item.book.price*100),
                            'product_data': {
                                'name': item.book.title
                            },
                        },
                        'quantity': 1
                    }
                    line_items.append(line_item)
            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url= request.build_absolute_uri(reverse('success')),
                    cancel_url= request.build_absolute_uri(reverse('cancel'))

                )
                return redirect(checkout_session.url,code=303)
            

def success(request):
    cart_items = CartItem.objects.all()
    for item in cart_items:
        product = item.book
        if product.quantity >= item.quantity:
            product.quantity-=item.quantity
            product.save()
    cart_items.delete()
    return render(request,'user/success.html')

def cancel(request):
    return render(request,'user/cancel.html')
