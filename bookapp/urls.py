from django.urls import path
from . import views
urlpatterns = [
    path('create/',views.createBook,name='create'),
    path('lists/',views.listview,name='lists'),
    path('detailsview/<int:book_id>/',views.detailsView,name='details'),
    path('updateview/<int:book_id>/',views.updateview,name='update'),
    path('delete/<int:book_id>',views.deleteview,name='delete'),
    path('author/',views.createAuthor,name='author'),
    path('search/',views.searchBooks,name='search')
]
