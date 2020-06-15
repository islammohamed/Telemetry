import logging
from datetime import datetime

from rest_framework import serializers, exceptions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services import LongestRouteService

logger = logging.getLogger(__name__)


class LongestLengthApiView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, date: datetime):
        """
        Get the longest route for a given date
        date should be in the past

        :return
        200 if the longest path found for the given date
        400 if the date in invalid e.g. today or in the future
        404 if the longest date can't be found
        """
        if LongestRouteService.date_not_in_the_past(date):
            logger.error(f"a request to longest path for a data in the past {date}")

            raise serializers.ValidationError(f"Date provided {date.date()} "
                                              f"is invalid, date should be in the past and in UTC")

        longest_route = LongestRouteService.get_longest_route_for_date(date)

        if not longest_route:
            logger.error(f"a request for longest data for date {date} can't be found in the database")
            raise exceptions.NotFound(f'No routes for date {date.date()}')

        response = {"length": longest_route.route.cached_distance,
                    "route_id": longest_route.route.id, 'date': date.date()}

        return Response(response)
