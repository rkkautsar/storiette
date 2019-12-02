from rest_framework import views, permissions
from rest_framework.response import Response

from users.serializers import UserSerializer


class UserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
