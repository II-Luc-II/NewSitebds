from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
import logging

from django.utils.html import strip_tags

from customer.models import Customer, MyProject
from site_bds.ArticleForm import ArticleForm
from site_bds.ContactForm import ContactForm, NewsLetterForm, ContactFormPopUp
from site_bds.models import Gallery, Testimonials, Team, Ask, Contact, Newsletter, Blogs, ALaUne, Article
from site_bds.tasks import send_mail_batch

# Initialise le logger
logger = logging.getLogger(__name__)


# -------------------Super User verify-------------------

def is_superuser(user):
    return user.is_superuser


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /account/",
        "Disallow: /site_gadgetes/",
        "Sitemap: https://site.bds38.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def handle404(request, exception):
    return render(request, '404.html', status=404)


def index(request):
    gallery = Gallery.objects.all()
    testimonials = Testimonials.objects.all()
    team = Team.objects.all()
    ask = Ask.objects.all()
    a_la_une = ALaUne.objects.all().first()

    context = {
        'gallery': gallery,
        'testimonials': testimonials,
        'team': team,
        'ask': ask,
        'a_la_une': a_la_une,
    }
    return render(request, 'site/index.html', context)


@login_required(login_url='account_login')
def account(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    projects = MyProject.objects.filter(user=customer)

    if not customer:
        messages.error(request, '⬅︎ Merci de compléter votre profil.')

    context = {
        'customer': customer,
        'projects': projects,
    }

    return render(request, 'site/account.html', context)


@login_required(login_url='account_login')
def details_my_project(request, project_id):
    project = get_object_or_404(MyProject, id=project_id)
    # Organiser les documents sous forme de dictionnaire

    context = {
        'project': project,
    }

    return render(request, 'site/details-my-project.html', context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Merci, le message a bien été envoyé.')
            return redirect('contact_message')
        else:
            # 🔍 Logguer toutes les erreurs du formulaire
            logger.warning("Échec de validation du formulaire de contact.")
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(f"[{field}] {error}")

            messages.error(request, 'Merci de vérifier les informations du formulaire.')
    else:
        form = ContactForm()

    context = {
        "form": form,
    }
    return render(request, 'site/contact.html', context)


def contact_form_view(request):
    if request.method == "POST":
        print("POST reçu:", request.POST)
        form = ContactFormPopUp(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Merci, le message a bien été envoyé.')

            message = Contact.objects.order_by('-created_at').first()

            html = f"""
                <p>Bonjour.</p>
                <p>Un nouveau message vient d'être publié par : <br>
                {message.name}  {message.email} <br>
                sur le site 'BDS' le {message.created_at}</p>
                <p>Le message : {message.message}</p>
            """

            # Email admin
            EmailMessage(
                "Nouveau message de contact",
                html,
                "BDS <contact@bds38.com>",
                ["contact@bds38.com"],
                headers={'Reply-To': message.email}
            ).send()

            # Email client
            html_text = render_to_string("email-client.html", {})
            EmailMessage(
                "Contact BDS",
                html_text,
                "BDS <contact@bds38.com>>",
                [message.email],
            ).send()

            return redirect('index')

        else:
            print("Erreurs formulaire :", form.errors.as_data())
            messages.error(request, 'Merci de vérifier les informations du formulaire.')
            request.session['popup_active'] = True

            return render(request, 'site/index.html', {
                'popup_form': form,
                'popup_active': True
            })


def contact_message(request):
    message = Contact.objects.all().order_by('-created_at').first()
    html = f"""
           <p>Bonjour Luc.</p>
           <p>Un nouveau message vient d'être publié par : <br>
           {message.name}  {message.email} <br>
           sur le site 'BDS' le {message.created_at}</p>
           <p>Le message : {message.message}</p>
           """

    # Créer un objet EmailMessage
    msg = EmailMessage(
        "Nouveau message de contact",
        html,
        "contact@bds38.com",
        ["contact@bds38.com"],
    )

    # Définir le type de contenu de l'email comme HTML
    msg.content_subtype = 'html'
    # Envoyer l'email
    msg.send()

    return redirect('client-message-contact')


def add_news_letter(request):
    if request.method == "POST":
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            obj, created = Newsletter.objects.get_or_create(email=email)
            if not created:
                messages.error(request, 'Vous êtes déjà inscrit à la newsletter.')
            else:
                messages.success(request, 'Vous êtes bien inscrit à la newsletter.')
            return redirect(reverse('index') + '#newsletter')
        else:
            messages.error(request, "Merci de valider le formulaire.")
            return redirect(reverse('index') + '#newsletter')


def client_message_contact(request):
    message = Contact.objects.all().order_by('-created_at').first()
    html_text = render_to_string("email-client.html", {})

    # Créer un objet EmailMessage
    msg = EmailMessage(
        "Contact BDS",
        html_text,
        "BDS <contact@bds38.com>",
        [message.email],
    )

    # Définir le type de contenu de l'email comme HTML
    msg.content_subtype = 'html'
    # Envoyer l'email
    msg.send()

    return redirect('page-success-client')


def page_success_client(request):
    contact = Contact.objects.all().order_by('-created_at').first()
    return render(request, 'site/page-success-client.html', {'contact': contact})


def privacy(request):
    return render(request, 'site/privacy.html')


def contact_message_newsletter(request):
    news_letter = Newsletter.objects.all().order_by('-created_at').first()
    html = f"""
           <p>Bonjour Luc.</p>
           <p>Un nouveau client vient de s'abonner à la news-letter : <br>
           {news_letter.email}<br>
           sur le site 'BDS' le {news_letter.created_at}</p>
           """

    # Créer un objet EmailMessage
    msg = EmailMessage(
        "Client news-letter",
        html,
        "contact@bds38.com",
        ["contact@bds38.com"],
    )

    # Définir le type de contenu de l'email comme HTML
    msg.content_subtype = 'html'
    # Envoyer l'email
    msg.send()

    url = reverse('index') + '#newsletter'
    return redirect(url)


def news(request):
    blogs = Blogs.objects.all().order_by('-created_at')

    context = {
        'blogs': blogs,
    }
    return render(request, 'site/news.html', context)


def blog_single(request, blog_id):
    blogs = Blogs.objects.get(id=blog_id)
    blog_all = Blogs.objects.all()

    context = {
        'blogs': blogs,
        "blog_all": blog_all,
        'blog_single': blog_single,
    }

    return render(request, 'site/blog-single.html', context)


def gallery_single(request, gallery_id):
    gallery = Gallery.objects.get(id=gallery_id)
    gallery_all = Gallery.objects.all()

    context = {
        'gallery': gallery,
        'gallery_all': gallery_all,
    }

    return render(request, 'site/gallery-single.html', context)


# ------------ VIEWS ARTICLES -------------------

@user_passes_test(is_superuser)
def add_article(request):
    articles = Article.objects.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, "Article ajouté avec succès !")
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()

    context = {
        'form': form,
        'articles': articles
    }

    return render(request, 'articles/add-article.html', context)


@user_passes_test(is_superuser)
def change_article(request, slug):
    articles = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=articles)
        if form.is_valid():
            article = form.save()
            messages.success(request, "Article modifié avec succès !")
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=articles)

    context = {
        'form': form,
        'articles': articles
    }

    return render(request, 'articles/change-article.html', context)


