import logging

from background_task import background


logger = logging.getLogger( __name__ )


@background()
def calculate_longest_path_daily_task():
    logger.debug( "executing task to generate longest path daily" )

    from .services import LongestRouteService
    LongestRouteService.calculate_longest_path_for_day()


@background()
def calculate_route_length_task(route_id: str):
    logger.debug( f"Calculating the longest path for the route: {route_id}" )
    from .services import RouteService
    RouteService.calculate_router_len_km( route_id )

