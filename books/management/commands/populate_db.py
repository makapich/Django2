from decimal import Decimal
from random import randint, sample

from books.models import Author, Book, Publisher, Store

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    about = 'fills the db with fixtures'

    def handle(self, *args, **options):
        authors = (Author(name=f"Author {i}", age=randint(20, 80)) for i in range(1, 201))
        Author.objects.bulk_create(authors)

        publishers = (Publisher(name=f"Publisher {i}") for i in range(1, 71))
        Publisher.objects.bulk_create(publishers)

        books = (Book(
            name=f"Book {i}",
            pages=randint(50, 1000),
            price=Decimal(randint(100, 5000) / 100),
            rating=Decimal(randint(1, 50) / 10),
            pubdate=timezone.now().date(),
            publisher=Publisher.objects.order_by("?").first()
        ) for i in range(1, 991))
        Book.objects.bulk_create(books)

        for book in Book.objects.all():
            authors = sample(list(Author.objects.all()), k=randint(1, 2))
            book.authors.set(authors)

        stores = (Store(name=f"Store {i}") for i in range(1, 31))
        Store.objects.bulk_create(stores)

        for store in Store.objects.all():
            books = sample(list(Book.objects.all()), k=randint(50, 100))
            store.books.set(books)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database!'))
