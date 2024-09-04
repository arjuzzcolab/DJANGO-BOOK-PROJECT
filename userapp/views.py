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


def add_to_cart(request, book_id):
    # Fetch the book object; handle the case where it does not exist
    book = get_object_or_404(Book, id=book_id)
    
    # Retrieve the logged-in user from your custom login model (not request.user)
    username = request.session.get('username')  # Use session data to get the username
    login_user = get_object_or_404(loginTable, username=username)

    # Ensure the book has sufficient quantity before adding to the cart
    if book.quantity > 0:
        # Create a cart for the specific user if not exists
        cart, created = Cart.objects.get_or_create(user=login_user)

        # Get or create a cart item for the specific book
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

        # Increase quantity if item already exists
        if not item_created:
            if cart_item.quantity < book.quantity:  # Ensure we don't exceed available stock
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.error(request, 'Not enough stock available.')
        else:
            cart_item.save()

    return redirect('viewcartuser')

def view_cart_user(request):
    # Retrieve the logged-in user from session (since custom auth is used)
    username = request.session.get('username')  # Fetch username from session
    if not username:
        return redirect('login')  # Redirect to login if no user in session

    # Fetch the logged-in user from the custom login model
    login_user = get_object_or_404(loginTable, username=username)

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=login_user)

    # Fetch all items associated with the cart
    cart_items = cart.cartitem_set.all()

    # Calculate total price and total items
    total_price = sum(item.quantity * item.book.price for item in cart_items)
    total_items = cart_items.count()

    return render(request, 'user/usercart.html', {'cart_items': cart_items, 'total_price': total_price, 'total_items': total_items})


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
