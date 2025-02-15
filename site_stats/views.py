from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from .models import Visitor, Vpn
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from django.utils import timezone  # Importez timezone
from .models import Visitor
from datetime import timedelta
from django.shortcuts import render
from .models import Site
from .models import Visit
import json
from django.db.models.functions import TruncDate



@login_required(login_url='sign_in')
def visitor_statistics(request):
    # Obtenez la date et l'heure actuelle avec le fuseau horaire
    now = timezone.now()

    # Calcul des dates pour filtrer les visites récentes
    today = now.date()  # Utilisez la date de 'now'
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Convertir les dates de filtrage en dates conscientes du fuseau horaire
    start_of_week = timezone.make_aware(datetime.combine(start_of_week, datetime.min.time()))
    start_of_month = timezone.make_aware(datetime.combine(start_of_month, datetime.min.time()))
    start_of_year = timezone.make_aware(datetime.combine(start_of_year, datetime.min.time()))

    # Visiteurs par jour (les 7 derniers jours)
    daily_visitors = Visitor.objects.filter(date_visited__gte=now - timedelta(days=7)).annotate(
        day=TruncDay('date_visited')).values('day').annotate(count=Count('id')).order_by('day')

    # Visiteurs par semaine (les 4 dernières semaines)
    weekly_visitors = Visitor.objects.filter(date_visited__gte=start_of_week - timedelta(weeks=4)).annotate(
        week=TruncWeek('date_visited')).values('week').annotate(count=Count('id')).order_by('week')

    # Visiteurs par mois (les 12 derniers mois)
    monthly_visitors = Visitor.objects.filter(date_visited__gte=start_of_month - timedelta(days=365)).annotate(
        month=TruncMonth('date_visited')).values('month').annotate(count=Count('id')).order_by('month')

    # Visiteurs par année (les 5 dernières années)
    yearly_visitors = Visitor.objects.filter(date_visited__gte=start_of_year - timedelta(days=5 * 365)).annotate(
        year=TruncYear('date_visited')).values('year').annotate(count=Count('id')).order_by('year')

    context = {
        'daily_visitors': daily_visitors,
        'weekly_visitors': weekly_visitors,
        'monthly_visitors': monthly_visitors,
        'yearly_visitors': yearly_visitors,
    }
    return render(request, 'statistics/stats.html', context)


@login_required(login_url='sign_in')
def site_list(request):
    sites = Site.objects.all()
    applis = Vpn.objects.all()

    context = {
        'sites': sites,
        'applis': applis,
    }
    return render(request, 'statistics/site-list.html', context)


""" def stats_combined(request):
    # 📍 1️⃣ Récupérer toutes les visites avec leur localisation
    visits = Visit.objects.values('latitude', 'longitude', 'city', 'country')

    # 🇫🇷 2️⃣ Récupérer les connexions en France par jour
    visits_france = Visit.objects.filter(country="France") \
        .annotate(date=TruncDate('timestamp')) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    data = [(v['date'].strftime('%Y-%m-%d'), v['count']) for v in visits_france]

    # 📡 3️⃣ Envoyer toutes les données dans le template
    return render(request, "statistics/stats-2.html", {
        "visits": json.dumps(list(visits)),
        "data": data
    })"""