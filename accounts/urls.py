from django.urls import path
from . import views


urlpatterns = [

    
    path('register/',views.userRegistration,name='register'),
    path('login/',views.loginPage,name='login'),
  
    path('userview/',views.user_view,name='userview'),
    path('another_view',views.another_view,name='another'),
  
    path('logout/',views.logOutPage,name='logout'),

]
