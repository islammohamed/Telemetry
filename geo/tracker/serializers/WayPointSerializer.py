import logging

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from ..models import Route

logger = logging.getLogger(__name__)


class WayPointSerializer(serializers.Serializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()
    route_id = serializers.UUIDField()

    def validate_lon(self, lon):
        """Validate lon value"""
        if not -180 <= lon <= 180:
            logger.debug(f"Invalid lon value {lon}")
            raise serializers.ValidationError("Provided long value is invalid, Probably out of range (-180, 80)")

        return lon

    def validate_lat(self, lat):
        """Validate lat value"""
        logger.debug( f"Invalid lat value {lat}" )
        if not -90 <= lat <= 90:
            raise serializers.ValidationError("Provided lat value is invalid, Probably out of range (-90, 90)")

        return lat

    def validate_route_id(self, route_id):
        """
        Validate route_id, which is not older than a day
        """
        try:
            route = Route.objects.get(id=route_id)
        except Route.DoesNotExist:
            logger.debug(f"route_id value is invalid or does not exist {route_id}")
            raise NotFound(f"Provided route_id value is invalid or does not exist {route_id}")

        if route.older_than_a_day():
            logger.info(f"route requests is older than a day {route_id}")
            raise serializers.ValidationError( "Provided way point can't be added to a route older than a day" )

        return route_id
