from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer

class SignupView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer

class MeView(APIView):
    def get(self, request):
        u = request.user
        return Response({"id": u.id, "email": u.email, "username": u.username})
