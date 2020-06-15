import datetime

from parameterized import parameterized
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ....services import LongestRouteService, RouteService
from ..ClientMixin import ClientMixin


class LongestPathRequest(ClientMixin, APITestCase):

    def setUp(self):
        wgs84_coordinates = [
            {"lat": -25.4025905, "lon": -49.3124416},
            {"lat": -23.559798, "lon": -46.634971},
            {"lat": 59.3258414, "lon": 17.70188},
            {"lat": 54.273901, "lon": 18.591889}
        ]

        self.yesterday = (timezone.now() - datetime.timedelta(days=1)).date()

        for i in range(len(wgs84_coordinates)):
            # create route first
            route_response = self._create_route()
            route_id = route_response.data['id']

            # add points to route, add more point on the way
            self._create_points_for_yesterday(route_id, wgs84_coordinates[:i+1], self.yesterday)

            # execute (The background task) to generate route length
            RouteService.generate_route_length(route_id)

        # execute the background task to calculate the length route daily
        LongestRouteService.calculate_longest_path_for_day(self.yesterday)

    def test_given_a_request_when_valid_datetime_then_return_valid_response(self):

        response = self.client.get(reverse('tracker:longest_route', args={self.yesterday}), format='json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        length = response.data['length']

        self.assertGreater(length, 11750)
        self.assertLess(length, 11900)

    def test_given_a_request_when_invalid_datetime_then_return_bad_request(self):

        response = self.client.get(reverse('tracker:longest_route', args={timezone.now().date()}), format='json')

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @parameterized.expand([
        'post',
        'put',
        'delete',
    ])
    def test_given_a_request_when_wrong_http_method_then_return_error_response_code(self, method):

        response = self.client.generic(method, reverse('tracker:longest_route', args={self.yesterday}), format='json')

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
