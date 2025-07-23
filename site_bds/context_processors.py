from django.contrib import messages
from django.shortcuts import redirect

from site_bds.ContactForm import NewsLetterForm


def unread_bds(request):
    form_news = NewsLetterForm()

    return {
        'form_news': form_news,
    }





