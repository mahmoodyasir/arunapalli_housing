from django.shortcuts import render
from rest_framework import generics, mixins, viewsets, views, status
from rest_framework.response import Response

from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.authtoken import views as auth_views
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema

from .serializers import MyAuthTokenSerializer

# Create your views here.


class MemberView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        try:
            query = Member.objects.get(member_email__prouser__email=request.user)
            query2 = User.objects.get(email=request.user)
            serializer = MemberSerializer(query)
            serializer_data = serializer.data
            all_data = []
            serializer_user = UserSerializer(query2)
            serializer_data["email_id"] = serializer_user.data
            all_data.append(serializer_data)
            response_msg = {"error": False, "data": all_data}
        except:
            response_msg = {"error": True, "message": "Something is wrong !! Try again....."}
        return Response(response_msg)


class AdminProfileView(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        try:
            query = AdminUserInfo.objects.get(admin_email=request.user)
            query2 = Profile.objects.get(prouser=request.user)
            serializer = AdminUserInfoSerializer(query)
            serializer_data = serializer.data
            all_data = []
            serializer_user = ProfileSerializers(query2)
            serializer_data["profile_info"] = serializer_user.data
            all_data.append(serializer_data)
            response_msg = {"error": False, "data": all_data}
        except:
            response_msg = {"error": True, "message": "Something is wrong !! Try again....."}
        return Response(response_msg)


class MyAuthToken(auth_views.ObtainAuthToken):
    serializer_class = MyAuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )


obtain_auth_token = MyAuthToken.as_view()


class CustomAuthToken(MyAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'admin_token': token.key,
                'user_id': user.pk,
                'email': user.email,
                "message": True
            })
        else:
            return Response({"error": True, "message": False})


class RegisterView(views.APIView):
    def post(self, request):
        serializers = UserSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response({"error": False, "message": f"User is created for '{serializers.data['email']}'"})
        return Response({"error": True, "message": "Something is wrong"})

# General Model Serializing


# class MemberAPI(views.APIView):
#     def get(self, request):
#         query = Member.objects.all()
#         serializer = MemberSerializer(query, many=True)
#         sub_serial = UserSerializer(query, many=True)
#         serializer_data = serializer.data
#         all_data = []
#         serializer_data["sub_serial"] = sub_serial.data
#         all_data.append(serializer_data)
#         return Response(all_data)


class MemberAPI(views.APIView):

    def get(self, request):
        try:
            query = Member.objects.all()
            query2 = Member.objects.all()
            serializer = MemberSerializer(query, many=True)
            serializer_data = serializer.data
            all_data = []
            serializer_user = UserSerializer(query2, many=True)
            serializer_data["email_id"] = serializer_user.data
            all_data.append(serializer_data)
            response_msg = {"error": False, "data": all_data}
        except:
            response_msg = {"error": True, "message": "Something is wrong !! Try again....."}
        return Response(response_msg)


class ProfileView(views.APIView):
    def get(self, request):
        query = Profile.objects.all()
        serializer = ProfileSerializers(query, many=True)
        return Response(serializer.data)


class StatusView(views.APIView):
    def get(self, request):
        query = Status.objects.all()
        serializer = StatusSerializer(query, many=True)
        return Response(serializer.data)


class AddMember(views.APIView):
    def post(self, request):
        data = request.data
        serializers = MemberSerializer(data=data, context={"request": request})

        if serializers.is_valid(raise_exception=True):
            serializers.save()

            return Response({"error": False, "message": "Member Added"})
        return Response({"error": True, "message": "Something is wrong"})