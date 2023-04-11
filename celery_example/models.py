from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=50)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text[0:50]}..'