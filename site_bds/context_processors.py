from django.contrib import messages
from django.shortcuts import redirect

from site_bds.ContactForm import NewsLetterForm, ContactFormPopUp
from site_bds.models import Contact, PopUp, InfoLegacy, PolicyLegacy


def unread_bds(request):
    form_news = NewsLetterForm()
    popups = PopUp.objects.filter(on_line=True).order_by("?")
    info_legacy = InfoLegacy.objects.all().first()
    policy = PolicyLegacy.objects.all().first()


    return {
        'form_news': form_news,
        'popups': popups,
        'info_legacy': info_legacy,
        'policy': policy,
    }



def unread_pop_over(request):
    contact_messages = Contact.objects.all()
    # Vérifie que le bon formulaire est soumis
    if request.method == "POST" and request.POST.get('form_name') == 'popup_contact':
        form = ContactFormPopUp(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Merci, Le message est bien envoyé')
            return redirect('contact_message')
        else:
            messages.error(request, 'Merci de vérifier les informations du formulaire.')
    else:
        form = ContactFormPopUp()

    return {'popup_form': form}





