from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from .models import Visitor
from datetime import datetime, timedelta


@login_required(login_url='sign_in')
def visitor_statistics(request):
    # Visiteurs par jour
    # Calcul des dates pour filtrer les visites récentes
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Visiteurs par jour (les 7 derniers jours)
    daily_visitors = Visitor.objects.filter(date_visited__gte=today - timedelta(days=7)).annotate(
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
