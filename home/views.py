from rest_framework import status
from rest_framework.views import APIView, Response


class HomeAPI(APIView):

    def get(self, request):
        return Response(data={'message': 'this is home page'}, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response.headers['host'] = 'localhost'
        response.headers['user'] = request.user
        return response
