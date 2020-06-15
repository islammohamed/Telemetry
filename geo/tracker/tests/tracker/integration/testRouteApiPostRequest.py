from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase

from ..ClientMixin import ClientMixin


class TestRouteApiPostRequest(ClientMixin, APITestCase):

    def test_given_a_create_request_when_provide_valid_request_then_return_created_resource(self):
        response = self._create_route()
        id = response.data['id']

        self.assertTrue(self.is_valid_uuid(id))

    @parameterized.expand([
        'get',
        'put',
        'delete',
    ])
    def test_given_a_create_request_when_provide_invalid_http_method_then_return_invalid_http_response(self, method):
        response = self._create_route(method)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
