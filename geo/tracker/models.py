import datetime
from typing import Tuple

from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString


class Route(models.Model):
    id = models.UUIDField("id", primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    coordinates = models.LineStringField(blank=True)
    cached_distance = models.FloatField(blank=True, default=0)

    def add_point(self, lon_lat: Tuple[float, float]) -> None:
        """
        Add a point(GPS location)  to a route (LineString)
        :param lon_lat: Tuple[float, float] a point to add to the linestring
        """
        if not self.coordinates:
            self.coordinates = LineString(lon_lat, lon_lat)
        else:
            self.coordinates.append(lon_lat)

    def older_than_a_day(self) -> bool:
        """
        Evaluate if the creation Route datetime created more than a day
        """
        return self.created_at < datetime.datetime.now() - datetime.timedelta(days=1)

    class Meta:
        indexes = [models.Index(fields=['-cached_distance'])]


class LongestRoute(models.Model):
    created = models.DateTimeField(auto_now=True)
    route_date = models.DateField(unique=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    class Meta:
        db_table = 'longest_route'

