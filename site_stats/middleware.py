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


