
from django.urls import reverse
from django.utils import timezone
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from ....services import RouteService
from ..ClientMixin import ClientMixin


class TestRouteLengthApiRequest(ClientMixin, APITestCase):
    def setUp(self):
        wgs84_coordinates = [
            {"lat": -25.4025905, "lon": -49.3124416},
            {"lat": -23.559798, "lon": -46.634971},
            {"lat": 59.3258414, "lon": 17.70188},
            {"lat": 54.273901, "lon": 18.591889}
        ]

        # create route first
        route_response = self._create_route()
        self.route_id = route_response.data['id']

        # add points to route, add more point on the way
        self._add_route_points(self.route_id, wgs84_coordinates)

        # execute (The background task) to generate route length
        RouteService.generate_route_length(self.route_id)

    def test_given_a_request_when_provide_valid_route_then_return_valid_response(self):
        response = self.client.get(reverse("tracker:route_length", args=[self.route_id]))

        self.assertIsNotNone(response.data['km'])
        self.assertIsNotNone(response.data['route_id'])

        self.assertEquals(self.route_id, response.data['route_id'])

    @parameterized.expand([
        'post',
        'put',
        'delete',
    ])
    def test_given_a_request_when_provide_invalid_http_method_then_return_invalid_http_response(self, method):

        response = self.client.generic(method, reverse( "tracker:route_length", args=[self.route_id] ) )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

