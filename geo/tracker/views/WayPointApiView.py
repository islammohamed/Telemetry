import logging

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import WayPointSerializer
from ..services import RouteService

logger = logging.getLogger(__name__)


class WayPointApiView(APIView):

    parser_classes = [JSONParser]

    def post(self, request, route_id):
        """
        Handle adding a new point to an existing route.

        It continuously populates the route with data points (WGS84 coordinates).
        A route is expected to be done within a day.
        After a day, the user can not add more data points.

        :return
        HTTP 201 will be returned if the point added successfully.
        HTTP 400 will be returned if there is a validation error
        HTTP 404 will be returned if route doesn't exist in the database

        """
        request_data = request.data
        request_data.update({'route_id': route_id})

        way_point_serializer = WayPointSerializer(data=request_data)

        way_point_serializer.is_valid(raise_exception=True)

        clean_data = way_point_serializer.validated_data

        logger.debug(f"adding point for route: {route_id}, long, lat: {clean_data['lon']}, {clean_data['lat']}")

        RouteService.add_route_point(route_id, (clean_data['lon'], clean_data['lat']))

        return Response(status=201)

