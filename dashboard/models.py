from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from uuid import uuid4
from django_resized import ResizedImageField



import os 
# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addressLine1 = models.TextField(null=True, blank=True, max_length=200)
    addressLine2 = models.TextField(null=True, blank=True ,max_length=200)
    city = models.TextField(null=True, blank=True, max_length=200)
    state = models.TextField(null=True, blank=True, max_length=200)
    country = models.TextField(null=True, blank=True, max_length=200)
    postalCode = models.TextField(null=True, blank=True, max_length=200)
    profile_image = ResizedImageField(size=[200, 200], quality=90, upload_to='profile_image')





    #Utility Variable
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.username} {self.user.email}"




    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
           


        self.slug = slugify(f"{self.user.first_name} {self.user.username} {self.user.email}")
        self.last_updated = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)


class Blog(models.Model):
    blogIdea = models.CharField(blank=True, null=True, max_length=200)
    title = models.CharField( max_length=200)
    audience = models.CharField(blank=True, null=True, max_length=200)
    keyword = models.CharField(blank=True, null=True, max_length=200)
    word_count = models.CharField(blank=True, null=True, max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    #Utility Variable
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} {self.uniqueId}"




    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
           


        self.slug = slugify(f"{self.title} {self.uniqueId}")
        self.last_updated = timezone.localtime(timezone.now())
        super(Blog, self).save(*args, **kwargs)


class BlogSection(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    word_count = models.CharField(blank=True, null=True,max_length=100)

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    #Utility Variable
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} {self.uniqueId}"




    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
           


        self.slug = slugify(f"{self.title} {self.uniqueId}")
        self.last_updated = timezone.localtime(timezone.now())


        if self.body:
            x = len(self.body.split(' '))
            self.word_count = str(x)
        super(BlogSection, self).save(*args, **kwargs)