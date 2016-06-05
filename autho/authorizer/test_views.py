# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase

from .models import (Organization, OrganizationUser,
                     UserInfo, Application, Permissions,
                     Role, RolePermission, UserRole)
# Create your tests here.


class LoginApiTestCase(APITestCase):
    def setUp(self):
        # super(LoginApiTestCase).setUp()
        User = get_user_model()
        self.email = "johndoe@example.com"
        self.username = 'johndoe'
        self.password = 'password'
        self.phone = "+91919911"
        # User
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.user_info = UserInfo.objects.create(user=self.user,
                                                 phone=self.phone)
        self.organization = Organization.objects.create(name='Org')
        self.org_user = OrganizationUser.objects.create(
            organization=self.organization, user=self.user)
        self.application = Application.objects.create(
            name='App', token='token', organization=self.organization)
        self.permission = Permissions.objects.create(
            name='Report', app=self.application)
        self.role = Role.objects.create(
            organization=self.organization, name='Supervisor',
            app=self.application)
        self.role_perm = RolePermission.objects.create(
            role=self.role, permission=self.permission,
            is_internal=False, can_create=True, can_read=True,
            can_edit=True, can_delete=True)
        self.user_role = UserRole.objects.create(
            role=self.role, organization_user=self.org_user)
        self.client = APIClient()

    def test_login_by_username(self):
        url = reverse('login-view')
        data = {'username': self.user.username,
                'password': self.password,
                'app_token': self.application.token}
        resp = self.client.post(url, format='json', data=data)
        assert resp.status_code == 200

        data = resp.data
        assert len(data['role']) == 1
        assert len(data['role'][0]['permission']) == 1

        assert data['role'][0]['name'] == self.role.name
        assert data['role'][0]['permission'][0]['name'] == self.permission.name
        assert data['role'][0]['permission'][0]['is_internal'] == self.role_perm.is_internal  # noqa
        assert data['role'][0]['permission'][0]['can_create'] == self.role_perm.can_create  # noqa
        assert data['role'][0]['permission'][0]['can_read'] == self.role_perm.can_read  # noqa
        assert data['role'][0]['permission'][0]['can_edit'] == self.role_perm.can_edit  # noqa
        assert data['role'][0]['permission'][0]['can_delete'] == self.role_perm.can_delete  # noqa

    def test_login_by_phone(self):
        url = reverse('login-view')
        data = {'phone': self.user_info.phone,
                'password': self.password,
                'app_token': self.application.token}
        resp = self.client.post(url, format='json', data=data)
        assert resp.status_code == 200

        data = resp.data
        assert len(data['role']) == 1
        assert len(data['role'][0]['permission']) == 1

        assert data['role'][0]['name'] == self.role.name
        assert data['role'][0]['permission'][0]['name'] == self.permission.name
        assert data['role'][0]['permission'][0]['is_internal'] == self.role_perm.is_internal  # noqa
        assert data['role'][0]['permission'][0]['can_create'] == self.role_perm.can_create  # noqa
        assert data['role'][0]['permission'][0]['can_read'] == self.role_perm.can_read  # noqa
        assert data['role'][0]['permission'][0]['can_edit'] == self.role_perm.can_edit  # noqa
        assert data['role'][0]['permission'][0]['can_delete'] == self.role_perm.can_delete  # noqa

    def test_login_without_app_token(self):
        url = reverse('login-view')
        data = {'phone': self.user_info.phone,
                'password': self.password}
        resp = self.client.post(url, format='json', data=data)
        assert resp.status_code == 400

    def test_login_with_wrong_username(self):
        url = reverse('login-view')
        data = {'username': self.user_info.phone,
                'password': self.password,
                'app_token': self.application.token}
        resp = self.client.post(url, format='json', data=data)
        assert resp.status_code == 401

    def test_login_with_wrong_password(self):
        url = reverse('login-view')
        data = {'phone': self.user_info.phone,
                'password': 'self.password',
                'app_token': self.application.token}
        resp = self.client.post(url, format='json', data=data)
        assert resp.status_code == 401
