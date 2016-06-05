# -*- coding: utf-8 -*-

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=30,
                                     required=False)
    password = serializers.CharField(max_length=62, required=True)
    phone = serializers.CharField(max_length=15, required=False)
    app_token = serializers.CharField(max_length=30, required=True)
