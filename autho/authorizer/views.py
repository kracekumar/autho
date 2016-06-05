# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate

from rest_framework import views, status
from rest_framework.response import Response

from .serializers import LoginSerializer
from .models import OrganizationUser, Application, UserInfo


class HTTPException(Exception):
    def __init__(self, data, status, *args, **kwargs):
        super(HTTPException, self).__init__(*args, **kwargs)
        self.data = data or {}
        self.status = status


class LoginAPIView(views.APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            return self.authenticate(serializer)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def verify_token(self, serializer):
        token = Application.objects.filter(token=serializer.data['app_token'])
        if not token:
            raise HTTPException(data={'app_token': 'Incorrect token'},
                                status=status.HTTP_400_BAD_REQUEST)

    def authenticate_by_username(self, serializer):
        user = authenticate(
            username=serializer.data['username'],
            password=serializer.data['password'])
        return user

    def authenticate_by_phone(self, serializer):
        phone = serializer.data.get('phone')
        user_info = UserInfo.objects.filter(phone=phone).all()
        if user_info:
            user_obj = user_info[0].user
            user = authenticate(
                username=user_obj.username,
                password=serializer.data['password'])
            return user
        else:
            raise HTTPException({'phone': 'This field is required'},
                                status=status.HTTP_400_BAD_REQUEST)

    def fetch_data(self, user):
        if user:
            return self.format_data(user)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def authenticate(self, serializer):
        try:
            self.verify_token(serializer)
            if serializer.data.get('username'):
                user = self.authenticate_by_username(serializer)
                return self.fetch_data(user)
            elif serializer.data.get('phone'):
                user = self.authenticate_by_phone(serializer)
                return self.fetch_data(user)
            else:
                return Response({'username': 'This field is required'},
                                status=status.HTTP_400_BAD_REQUEST)
        except HTTPException as e:
            return Response(e.data, status=e.status)

    def format_data(self, user):
        resp_data = {'role': []}
        org_user = OrganizationUser.objects.filter(user=user).all()[0]
        userrole_set = org_user.userrole_set.all()
        for userrole in userrole_set:
            role_data = {'name': userrole.role.name, 'id': userrole.role.id,
                         'permission': []}
            for role_perm in userrole.role.rolepermission_set.all():
                perm_data = {'name': role_perm.permission.name}
                perm_data.update(role_perm.to_dict())
                role_data['permission'].append(perm_data)
            resp_data['role'].append(role_data)
        return Response(resp_data, status=status.HTTP_200_OK)
