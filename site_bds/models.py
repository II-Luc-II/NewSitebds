from django.db import models
from django.urls import reverse


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='galleries/')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Testimonials(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='testimonials/')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

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
    no_robot = models.BooleanField(default=False, verbose_name="Robot")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Blogs(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre", blank=True, null=True)
    image = models.ImageField(upload_to='images-blogs', blank=True, null=True, verbose_name="Image")
    image_2 = models.ImageField(upload_to='images-blogs', blank=True, null=True, verbose_name="Image 2")
    image_3 = models.ImageField(upload_to='images-blogs', blank=True, null=True, verbose_name="Image 3")
    text = models.TextField(blank=True, null=True)
    text_details = models.TextField(blank=True, null=True, verbose_name="Texte détails")
    text_details_2 = models.TextField(blank=True, null=True, verbose_name="Texte détails 2")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    en_ligne = models.BooleanField(default=False, verbose_name="Publié")

    class Meta:
        verbose_name_plural = 'News'
        verbose_name = 'News'

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('blog_single', args=[self.pk])


class ALaUne(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre", blank=True, null=True)
    text = models.TextField(verbose_name="Texte", blank=True, null=True)
    title_2 = models.CharField(max_length=255, verbose_name="Titre 2", blank=True, null=True)
    text_2 = models.TextField(verbose_name="texte_2", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    en_ligne = models.BooleanField(default=False, verbose_name="Publié")

    class Meta:
        verbose_name_plural = 'A la une'
        verbose_name = 'A la une'


class PopUp(models.Model):
    name = models.CharField(max_length=255, verbose_name="Titre", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(upload_to='Pop-up', blank=True, null=True, verbose_name="Image")
    on_line = models.BooleanField(default=False, verbose_name="En ligne")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")

    class Meta:
        verbose_name_plural = 'Pop up'
        verbose_name = 'Pop-up'

    def __str__(self):
        return self.name


class InfoLegacy(models.Model):
    title= models.CharField(max_length=400)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Info légale pour client (formulaires)'
        verbose_name_plural = 'Info légale pour client (formulaires)'


class PolicyLegacy(models.Model):
    titre = models.CharField(max_length=400)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = 'politique de confidentialité'