from asyncio import exceptions

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {"password": {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        Profile.objects.create(prouser=user)
        return user


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {"password": {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        Token.objects.create(user=user)
        Profile.objects.create(prouser=user)
        AdminUserInfo.objects.create(admin_email=user)
        return user


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['prouser']

    def validate(self, attrs):
        attrs['prouser'] = self.context['request'].user
        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['prouser'] = UserSerializer(instance.prouser).data
        return response


class AdminUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUserInfo
        fields = "__all__"
        read_only_fields = ['admin_email']

    def validate(self, attrs):
        attrs['admin_email'] = self.context['request'].user
        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['admin_email'] = UserSerializer(instance.admin_email).data
        return response


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
        depth = 1
    #     read_only_fields = ['member_email']
    #
    # def validate(self, attrs):
    #     attrs['member_email'] = self.context['request'].user
    #     return attrs
    #
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['member_email'] = UserSerializer(instance.member_email).data
    #     return response


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password",),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
        depth = 1


class PlotPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotPosition
        fields = "__all__"
        depth = 1


class RoadNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadNumber
        fields = "__all__"
        depth = 1


class PlotNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlotNumber
        fields = "__all__"
        depth = 1


class TrackPlotOwnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPlotOwnership
        fields = "__all__"
        depth = 1


class PaymentDateFixSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDateFix
        fields = "__all__"
        depth = 1


class OfflinePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflinePayment
        fields = "__all__"
        depth = 1


class TrackMembershipPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackMembershipPayment
        fields = "__all__"
        depth = 2


class OfflineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflinePayment
        fields = "__all__"
        depth = 1


class PayOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayOnline
        fields = "__all__"
        depth = 1


class MemberHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberHistory
        fields = "__all__"
        depth = 1







