import datetime
import uuid

from parameterized import parameterized
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from ..ClientMixin import ClientMixin


class TestWayPointApiRequest(ClientMixin, APITestCase):

    def setUp(self):
        self.yesterday = (timezone.now() - datetime.timedelta(days=1)).date()

        route_response = self._create_route()
        self.route_id = route_response.data['id']


    @parameterized.expand([
            [{"lat": -25.4025905, "lon": -49.3124416}],
            [{"lat": -23.559798, "lon": -46.634971}],
            [{"lat": 59.3258414, "lon": 17.70188}],
            [{"lat": 54.273901, "lon": 18.591889}]
    ])
    def test_given_a_waypoint_request_when_valid_lonlat_then_return_valid_response(self, coordinates):

        response = self.client.post(reverse('tracker:route_way_point',args={self.route_id}),
                                    coordinates, format='json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    @parameterized.expand(['RANDOMTEXT',  "387c6485-0e30-4e62-94a6-be2b9a8111aa"])
    def test_given_a_waypoint_request_when_invalid_route_id_then_return_not_found(self, route_id):

        response = self.client.post(f'/routes/{route_id}/way_point/',
                                     {"lat": -25.4025905, "lon": -49.3124416}, format='json')

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    @parameterized.expand( [
        [{"lat": -200.4025905, "lon": -4900.3124416}],
        [{"lat": 223.559798, "lon": -4622.634971}],
        [{"lat": 59.3258414, "lon": 199.70188}],
        [{"lat": 54.273901, "lon": 591889}],
        [{"lat": 10000, "lon": 10000}]
    ])
    def test_given_a_waypoint_request_when_invalid_request_payload_then_return_bad_request(self, coordinates):
        response = self.client.post(reverse('tracker:route_way_point', args={self.route_id}),
                                     coordinates, format='json')

        self.assertEquals( response.status_code, status.HTTP_400_BAD_REQUEST )


    @parameterized.expand([
        'get',
        'put',
        'delete',
    ])
    def test_given_a_request_when_wrong_http_method_then_return_error_response_code(self, method):

        response = self.client.generic(method, reverse('tracker:route_way_point', args={self.route_id}), format='json')

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
