from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .serializers import UserSerializer


@api_view(["POST"])
def signup(request) -> Response:
    """
    Create new user and return token
    """
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_200_OK)

    serializer.save()
    user = User.objects.get(username=request.data["username"])
    user.set_password(request.data["password"])
    user.save()
    token = Token.objects.create(user=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["POST"])
def login(request) -> Response:
    """
    Returns token for already existing user
    """
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response(
            {"error": "Wrong password or login"}, status=status.HTTP_404_NOT_FOUND
        )
    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def info(request) -> Response:
    """
    Returns information about user / token
    """
    return Response({"user": UserSerializer(request.user).data})
