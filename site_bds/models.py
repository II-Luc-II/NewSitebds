from django.db import models


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='galleries/')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Testimonials(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='testimonials/')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Témoignages'
        verbose_name = 'Témoignage'


class Team(models.Model):
    name = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    description = models.TextField()
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='team/')
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Equipe'
        verbose_name = 'Equipe'


class Ask(models.Model):
    ask = models.TextField(max_length=300)
    response = models.TextField(max_length=300)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ask

    class Meta:
        verbose_name_plural = 'Questions clients'
        verbose_name = 'Question client'


class Contact(models.Model):
    name = models.CharField(max_length=60, verbose_name="Nom")
    email = models.EmailField()
    subject = models.CharField(max_length=255, verbose_name="Sujet")
    message = models.TextField()
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
