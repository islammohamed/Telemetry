import logging

from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services import RouteService

logger = logging.getLogger(__name__)


class RouteLengthApiView(APIView):

    renderer_classes = [JSONRenderer]

    def get(self, request, route_id):
        """
        Get length for given route

        :return
        HTTP 200 JSON Response
        HTTP 404 When route_id doesn't exist
        """
        try:
            length = RouteService.get_router_len_km(route_id=route_id)
        except Route.DoesNotExist:
            logger.warning(f"route length can't be found for route: {route_id}")

            raise NotFound("route length can't be found")

        return Response({"km": length, "route_id": route_id})
