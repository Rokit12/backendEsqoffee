from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContactCreateUpdateSerializer


class CreateContactAPIView(APIView):
    """
    post:
        Create a contact instance. Returns created contact data

        parameters: [name, email, subject, message]

    """

    serializer_class = ContactCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContactCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

