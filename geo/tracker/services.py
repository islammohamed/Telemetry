import logging
from datetime import datetime, date, timedelta

import uuid
from typing import Tuple, Optional

from django.contrib.gis.db.models.functions import Length

from .tasks import calculate_route_length_task
from .models import Route, LongestRoute
from .exceptions import RouteLenCantNotBeCalculated

logger = logging.getLogger(__name__)


class RouteService:

    _setup_executed = False

    @classmethod
    def generate_route_length(cls, route_id : str) -> None:
        """
        Generate the route length and cache it in the route table
        """
        from .exceptions import RouteLenCantNotBeCalculated
        try:
            length_km = cls.calculate_router_len_km(route_id)
            logger.debug(f"calculate route length for route: "
                         f"{route_id} is executing")

        except RouteLenCantNotBeCalculated:
            logger.error(f"route length for route {route_id} can't be calculated")
            raise

        route = Route.objects.get(pk=route_id)
        route.cached_distance = length_km
        route.save()

    @classmethod
    def calculate_router_len_km(cls, route_id: str) -> Optional[float]:
        """
        Calculates the router using the length gis internal function
        and convert it in km.
        :raise RouteLenCantNotBeCalculated
        """
        route = Route.objects.annotate(length=Length('coordinates'))\
            .filter(id=route_id)

        if not route:
            raise RouteLenCantNotBeCalculated()

        return route.last().length.m / 1000

    @classmethod
    def get_router_len_km(cls, route_id: str) -> Optional[float]:
        """
        Get the router length
        """
        return Route.objects.get(id=route_id).cached_distance

    @classmethod
    def add_route_point(cls, route_id: str, lon_lat: Tuple[float, float], point_created_at=None) -> None:
        """
        adds a new GPS location lon, lat for an already created route
        will raise Entry.DoesNotExist if the route_id doesn't exist in the database
        :raise Entry.DoesNotExist

        """
        logger.debug(f"a new route point added {lon_lat} for {route_id}")

        route = Route.objects.get(pk=route_id)
        route.add_point(lon_lat)

        if point_created_at:
            route.created_at = point_created_at

        route.save()


    @classmethod
    def create_route(cls) -> Optional[Route]:
        """
        Create a new route in the database

        Created Async task will be scheduled to compute the length every minute,
        for the lifetime of the route (24Hours)

        """
        cls._setup()

        from django.contrib.gis.geos import LineString
        route = Route.objects.create(id=uuid.uuid4(), coordinates=LineString())

        logger.debug(f"a new route created {route.id}")

        calculate_route_length_task(str(route.id), repeat=60,
                                    repeat_until=datetime.now() + timedelta(days=1))

        return route

    @classmethod
    def _setup(cls):
        if cls._setup_executed:
            logger.debug("service setup started")
            return

        cls._setup_executed = True
        """
        Creates Async task to generate the most length route of the day
        """
        from .tasks import calculate_longest_path_daily_task

        logger.info("queuing task for the longest path calculation")
        calculate_longest_path_daily_task(repeat=1)


class LongestRouteService:

    @classmethod
    def calculate_longest_path_for_day(cls, selected_date=datetime.today().date()):
        """
        Update the longest path mapped to day
        As result, the database will be having a mapping of
        Day1 -> Route (longest)
        Day2 -> Route2 (longest)
        """
        routes = Route.objects.filter(created_at__date=selected_date) \
            .order_by('-cached_distance')

        if not routes:
            return

        route = routes.first()

        try:
            longest_route = LongestRoute.objects.get(route_date=selected_date)
            longest_route.route = route
            longest_route.save(update_fields=['route'])

        except LongestRoute.DoesNotExist:
            LongestRoute.objects.create(route=route, route_date=selected_date)
        finally:
            logger.debug(f"the longest path for the route: {route.id} "
                         f"saved in the database")

    @classmethod
    def get_longest_route_for_date(cls, route_datetime: datetime) -> Optional[LongestRoute]:
        """
        Retrieve the longest path for a given date
        """
        return LongestRoute.objects.filter(route_date=route_datetime).last()

    @classmethod
    def date_not_in_the_past(cls, date: datetime) -> bool:
        """
        Check is the given date in the past, it will return boolean if the
        date in the future too
        """
        return date.date() >= datetime.today().date()
