from django.utils.deprecation import MiddlewareMixin
from django.contrib.gis.geoip2 import GeoIP2
from .models import Visit
from django.utils.crypto import get_random_string
from .models import Visitor


class VisitorTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'visitor_id' not in request.COOKIES:
            visitor_id = get_random_string(length=32)
            response = self.get_response(request)
            response.set_cookie('visitor_id', visitor_id, max_age=365*24*60*60)
            self.increment_visitor_count(visitor_id)
            return response
        else:
            return self.get_response(request)

    def increment_visitor_count(self, visitor_id):
        if not Visitor.objects.filter(visitor_id=visitor_id).exists():
            Visitor.objects.create(visitor_id=visitor_id)






class GeoIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        geo = GeoIP2()

        try:
            location = geo.city(ip)
            Visit.objects.create(
                ip_address=ip,
                country=location.get('country_name', ''),
                city=location.get('city', ''),
                latitude=location.get('latitude', None),
                longitude=location.get('longitude', None),
            )
        except Exception as e:
            print(f"Erreur GeoIP: {e}")
