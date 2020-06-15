import datetime

import uuid
from django.contrib.gis.geos import LineString

from django.test import TestCase
from django.utils import timezone

from ...models import Route


class TestModels(TestCase):

    def test_give_route_when_refresh_then_calling_older_than_day_will_return_false(self):
        route = Route(id=uuid.uuid4(), coordinates=LineString())
        route.save()

        self.assertFalse(route.older_than_a_day())

