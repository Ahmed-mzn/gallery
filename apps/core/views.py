from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import SignUpSerializer, RoleSerializer
from .models import Role, User


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            response = {"access": str(refresh.access_token), "refresh": str(refresh)}

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def new_subscription(request):
    plan_id = request.data.get('plan_id')
    user_id = request.data.get('user_id')
    user = get_object_or_404(User, pk=user_id)
    user.plan_id = plan_id
    user.save()

    return Response(data={"message": "Subscription success"})
