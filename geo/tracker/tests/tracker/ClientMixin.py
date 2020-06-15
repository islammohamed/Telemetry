import uuid

from django.urls import reverse
from rest_framework.test import APITestCase

from ...services import RouteService


class ClientMixin(APITestCase):

    def _create_route(self, method=None):
        """
        create a new route
        """
        if not method:
            method = 'post'

        response = self.client.generic(method, reverse('tracker:route'), {}, format='json')

        return response

    def _add_route_points(self, route_id, wgs84_coordinates):
        """
        add route points to a given route
        """
        for coordinates in wgs84_coordinates:
            self.client.post(reverse("tracker:route_way_point", args=[route_id]), coordinates,  format='json')

    def _create_points_for_yesterday(self, route_id, coordinates, route_created_at):
        for coordinate in coordinates:
            RouteService.add_route_point(route_id, (coordinate['lon'], coordinate['lat']), route_created_at)

    def is_valid_uuid(self, value):
        try:
            uuid.UUID(str(value))
            return True
        except ValueError:
            return False
