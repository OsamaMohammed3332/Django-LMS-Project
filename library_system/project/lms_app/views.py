from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import BookForm, CategoryForm
# Create your views here.

def index(request):
    if request.method == 'POST':
        add_book = BookForm(request.POST, request.FILES)
        if add_book.is_valid():
            add_book.save()
        
        add_cat = CategoryForm(request.POST)
        if add_cat.is_valid():
            add_cat.save()


    context = {
        'category': Category.objects.all(),
        'books': Book.objects.all(),
        'form': BookForm(),
        'cat': CategoryForm(),
        'allbook': Book.objects.filter(active=True).count(),
        'bookavail': Book.objects.filter(status='available').count(),
        'bookrental': Book.objects.filter(status='rental').count(),
        'booksold': Book.objects.filter(status='sold').count(),
    }
    return render(request, 'pages/index.html', context)


def books(request):
    if request.method =='POST':
        add_cat = CategoryForm(request.POST)
        if add_cat.is_valid():
            add_cat.save()
            
    search = Book.objects.all()
    title = None
    if 'search_name' in request.GET:
        title = request.GET['search_name']
        if title:
            search = search.filter(title__icontains = title)




    context = {
        'category': Category.objects.all(),
        'books': search,
        'cat': CategoryForm(),
    }
    return render(request, 'pages/books.html', context)


def update(request, id):
    book_id = Book.objects.get(id=id)
    if request.method == 'POST':
        book_update = BookForm(request.POST, request.FILES, instance=book_id)
        if book_update.is_valid():
            book_update.save()
            return redirect('/')
    else:
        book_update = BookForm(instance=book_id)

    context = {
        'update': book_update
    }
    return render(request, 'pages/update.html', context)


def delete(request, id):
    book_delete = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book_delete.delete()
        return redirect('/')

    
    return render(request, 'pages/delete.html') 
