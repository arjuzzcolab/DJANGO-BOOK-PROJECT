from django.shortcuts import render,redirect
from .models import userProfiles,loginTable
from django.contrib import messages
from django.contrib.auth import logout
from bookapp.models import Book
from django.core.paginator import Paginator,EmptyPage

# Create your views here.

def userRegistration(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')

        if password and cpassword:
            if password == cpassword:
                # Check if the username already exists in userProfiles
                if userProfiles.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('register')
                # Check if the username already exists in loginTable
                elif loginTable.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('register')
                else:
                    userprofile = userProfiles(username=username, password=password, cpassword=cpassword)
                    logintable = loginTable(username=username, password=password, cpassword=cpassword, type='user')
                    userprofile.save()
                    logintable.save()
                    return redirect('login')
            else:
                messages.info(request, 'Password mismatch')
        else:
            messages.info(request, 'All fields are required')
        return redirect('register')
    return render(request, 'authentication/register.html')
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    try:
        if loginTable.objects.filter(username=username,password=password).exists():
            user_details = loginTable.objects.get(username=username,password=password)
            user_name = user_details.username
            user_type = user_details.type

           
            if user_type == 'user':
                request.session['username'] = user_name
                return redirect('userview')
            elif user_type == 'admin':
                request.session['username'] = user_name
                return redirect('lists')
        else:
            messages.error(request,'Username or password does not exist')
    except:
        pass

    return render(request,'authentication/login.html')



def user_view(request):
    books = Book.objects.all()
    username = request.session['username']
    paginator = Paginator(books,4)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)


    return render(request,'user/userlistview.html',{'username':username,'books':books,'page':page})





def another_view(request):
    username = request.POST.get('username')
    # Other context variables
    return render(request, 'admin_file/authorindex.html', {'username': username})



def logOutPage(request):
    logout(request)
    return redirect('login')
            