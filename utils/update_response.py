from rest_framework import status
from rest_framework.response import Response


def update_response(response, message: str):
    """Handles the response for update operations."""
    if response.status_code == 200:
        return Response(data={'message': message}, status=status.HTTP_200_OK)
    return response
