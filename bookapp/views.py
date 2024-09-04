from django.shortcuts import render,redirect
from .models import Book
from .forms import AuthorForm,BookForm
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q

# Create your views here.
def createBook(request):
    if request.method=='POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lists')
    else:
        form = BookForm()
    return render(request,'admin_file/createBook.html',{'form':form})

def createAuthor(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create')
    else:
        form = AuthorForm()
    return render(request,'admin_file/author.html',{'form':form})

def listview(request):
    books = Book.objects.all()
    paginator = Paginator(books,4)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(page_number.num_pages)
    return render(request,'admin_file/listview.html',{'books':books,'page':page})

def detailsView(request,book_id):
    book = Book.objects.get(id=book_id)
    return render(request,'admin_file/detailsview.html',{'book':book})

def updateview(request,book_id):
    book = Book.objects.get(id=book_id)
    if request.method=='POST':
        form = BookForm(request.POST,request.FILES,instance=book)
        if form.is_valid():
            form.save()
            return redirect('lists')
    else:
        form = BookForm(instance=book)
    return render(request,'admin_file/updateview.html',{'book':book,'form':form})

def deleteview(request,book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('lists')
    return render(request,'admin_file/deleteview.html',{'book':book})

def searchBooks(request):
    query = None
    books = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books = []
    return render(request,'admin_file/search.html',{'books':books,'query':query})