@user_passes_test(is_superuser)
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'articles/article_detail.html', {'article': article})


@user_passes_test(is_superuser)
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        article.delete()
        messages.success(request, "L'article est bien supprimé.")
        return redirect('add_article')
    else:
        messages.error(request, "désolé, impossible de supprimer l'article.")

    return render(request, 'articles/add-article.html')


@user_passes_test(is_superuser)
def send_mail_article(request, slug):
    # Récupérer l'article
    article = get_object_or_404(Article, slug=slug)

    # Générer l'URL complète de l'image
    image_url = request.build_absolute_uri(article.image.url) if article.image else None

    # Récupérer tous les emails des responsables
    responsables = Customer.objects.all()
    recipient_list = [responsable.email for responsable in responsables]

    # Vérifier qu'il y a des destinataires
    if not recipient_list:
        messages.error(request, "Aucun destinataire trouvé pour l'envoi.")
        return redirect('article_detail', slug=article.slug)

    # Générer le lien vers l'article
    article_link = request.build_absolute_uri(
        reverse('article_detail', kwargs={'slug': article.slug})
    )

    # Obtenir le domaine actuel
    current_site = Site.objects.get_current().domain

    # Contexte pour le template
    context = {
        "article": article,
        "image_url": image_url,
        "article_link": article_link,
        "domain": current_site,
    }

    # Préparer l'email
    subject = f"Nouveau post : {article.title}"
    html_message = render_to_string('email_article.html', context)
    plain_message = strip_tags(html_message)

    # Diviser les destinataires en lots de 10
    batch_size = 10
    for i in range(0, len(recipient_list), batch_size):
        batch = recipient_list[i:i + batch_size]
        # Appeler la tâche Celery pour envoyer par lots
        send_mail_batch.delay(subject, html_message, plain_message, batch, "BDS <contact@bds38.com>")

    messages.success(request, "L'email a été envoyé avec succès aux destinataires.")
    return redirect('article_detail', slug=article.slug)

