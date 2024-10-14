from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class About(models.Model):
    text = models.TextField()
    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    description = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username}s cart'


class News(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='news_images', blank=True, null=True)
    content = models.TextField()
    summary = models.TextField(default="")

    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='vacancy_images', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    video = models.FileField(upload_to='company_videos/', null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    legal_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=20)
    bank_details = models.TextField()
    sertificate = models.FileField(upload_to='company_sertificate', null=True, blank=True)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=50)
    website = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners_logos', null=True, blank=True)

    def __str__(self):
        return self.name


class FAQEntry(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.date}"
