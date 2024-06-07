from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from site_bds.ContactForm import ContactForm, NewsLetterForm
from site_bds.models import Gallery, Testimonials, Team, Ask, Contact, Newsletter
from django.utils.html import escape


def handle404(request, exception):
    return render(request, '404.html', status=404)


def index(request):
    gallery = Gallery.objects.all()
    testimonials = Testimonials.objects.all()
    team = Team.objects.all()
    ask = Ask.objects.all()
    if request.method == "POST":
        # traitement des données
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Merci, Le message est bien envoyé')
            return redirect('contact_message')
        else:
            messages.error(request, 'Merci de vérifier les informations du formulaire.')
            url = reverse('index') + '#contact'
            return redirect(url)
    else:
        form = ContactForm()

    context = {
        'gallery': gallery,
        'testimonials': testimonials,
        'team': team,
        'ask': ask,
        "form": form,
    }
    return render(request, 'site/index.html', context)


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
    new_letter = escape(request.POST.get('new-letter-email'))
    new_letter_email, created = Newsletter.objects.get_or_create(email=new_letter,)
    if not created:
        messages.error(request, 'Vous êtes déja inscrit à la newsletter')
        url = reverse('index') + '#newsletter'
        return redirect(url)
    else:
        messages.success(request, 'Vous êtes bien inscrit à la newsletter.')
        url = reverse('index') + '#newsletter'
        return redirect(url)


def client_message_contact(request):
    message = Contact.objects.all().order_by('-created_at').first()
    html_text = render_to_string("email-client.html", {})

    # Créer un objet EmailMessage
    msg = EmailMessage(
        "Contact BDS",
        html_text,
        "contact@bds38.com",
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
