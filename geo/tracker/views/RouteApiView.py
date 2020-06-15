import logging

from django.db import Error
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services import RouteService

logger = logging.getLogger(__name__)


class RouteApiView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        """
        created a new route and return it's corresponding information

        :return 201 created
        """
        try:
            route = RouteService.create_route()
            logger.debug(f"route created with id: {route.id}")
        except Error:
            logger.warning(f"route can't be created")
            raise APIException()

        return Response({
            "id": route.id, "created_at": route.created_at
        }, status.HTTP_201_CREATED)
