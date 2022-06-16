from aiohttp_utils.routing import add_resource_context

from .web_form_handlers import web_form_routes
from .start_handlers import start_routes
from .register_handlers import register_routes
from .handlers import static_routes


def setup(app, url_path_prefix):
    """Set up routes as resources so we can use the `Index:get` notation for URL lookup."""

    combined_routes = [*register_routes, *start_routes, *static_routes, *web_form_routes]

    for route in combined_routes:
        use_prefix = route.kwargs.get('use_prefix', True)
        prefix = url_path_prefix if use_prefix else ''
        with add_resource_context(app,
                                  module='app.handlers',
                                  url_prefix=prefix) as new_route:
            new_route(route.path, route.handler())
