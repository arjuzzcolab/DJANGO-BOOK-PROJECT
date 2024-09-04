
from django.urls import path
from . import views

urlpatterns = [
    path('userlist/',views.listview,name='userlist'),
    path('usersearch/',views.searchBooks,name='usersearch'),
    path('add_cart/<int:book_id>/',views.add_to_cart,name='add_cart'),
    path('view_cart_user/',views.view_cart_user,name='viewcartuser'),
  
    path('increase_item/<int:item_id>/',views.increase_quantity,name='increase_quantity'),
     path('decrease_item/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'),
      path('remove_item/<int:item_id>/',views.remove_from_cart,name='remove_item'),
      path('checkout-session/',views.create_checkout_session,name='checkout_session'),
      path('success/',views.success,name='success'),
      path('cancel/',views.cancel,name='cancel')
]
