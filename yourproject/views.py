from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from yourproject.forms import QuestionForm
from yourproject.models import Question


def your_project(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, )
        if form.is_valid():
            form.save()
            messages.success(request, 'Merci, votre devis est bien envoyé, nous reviendrons vers vous rapidement.')
            return redirect(devis_message)
        else:
            messages.error(request, 'Merci de vérifier la saisie du formulaire.')
            form = QuestionForm()

    else:
        form = QuestionForm()

    context = {
        'form': form,
        'questions': questions,
    }

    return render(request, 'yourproject/your-project.html', context)


def devis_message(request):
    message = Question.objects.all().order_by('-update_at').first()
    html = f"""
           <p>Bonjour Luc.</p>
           <p>Un nouveau devis vient d'être publié par : <br>
           {message.author}  {message.email} <br>
           sur le site 'BDS' le {message.update_at}</p>
           <p>Le message : {message.description}</p>
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

    return redirect('client-message')


def client_message(request):
    message = Question.objects.all().order_by('-update_at').first()
    html = f"""
           <p>Bonjour,</p>
           <p>Nous confirmons la reception de votre message.</p>
           <p>Nous vous contacterons rapidement après l'étude de votre demande.<p>
           <p>Merci pour votre confiance.<p>
           <p>Cordialement</p>
           <p>L'équipe BDS<p>
           """

    # Créer un objet EmailMessage
    msg = EmailMessage(
        "Contact BDS",
        html,
        "contact@bds38.com",
        [message.email],
    )

    # Définir le type de contenu de l'email comme HTML
    msg.content_subtype = 'html'
    # Envoyer l'email
    msg.send()

    return redirect('page-success')


def page_success(request):
    devis = Question.objects.all().order_by('-update_at').first()
    return render(request, 'yourproject/page-success.html', {'devis': devis})
