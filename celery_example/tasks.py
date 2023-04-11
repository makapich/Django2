from bs4 import BeautifulSoup

from celery import shared_task

from django.core.mail import send_mail as django_send_mail

import requests

from .models import Author, Quote


@shared_task
def send_mail(subject, message, from_email, to_email):
    django_send_mail(subject, message, from_email, to_email)


@shared_task
def quotes_parser():
    saved_quotes_count = 0
    page_number = 1

    while True:
        print(f'Checking the {page_number} page...')  # noqa: T201
        r = requests.get(f'https://quotes.toscrape.com/page/{page_number}')
        soup = BeautifulSoup(r.content, 'html.parser')
        quotes = soup.find_all('div', {'class': 'quote'})

        for quote in quotes:
            if saved_quotes_count < 5:
                quote_text = quote.find('span', {'class': 'text'}).text

                if Quote.objects.filter(text=quote_text).exists():
                    continue

                link_to_author = quote.find('a').attrs['href']
                r_author = requests.get('https://quotes.toscrape.com' + link_to_author)
                author_page = BeautifulSoup(r_author.content, 'html.parser')
                author_name = quote.find('small', {'class': 'author'}).text
                author_dob = author_page.find('span', {'class': 'author-born-date'}).text
                author_bio = author_page.find('div', {'class': 'author-description'}).text

                author, _ = Author.objects.get_or_create(name=author_name, date_of_birth=author_dob, bio=author_bio)
                quote = Quote.objects.create(text=quote_text, author=author)

                saved_quotes_count += 1

            else:
                break

        if saved_quotes_count == 5:
            print('Successfully saved 5 quotes. Finishing the task.')  # noqa: T201
            break

        elif soup.find('li', {'class': 'next'}):
            print('Going to the next page...')  # noqa: T201
            page_number += 1

        else:
            print(f'Ran out of quotes: only {saved_quotes_count} saved. Sending a notification email...')  # noqa: T201
            subject = 'No new quotes left'
            message = 'No new quotes left'
            from_email = 'fromemail@example.com'
            to_email = ['toemail@example.com', ]
            send_mail.delay(subject=subject, message=message, from_email=from_email, to_email=to_email)
            break

            