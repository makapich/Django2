from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BookModelForm
from .models import Author, Book, Publisher, Store


def index(request):
    return render(request, 'books/index.html')


@method_decorator(cache_page(10), name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    queryset = Book.objects.select_related('publisher').prefetch_related('authors').all()
    paginate_by = 400


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book.html'
    context_object_name = 'book'
    queryset = Book.objects.select_related('publisher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stores'] = self.object.store_set.all()
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookModelForm
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:book_list')


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookModelForm
    context_object_name = 'book'
    template_name = 'books/book_update.html'
    success_url = reverse_lazy('books:book_list')


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:book_list')


@cache_page(10)
def author_list(request):
    authors = Author.objects.prefetch_related(
        Prefetch('book_set', queryset=Book.objects.only('name'))
    )
    return render(request, 'books/author_list.html', {'authors': authors})


def author(request, pk):
    author_obj = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(authors=author_obj)
    return render(request, 'books/author.html', {'author': author_obj, 'books': books})


def publisher_list(request):
    publishers = Publisher.objects.prefetch_related('book_set')
    return render(request, 'books/publisher_list.html', {'publishers': publishers})


def publisher(request, pk):
    publisher_obj = get_object_or_404(Publisher, pk=pk)
    books = Book.objects.filter(publisher=publisher_obj)
    return render(request, 'books/publisher.html', {'publisher': publisher_obj, 'books': books})


def store_list(request):
    stores = Store.objects.annotate(num_books=Count('books')).all()
    return render(request, 'books/store_list.html', {'stores': stores})


def store(request, pk):
    store_obj = get_object_or_404(Store, pk=pk)
    return render(request, 'books/store.html', {'store': store_obj})
