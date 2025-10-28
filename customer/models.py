from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

from BDS_Site.settings import CELERY_BROKER_URL


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    first_name = models.CharField(max_length=50, verbose_name="Prénom")

    phone_validator = RegexValidator(
        regex=r'^(?:\+33|0)[1-9](?:\d{8})$',
        message="Entrez un numéro de téléphone valide (ex: +33612345678 ou 0612345678)."
    )

    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        verbose_name="Numéro de téléphone"
    )
    email = models.EmailField()
    address = models.CharField(max_length=50, verbose_name="Adresse")
    entreprise = models.CharField(max_length=50, null=True, blank=True, verbose_name="Entreprise")
    mail = models.EmailField(verbose_name="Mail")
    complement_address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Complément d'adresse")
    city = models.CharField(max_length=50, verbose_name="Ville")
    created_at = models.DateTimeField(auto_now_add=True)
    zip_code = models.CharField(
        verbose_name="Code Postal",
        max_length=5,
        validators=[RegexValidator(r'^\d{5}$', "Entrez un code postal valide (5 chiffres).")]
    )
    image = models.ImageField(upload_to='photos-customer', null=True, blank=True)
    register_web = models.BooleanField(default=False, verbose_name="Inscription web")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MyProject(models.Model):
    ON_HOLD_BDS = "Attente action BDS"
    ON_HOLD_CUSTOMER = "Attente action client"
    FINALIZED = "Finalisé"

    STATUS_CHOICES = [
        (ON_HOLD_BDS, 'Attente action BDS'),
        (ON_HOLD_CUSTOMER, 'Attente action client'),
        (FINALIZED, 'Finalisé'),
    ]
    SITE_WEB = "Site web"
    APP = "App web"
    APP_MOBILE = "App mobile"
    E_COMMERCE = "E-commerce"
    APP_BUREAU = "App bureau"
    GESTION_DB = "Gestion db"
    AUTRE = "Autre"

    PROJECTS_TYPE_CHOICES = [
        (SITE_WEB, 'Site web'),
        (APP, 'App web'),
        (APP_MOBILE, 'App mobile'),
        (E_COMMERCE, 'E-commerce'),
        (APP_BUREAU, 'App bureau'),
        (GESTION_DB, 'Gestion db'),
        (AUTRE, 'Autre'),
    ]

    user = models.ForeignKey(Customer, related_name="facilities", on_delete=models.CASCADE,
                             verbose_name="Utilisateur")
    ref = models.CharField(max_length=100, verbose_name="Reférence")
    project_type = models.CharField(max_length=60, choices=PROJECTS_TYPE_CHOICES, verbose_name="Type du projet")
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, verbose_name="Statut")
    project_name = models.CharField(max_length=100, verbose_name="Nom du projet")
    domaine = models.CharField(max_length=100, verbose_name="Domaine", blank=True, null=True)
    maintenance_contract = models.CharField(max_length=100, verbose_name="Contrat", blank=True, null=True)
    server = models.CharField(max_length=100, verbose_name="Serveur", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")

    class Meta:
        verbose_name = "Mon projet"
        verbose_name_plural = "Mes projets"

    def __str__(self):
        return self.project_name


class Documents(models.Model):
    ESTIMATE = "Devis"
    BILL = "Facture"
    PRODUCT_SHEET = "Cahier des charges"
    STRUCTURAL_STUDY = "Étude de structure"
    MAINTENANCE_CONTRACT = "Contrat de maintenance"
    CHARTE_GRAPHIQUE = "Charte graphique"


    DOCS_CHOICES = [
        (ESTIMATE, 'Devis'),
        (BILL, 'Facture'),
        (PRODUCT_SHEET, 'Cahier des charges'),
        (MAINTENANCE_CONTRACT, 'Contrat de maintenance'),
        (CHARTE_GRAPHIQUE, 'Charte graphique'),
    ]

    user = models.ForeignKey(Customer, related_name="documents", verbose_name="Utilisateur",
                             on_delete=models.PROTECT)
    document_name = models.CharField(max_length=60, choices=DOCS_CHOICES, verbose_name="Nom du document")
    document_description = models.CharField(max_length=100, verbose_name="description")
    document = models.FileField(upload_to="documents/", verbose_name="Document")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.document_name


class Fonctions(models.Model):
    ALLAUTH = "Allauth"
    SIMPLE = "Standard"

    AUTH_CHOICES = [
        (ALLAUTH, 'Allauth'),
        (SIMPLE, 'Standard'),
    ]

    CSS = 'Css'
    CSS_BOOTSTRAP = 'Css + Bootstrap'
    BOOTSTRAP = 'Bootstrap'
    TAILWIND = 'Tailwind'
    HTML = 'Html'
    JS = 'JavaScript'
    JS_HTML = 'JavaScript + Html'
    JS_HTML_HTMX = 'JavaScript + Html + Htmx'
    REACT = 'React'
    ANGULAR = 'Angular'
    VUE = 'Vue.js'
    SVELTE = 'Svelte'
    NEXT = 'Next.js'
    NUXT = 'Nuxt.js'
    CELERY = 'Celery'
    DJANGO = 'Django'
    FLASK = 'Flask'
    FASTAPI = 'FastAPI'
    EXPRESS = 'Express.js'
    NEST = 'NestJS'
    LARAVEL = 'Laravel'
    SYMFONY = 'Symfony'
    RUBY = 'Ruby on Rails'
    SPRING = 'Spring Boot'
    DOTNET = '.NET Core'
    PYTHON = 'Python'
    PYTHON_JS = 'Python + JavaScript'
    AUCUN = 'Aucun'

    LANGUAGE_CHOICES = [
        (CSS, 'Css'),
        (CSS_BOOTSTRAP, 'Css + Bootstrap'),
        (BOOTSTRAP, 'Bootstrap'),
        (TAILWIND, 'Tailwind'),
        (HTML, 'Html'),
        (JS, 'JavaScript'),
        (JS_HTML, 'JavaScript + Html'),
        (JS_HTML_HTMX, 'JavaScript + Html + Htmx'),
        (REACT, 'React'),
        (ANGULAR, 'Angular'),
        (VUE, 'Vue.js'),
        (SVELTE, 'Svelte'),
        (NEXT, 'Next.js'),
        (NUXT, 'Nuxt.js'),
        (CELERY, 'Celery'),
        (DJANGO, 'Django'),
        (FLASK, 'Flask'),
        (FASTAPI, 'FastAPI'),
        (EXPRESS, 'Express.js'),
        (NEST, 'NestJS'),
        (LARAVEL, 'Laravel'),
        (SYMFONY, 'Symfony'),
        (RUBY, 'Ruby on Rails'),
        (SPRING, 'Spring Boot'),
        (DOTNET, '.NET Core'),
        (PYTHON, 'Python'),
        (PYTHON_JS, 'Python + JavaScript'),
        (AUCUN, 'Aucun'),
    ]

    # 🧱 Liste des frameworks principaux
    FRAMEWORKS_CHOICES = [
        ('Bootstrap', 'Bootstrap'),
        ('Tailwind CSS', 'Tailwind CSS'),
        ('React', 'React'),
        ('Angular', 'Angular'),
        ('Vue.js', 'Vue.js'),
        ('Svelte', 'Svelte'),
        ('Next.js', 'Next.js'),
        ('Nuxt.js', 'Nuxt.js'),
        ('Django', 'Django'),
        ('Flask', 'Flask'),
        ('FastAPI', 'FastAPI'),
        ('Express.js', 'Express.js'),
        ('NestJS', 'NestJS'),
        ('Laravel', 'Laravel'),
        ('Symfony', 'Symfony'),
        ('Ruby on Rails', 'Ruby on Rails'),
        ('Spring Boot', 'Spring Boot'),
        ('.NET Core', '.NET Core'),
        ('Celery', 'Celery'),
        ('Htmx', 'Htmx'),
        ('jQuery', 'jQuery'),
        ('Aucun', 'Aucun'),
    ]

    project = models.ForeignKey(
        MyProject,
        related_name="project_function",
        verbose_name="Projet",
        on_delete=models.PROTECT
    )

    auth_name = models.CharField(max_length=60, choices=AUTH_CHOICES, verbose_name="Authentification")
    language_front = models.CharField(max_length=60, choices=LANGUAGE_CHOICES, verbose_name="Langage front")
    language_back = models.CharField(max_length=60, choices=LANGUAGE_CHOICES, verbose_name="Langage back-end")
    language_autre = models.CharField(max_length=60, choices=LANGUAGE_CHOICES, verbose_name="Langage autre")
    planification = models.CharField(max_length=60, choices=LANGUAGE_CHOICES, verbose_name="Planification")
    language_style = models.CharField(max_length=60, choices=LANGUAGE_CHOICES, verbose_name="Langage style")

    frameworks = models.CharField(
        max_length=60,
        choices=FRAMEWORKS_CHOICES,
        verbose_name="Framework principal"
    )

    nb_de_pages = models.IntegerField(default=0, blank=True, null=True, verbose_name="Nb de pages")

    class Meta:
        verbose_name = "Fonction dans le site"
        verbose_name_plural = "Fonctions dans le site"

    def __str__(self):
        return f"{self.project} — {self.frameworks}"







