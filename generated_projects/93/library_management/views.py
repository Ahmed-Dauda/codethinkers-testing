from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book, Author

class HomeView(ListView):
    template_name = 'home.html'
    model = Book
    paginate_by = 25
    ordering = ['-id']
    
class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 25

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

class BookCreateView(CreateView):
    model = Book
    template_name = 'book_form.html'
    fields = ['title', 'author']
    success_url = '/books/'

class BookUpdateView(UpdateView):
    model = Book
    template_name = 'book_form.html'
    fields = ['title', 'author']
    success_url = '/books/'

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = '/books/'

class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 25

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'

class AuthorCreateView(CreateView):
    model = Author
    template_name = 'author_form.html'
    fields = ['name']
    success_url = '/authors/'

class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'author_form.html'
    fields = ['name']
    success_url = '/authors/'

class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = '/authors/'