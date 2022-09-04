from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import (
    AdminSerializer, StandartUserSerializer, TokenSerializer)
from api import permissions

from users.models import User


class SignUpAPI(APIView):
    """Registration request"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = StandartUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                User, username=serializer.data['username'])
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Confirmate registration on YaMDB',
                message=f'Confirmate your email clicking {confirmation_code}',
                from_email='master@yamdb.com',
                recipient_list=(serializer.data['email'],),
            )
            return Response(
                {'email': serializer.data['email'],
                    'username': serializer.data['username']},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenAPI(APIView):
    """Token obtain request"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])
            if default_token_generator.check_token(
                    user, serializer.data['confirmation_code']):
                access_token = AccessToken.for_user(user)
                return Response(
                    {'token': str(access_token)}, status=status.HTTP_200_OK
                )
        return Response(
            {'confirmation_code': 'Invalid confirmation_code'},
            status=status.HTTP_400_BAD_REQUEST)


class UserDataAPI(APIView):
    """User can process own data"""
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = StandartUserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = StandartUserSerializer(
            user, many=False, partial=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDataAPI(ModelViewSet):
    """Admin can process users data"""
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
