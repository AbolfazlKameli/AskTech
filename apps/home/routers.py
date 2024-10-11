from rest_framework.routers import DefaultRouter


class NoListDefaultRouter(DefaultRouter):
    def get_routes(self, viewset):
        routes = super().get_routes(viewset)
        routes = [route for route in routes if route.name != '{basename}-list']
        return routes
