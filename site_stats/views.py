from .models import Vpn
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Site



@login_required(login_url='sign_in')
def site_list(request):
    sites = Site.objects.all()
    applis = Vpn.objects.all()

    context = {
        'sites': sites,
        'applis': applis,
    }
    return render(request, 'statistics/site-list.html', context)
