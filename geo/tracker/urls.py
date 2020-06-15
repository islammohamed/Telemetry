from datetime import datetime

from django.urls import register_converter, path

from . import views


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')

urlpatterns = [
      path(r'', views.RouteApiView.as_view(), name='route'),
      path(r'<uuid:route_id>/way_point/', views.WayPointApiView.as_view(), name='route_way_point'),
      path(r'<uuid:route_id>/length/', views.RouteLengthApiView.as_view(), name='route_length'),
      path(r'<yyyy:date>/longest/', views.LongestLengthApiView.as_view(), name='longest_route'),
]

app_name = 'tracker'
