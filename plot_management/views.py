from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, mixins, viewsets, views, status
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

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
from django.conf import settings

from .serializers import MyAuthTokenSerializer
from datetime import *

from sslcommerz_python.payment import SSLCSession
from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django.db.models import Q


# Create your views here.


class MemberView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        try:
            query = Member.objects.get(email=request.user)
            query2 = User.objects.get(email=request.user)
            query3 = Profile.objects.get(prouser=request.user)
            serializer = MemberSerializer(query)
            serializer_data = serializer.data
            all_data = []
            serializer_user = UserSerializer(query2)
            serializer_profile = ProfileSerializers(query3)
            serializer_data["email_id"] = serializer_user.data
            serializer_data["profile"] = serializer_profile.data
            all_data.append(serializer_data)
            response_msg = {"error": False, "data": all_data}
        except:
            response_msg = {"error": True, "message": "Something is wrong !! Try again....."}
        return Response(response_msg)


class AllMemberView(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        query = Member.objects.all().order_by("-id")
        serializer = MemberSerializer(query, many=True)
        return Response(serializer.data)


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


class AdminRegister(views.APIView):
    def post(self, request):
        serializers = AdminUserSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response({"error": False, "message": f"Admin User is created for '{serializers.data['email']}'"})
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
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        query = Profile.objects.filter(prouser__is_superuser=False).order_by("-id")
        serializer = ProfileSerializers(query, many=True)
        return Response(serializer.data)


class StatusView(views.APIView):
    def get(self, request):
        query = Status.objects.all()
        serializer = StatusSerializer(query, many=True)
        return Response(serializer.data)


class PlotPositionView(views.APIView):
    def get(self, request):
        query = PlotPosition.objects.all().order_by("-id")
        serializer = PlotPositionSerializer(query, many=True)
        return Response(serializer.data)


class PlotPositionDelete(views.APIView):
    def post(self, request, pk):
        obj = PlotPosition.objects.get(id=pk)
        obj.delete()
        return Response({"message": "Plot Position With Road Deleted"})


class PlotDelete(views.APIView):
    def post(self, request, pk):
        obj = PlotNumber.objects.get(id=pk)
        obj.delete()
        return Response({"message": "Plot Deleted"})


class RoadDelete(views.APIView):
    def post(self, request, pk):
        obj = RoadNumber.objects.get(id=pk)
        obj.delete()
        return Response({"message": "Road Deleted"})


class RoadPlotView(views.APIView):
    def get(self, request):
        query1 = PlotNumber.objects.all().order_by("-id").values()
        query2 = RoadNumber.objects.all().order_by("-id").values()

        return Response({
            'plot': query1,
            'road': query2
        })


class AddMember(views.APIView):
    def post(self, request):
        data = request.data
        serializers = MemberSerializer(data=data, context={"request": request})

        if serializers.is_valid(raise_exception=True):
            email = data["email"]
            bank_name = data["bank_name"]
            cheque = data["cheque_no"]
            account_no = data["account_no"]
            member_nid = data["member_nid"]
            amount = data["amount"]

            OnetimeMembershipPayment.objects.create(
                member_email=email,
                bank_name=bank_name,
                cheque_number=cheque,
                account_no=account_no,
                member_nid=member_nid,
                amount=amount
            )
            serializers.save()

            return Response({"error": False, "message": "Member Added"})
        return Response({"error": True, "message": "Something is wrong"})


class AddPlotRoad(views.APIView):
    def post(self, request):
        data = request.data
        serializers = PlotPositionSerializer(data=data, context={"request": request})

        if serializers.is_valid(raise_exception=True):
            serializers.save()

            return Response({"error": False, "message": "Plot and Road Added"})
        return Response({"error": True, "message": "Something is wrong"})


class PlotAdd(views.APIView):
    def post(self, request):
        data = request.data
        serializers = PlotNumberSerializer(data=data, context={"request": request})

        if serializers.is_valid(raise_exception=True):
            serializers.save()

            return Response({"error": False, "message": "Plot Added"})
        return Response({"error": True, "message": "Something is wrong"})


class RoadAdd(views.APIView):
    def post(self, request):
        data = request.data
        serializers = RoadNumberSerializer(data=data, context={"request": request})

        if serializers.is_valid(raise_exception=True):
            serializers.save()

            return Response({"error": False, "message": "Road Added"})
        return Response({"error": True, "message": "Something is wrong"})


class TrackOwnerView(viewsets.ViewSet):
    def list(self, request):
        query = TrackPlotOwnership.objects.all().order_by("-id")
        serializer = TrackPlotOwnershipSerializer(query, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = TrackPlotOwnership.objects.filter(plot_no=pk)
        serializer = TrackPlotOwnershipSerializer(query, many=True)
        return Response(serializer.data)


class PlotOwnerAdd(views.APIView):
    def post(self, request):
        data = request.data
        serializers = TrackPlotOwnershipSerializer(data=data, context={"request": request})

        if serializers.is_valid(raise_exception=True):
            member_email = data["owner_email"]
            mem_stat = data["member_status"]
            plot_num = data["plot_no"]
            member_query = Member.objects.get(id=member_email)
            email = getattr(member_query, "email")

            print(member_email, plot_num, mem_stat)

            if TrackPlotOwnership.objects.filter(owner_email__email=email, plot_no=plot_num).exists():
                return Response({"error": True, "message": "Member With Same Plot Already Exists  !!"})
            else:
                query = PlotPosition.objects.get(plot_no=plot_num)
                road_num = getattr(query, "road_no")

                serializers.save()
                owner_obj = TrackPlotOwnership.objects.last()
                owner_obj.owner_email = Member.objects.get(id=member_email)
                owner_obj.member_status = Status.objects.get(id=mem_stat)
                owner_obj.road_no = road_num
                owner_obj.save()

                return Response({"error": False, "message": "Owner Added"})
        return Response({"error": True, "message": "Something is wrong"})


class RetrievePaymentView(views.APIView):
    def get(self, request, pk):
        member_query = Member.objects.get(email=pk)
        member_serializer = MemberSerializer(member_query)
        temp_serializer = member_serializer.data
        all_data = []

        owner_query = TrackPlotOwnership.objects.filter(owner_email__email=pk)
        owner_serializer = TrackPlotOwnershipSerializer(owner_query, many=True)

        temp_serializer["owner_plot_info"] = owner_serializer.data
        all_data.append(temp_serializer)

        return Response(all_data)


class GetPlotWithOwner(views.APIView):
    def post(self, request):
        data = request.data
        owner_mail = data["owner_email"]
        plot_id = data["plot_id"]
        query = TrackPlotOwnership.objects.filter(owner_email__email=owner_mail).filter(plot_no=plot_id)
        serializer = TrackPlotOwnershipSerializer(query, many=True)
        return Response(serializer.data)


class CreateOfflinePayment(views.APIView):
    def post(self, request):
        try:
            data = request.data

            email = data["member_email"]
            email_query = Member.objects.get(email=email)

            cheque = data["cheque_number"]
            account = data["account_no"]
            nid = data["member_nid"]
            plot = data["plot_no"]
            road = data["road_no"]

            status = data["member_status"]
            status_query = Status.objects.get(title=status)

            paid = data["paid_amount"]

            query = PaymentDateFix.objects.last()
            start_date = getattr(query, "start_date")
            end_date = getattr(query, "end_date")
            date_today = date.today()
            payment_status = ""



            if start_date <= date_today <= end_date:
                payment_status = "ontime"
            else:
                payment_status = "late"

            if TrackMembershipPayment.objects.filter(Q(member_email__member_email__email=email) |
                                                     Q(online_email__email__email=email), plot_no=plot,
                                                     start_date=start_date, end_date=end_date).exists():
                return Response({"error": True, "message": "Already paid within required time duration"})
            else:
                OfflinePayment.objects.create(
                    member_email=email_query,
                    cheque_number=cheque,
                    account_no=account,
                    member_nid=nid,
                    plot_no=plot,
                    road_no=road,
                    member_status=status_query,
                    paid_amount=paid,
                    start_date=start_date,
                    end_date=end_date
                )

                query2 = OfflinePayment.objects.last()

                TrackMembershipPayment.objects.create(
                    member_email=query2,
                    member_status=status,
                    plot_no=plot,
                    road_no=road,
                    payment_type="offline",
                    payment_status=payment_status,
                    start_date=start_date,
                    end_date=end_date
                )

                # print(start_date)
                # print(end_date)
                # print(date_today)
                # print(email)
                # print(cheque)
                # print(account)
                # print(nid)
                # print(plot)
                # print(road)
                # print(status)
                # print(paid)

            response_msg = {"error": False, "message": "Your Payment is complete"}
        except:
            response_msg = {"error": True, "message": "Something is wrong ! "}

        return Response(response_msg)


class DateHandle(viewsets.ViewSet):
    def list(self, request):
        query = PaymentDateFix.objects.all().order_by("-id")
        serializer = PaymentDateFixSerializer(query, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            data = request.data
            start_date = data["start_date"]
            end_date = data["end_date"]

            PaymentDateFix.objects.create(
                start_date=start_date,
                end_date=end_date
            )

            obj = TrackPlotOwnership.objects.all()

            for i in range(obj.count()):
                email = getattr(getattr(obj[i], "owner_email"), "email")
                plot_no = getattr(obj[i], "plot_no")
                member_status = getattr(getattr(obj[i], "member_status"), "title")
                amount = getattr(getattr(obj[i], "member_status"), "payment_range")

                TrackDueTable.objects.create(
                    owner_email=email,
                    start_date=start_date,
                    end_date=end_date,
                    plot_no=plot_no,
                    member_status=member_status,
                    amount=amount
                )

            response_msg = {"error": False, "message": "Date Added"}
        except:
            response_msg = {"error": True, "message": "Something is wrong ! "}

        return Response(response_msg)

    def destroy(self, request, pk=None):
        try:
            query = PaymentDateFix.objects.get(id=pk)
            query.delete()
            response_msg = {"error": False, "message": "Date is deleted"}
        except:
            response_msg = {"error": True, "message": "Something is wrong !!"}

        return Response(response_msg)


class ProfileImageUpdate(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            query = Profile.objects.get(prouser=user)

            serializers = ProfileSerializers(query, data=data, context={"request": request})
            serializers.is_valid(raise_exception=True)
            serializers.save()
            response_msg = {"error": False, "message": "Profile Image Updated !!"}
        except:
            response_msg = {"error": True, "message": "Profile Image not Update !! Try Again ...."}
        return Response(response_msg)


class UserDataUpdate(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            user = request.user
            data = request.data
            user_obj = Member.objects.get(email=user)
            user_obj.member_firstname = data["firstname"]
            user_obj.member_lastname = data["lastname"]
            user_obj.member_phone = data["phone"]
            user_obj.save()

            response_msg = {"error": False, "message": "User Data is Updated"}
        except:
            response_msg = {"error": True, "message": "User Data is not update !! Try Again ...."}
        return Response(response_msg)


class ChangePassword(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        user = request.user
        if user.check_password(request.data['old_pass']):
            user.set_password(request.data['new_pass'])
            user.save()
            response_msg = {"message": True}
            return Response(response_msg)
        else:
            response_msg = {"message": False}
            return Response(response_msg)


class UserPaymentInfo(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def list(self, request):
        user = request.user
        all_data = []
        query = TrackMembershipPayment.objects.filter(Q(member_email__member_email__email=user) |
                                                      Q(online_email__email__email=user)).order_by("-id")
        serializer = TrackMembershipPaymentSerializer(query, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        query = TrackMembershipPayment.objects.filter(id=pk)
        serializer = TrackMembershipPaymentSerializer(query, many=True)
        return Response(serializer.data)


class PlotOwner(views.APIView):

    def get(self, request):
        user = request.user
        query = TrackPlotOwnership.objects.filter(owner_email__email=user)
        serializer = TrackPlotOwnershipSerializer(query, many=True)
        return Response(serializer.data)


class UserPaymentView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user

        owner_query = TrackPlotOwnership.objects.filter(owner_email__email=user)
        owner_serializer = TrackPlotOwnershipSerializer(owner_query, many=True)

        return Response(owner_serializer.data)


class AllPaymentStatus(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        query1 = TrackMembershipPayment.objects.exclude(member_email__isnull=True).order_by("-id")
        serializer1 = TrackMembershipPaymentSerializer(query1, many=True)

        query2 = TrackMembershipPayment.objects.exclude(online_email__isnull=True).order_by("-id")
        serializer2 = TrackMembershipPaymentSerializer(query2, many=True)

        return Response({"offline": serializer1.data, "online": serializer2.data})


class MemberDelete(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request, pk, key):

        if key == "button1":
            obj = Member.objects.get(id=pk)
            email = getattr(obj, "email")
            member_firstname = getattr(obj, "member_firstname")
            member_lastname = getattr(obj, "member_lastname")
            member_nid = getattr(obj, "member_nid")
            member_phone = getattr(obj, "member_phone")

            plot_query1 = TrackPlotOwnership.objects.filter(owner_email__email=email)

            for i in range(plot_query1.count()):
                owner_email = getattr(plot_query1[i], "owner_email")
                plot_no = getattr(plot_query1[i], "plot_no")
                road_no = getattr(plot_query1[i], "road_no")
                member_status = getattr(plot_query1[i], "member_status")


                MemberHistory.objects.create(
                    owner_email=owner_email,
                    member_firstname=member_firstname,
                    member_lastname=member_lastname,
                    member_nid=member_nid,
                    member_phone=member_phone,
                    plot_no=plot_no,
                    road_no=road_no,
                    member_status=member_status
                )

            obj.delete()

        elif key == "button2":
            obj1 = Member.objects.get(id=pk)
            email = getattr(obj1, "email")
            member_firstname = getattr(obj1, "member_firstname")
            member_lastname = getattr(obj1, "member_lastname")
            member_nid = getattr(obj1, "member_nid")
            member_phone = getattr(obj1, "member_phone")

            obj2 = User.objects.get(email=email)
            plot_query2 = TrackPlotOwnership.objects.filter(owner_email__email=email)

            for i in range(plot_query2.count()):
                owner_email = getattr(plot_query2[i], "owner_email")
                plot_no = getattr(plot_query2[i], "plot_no")
                road_no = getattr(plot_query2[i], "road_no")
                member_status = getattr(plot_query2[i], "member_status")

                MemberHistory.objects.create(
                    owner_email=owner_email,
                    member_firstname=member_firstname,
                    member_lastname=member_lastname,
                    member_nid=member_nid,
                    member_phone=member_phone,
                    plot_no=plot_no,
                    road_no=road_no,
                    member_status=member_status
                )

            obj1.delete()
            obj2.delete()

        return Response({"OK"})


class OnlyUserDelete(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request, pk, key):
        if key == "button1":
            query = Profile.objects.get(id=pk)
            email = getattr(query, "prouser")
            obj = User.objects.get(email=email)

            if Member.objects.filter(email=email).exists():
                obj2 = Member.objects.get(email=email)
                email = getattr(obj2, "email")
                member_firstname = getattr(obj2, "member_firstname")
                member_lastname = getattr(obj2, "member_lastname")
                member_nid = getattr(obj2, "member_nid")
                member_phone = getattr(obj2, "member_phone")
                print(email, member_firstname, member_lastname, member_nid, member_phone)

                if TrackPlotOwnership.objects.filter(owner_email__email=email).exists():
                    plot_query = TrackPlotOwnership.objects.filter(owner_email__email=email)

                    for i in range(plot_query.count()):
                        owner_email = getattr(plot_query[i], "owner_email")
                        plot_no = getattr(plot_query[i], "plot_no")
                        road_no = getattr(plot_query[i], "road_no")
                        member_status = getattr(plot_query[i], "member_status")

                        MemberHistory.objects.create(
                            owner_email=owner_email,
                            member_firstname=member_firstname,
                            member_lastname=member_lastname,
                            member_nid=member_nid,
                            member_phone=member_phone,
                            plot_no=plot_no,
                            road_no=road_no,
                            member_status=member_status
                        )

                    print("Owner Exists")
                    obj.delete()
                    obj2.delete()

                else:
                    print("No Owner Found")
                    obj.delete()
                    obj2.delete()
            else:
                print("Not a Member")
                obj.delete()

        return Response({"OK"})


class OwnerHistory(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        query = MemberHistory.objects.all().order_by("-id")
        serializer = MemberHistorySerializer(query, many=True)
        return Response(serializer.data)


class OwnerDelete(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request, pk, key):
        if key == "button1":
            query = TrackPlotOwnership.objects.get(id=pk)
            owner_email = getattr(query, "owner_email")
            plot_no = getattr(query, "plot_no")
            road_no = getattr(query, "road_no")
            member_status = getattr(query, "member_status")

            member_obj = Member.objects.get(email=owner_email)
            member_firstname = getattr(member_obj, "member_firstname")
            member_lastname = getattr(member_obj, "member_lastname")
            member_nid = getattr(member_obj, "member_nid")
            member_phone = getattr(member_obj, "member_phone")

            MemberHistory.objects.create(
                owner_email=owner_email,
                member_firstname=member_firstname,
                member_lastname=member_lastname,
                member_nid=member_nid,
                member_phone=member_phone,
                plot_no=plot_no,
                road_no=road_no,
                member_status=member_status
            )
            query.delete()

        return Response({"OK"})


class AdminView(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        query = Profile.objects.filter(prouser__is_superuser=True).order_by("-id")
        serializer = ProfileSerializers(query, many=True)

        return Response(serializer.data)


class AdminDelete(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request, pk, key):
        if key == "button1":
            query = User.objects.get(id=pk)
            query.delete()

        return Response({"Admin User Deleted"})


class MemberDetails(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request, pk):
        member_query = Member.objects.get(id=pk)
        email = getattr(member_query, "email")
        member_serializer = MemberSerializer(member_query)
        serializer = member_serializer.data
        all_data = []

        profile_query = Profile.objects.get(prouser__email=email)
        pro_serializer = ProfileSerializers(profile_query)
        serializer["profile"] = pro_serializer.data
        all_data.append(serializer)

        return Response(all_data)


class TableCount(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        user = User.objects.all().values().count()
        member = Member.objects.all().values().count()
        plot = PlotNumber.objects.all().values().count()
        road = RoadNumber.objects.all().values().count()
        assigned_plot = PlotPosition.objects.all().values().count()
        online = PayOnline.objects.all().values().count()
        offline = OfflinePayment.objects.all().values().count()
        return Response({
            "user": user,
            "member": member,
            "plot": plot,
            "road": road,
            "assigned_plot": assigned_plot,
            "online": online,
            "offline": offline
        })


class UpdateStatusAmount(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        data = request.data
        pk = data["id"]
        name = data["name"]
        amount = data["amount"]

        if name == "Main":
            obj = Status.objects.get(id=pk)
            obj.payment_range = amount
            obj.date = date.today()
            obj.save()

        elif name == "General":
            obj = Status.objects.get(id=pk)
            obj.payment_range = amount
            obj.date = date.today()
            obj.save()
        else:
            print("doesn't work")
        return Response({"OK"})


class PaymentBoolean(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request, pk, plot):
        query = TrackMembershipPayment.objects.filter(Q(member_email__member_email__email=pk) |
                                                      Q(online_email__email__email=pk), plot_no=plot).exists()
        return Response({"message": query})


class PlotOwnerUpdate(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        data = request.data

        pk = data["id"]
        plot_no = data["plot_no"]
        plot_id = data["plot_id"]
        status_no = data["status_no"]
        bool_delete = data["bool_delete"]

        query = TrackPlotOwnership.objects.get(id=pk)
        email = getattr(query, "owner_email")
        obj = TrackMembershipPayment.objects.filter(Q(member_email__member_email__email=email) |
                                                      Q(online_email__email__email=email), plot_no=plot_id).exists()
        print(email)
        print(pk, plot_no, status_no, bool_delete)
        print(obj)
        if bool_delete == "true":
            print("Bool True")

            if plot_no == "null" and status_no == "null":
                return Response({"message": "all_null"})

            elif plot_no == "null" and status_no != "null":
                return Response({"message": "plot_null"})

            elif plot_no != "null" and status_no == "null":
                return Response({"message": "status_null"})

            elif plot_no != "null" and status_no != "null":

                if obj == True:
                    plot = getattr(query, "plot_no")
                    road = getattr(query, "road_no")
                    member_status = getattr(query, "member_status")

                    member_obj = Member.objects.get(email=email)
                    member_firstname = getattr(member_obj, "member_firstname")
                    member_lastname = getattr(member_obj, "member_lastname")
                    member_nid = getattr(member_obj, "member_nid")
                    member_phone = getattr(member_obj, "member_phone")

                    MemberHistory.objects.create(
                        owner_email=email,
                        member_firstname=member_firstname,
                        member_lastname=member_lastname,
                        member_nid=member_nid,
                        member_phone=member_phone,
                        plot_no=plot,
                        road_no=road,
                        member_status=member_status
                    )
                    status_query = Status.objects.get(id=status_no)
                    member_query = Member.objects.get(email=email)
                    road_query = PlotPosition.objects.get(plot_no=plot_no)
                    road_num = getattr(road_query, "road_no")

                    TrackPlotOwnership.objects.create(
                        owner_email=member_query,
                        plot_no=plot_no,
                        road_no=road_num,
                        member_status=status_query
                    )
                    query.delete()

                elif obj == False:
                    up_obj = TrackPlotOwnership.objects.get(id=pk)
                    status_query = Status.objects.get(id=status_no)
                    road_query = PlotPosition.objects.get(plot_no=plot_no)
                    road_num = getattr(road_query, "road_no")

                    up_obj.plot_no = plot_no
                    up_obj.road_no = road_num
                    up_obj.member_status = status_query
                    up_obj.save()

                    print("I'm gonna just update")

        elif plot_no == "null" and status_no == "null":
            return Response({"message": "all_null"})

        elif plot_no == "null" and status_no != "null":
            print("Status not null")

        elif plot_no != "null" and status_no == "null":
            # Check if any payment record exists, if not then update else show error response
            if obj == True:
                return Response({"message": "delete_record"})
            elif obj == False:
                up_obj = TrackPlotOwnership.objects.get(id=pk)
                road_query = PlotPosition.objects.get(plot_no=plot_no)
                road_num = getattr(road_query, "road_no")

                up_obj.plot_no = plot_no
                up_obj.road_no = road_num
                up_obj.save()
                print("Can Update")

        elif plot_no != "null" and status_no != "null":
            # Check if mistakenly any payment record exists, if found response "delete_record" else update
            if obj == True:
                return Response({"message": "delete_record"})
            elif obj == False:
                up_obj = TrackPlotOwnership.objects.get(id=pk)
                status_query = Status.objects.get(id=status_no)
                road_query = PlotPosition.objects.get(plot_no=plot_no)
                road_num = getattr(road_query, "road_no")

                up_obj.plot_no = plot_no
                up_obj.road_no = road_num
                up_obj.member_status = status_query
                up_obj.save()
            print("Plot and Status both not null")

        return Response({"OK"})


class ShowPayment(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        grand_amount = 0
        offline_amount = 0
        pay_online = 0
        onetime_amount = 0

        query1 = TrackMembershipPayment.objects.exclude(member_email__isnull=True).order_by("-id")
        serializer1 = TrackMembershipPaymentSerializer(query1, many=True)

        query2 = TrackMembershipPayment.objects.exclude(online_email__isnull=True).order_by("-id")
        serializer2 = TrackMembershipPaymentSerializer(query2, many=True)

        query3 = OnetimeMembershipPayment.objects.all()
        serializer3 = OnetimeMembershipPaymentSerializer(query3, many=True)

        obj1 = OfflinePayment.objects.all()
        obj2 = PayOnline.objects.all()
        obj3 = OnetimeMembershipPayment.objects.all()

        for i in range(obj1.count()):
            paid_amount = getattr(obj1[i], "paid_amount")
            grand_amount += float(paid_amount)
            offline_amount += float(paid_amount)

        for j in range(obj2.count()):
            paid_amount = getattr(obj2[j], "paid_amount")
            grand_amount += float(paid_amount)
            pay_online = pay_online + float(paid_amount)

        for k in range(obj3.count()):
            amount = getattr(obj3[k], "amount")
            grand_amount += float(amount)
            onetime_amount += float(amount)

        return Response({"offline": serializer1.data, "online": serializer2.data,
                         "onetime": serializer3.data, "grand_amount": grand_amount, "online_amount": pay_online,
                         "offline_amount": offline_amount, "onetime_amount": onetime_amount})


class FilterPayment(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request, pk, start_date, end_date):

        if pk == "offline":
            amount = 0
            offline_query = OfflinePayment.objects.filter(payment_date__range=[start_date, end_date])

            for i in range(offline_query.count()):
                paid_amount = getattr(offline_query[i], "paid_amount")
                amount += float(paid_amount)
            query1 = TrackMembershipPayment.objects.filter(date__range=[start_date, end_date],
                                                           member_email__isnull=False)
            offline_serializer = TrackMembershipPaymentSerializer(query1, many=True)
            return Response({"type": pk, "data": offline_serializer.data, "total": amount})

        elif pk == "online":
            amount = 0
            online_query = PayOnline.objects.filter(payment_date__range=[start_date, end_date])

            for i in range(online_query.count()):
                paid_amount = getattr(online_query[i], "paid_amount")
                amount += float(paid_amount)
            query2 = TrackMembershipPayment.objects.filter(date__range=[start_date, end_date],
                                                           online_email__isnull=False)
            online_serializer = TrackMembershipPaymentSerializer(query2, many=True)
            return Response({"type": pk, "data": online_serializer.data, "total": amount})

        elif pk == "onetime":
            amount = 0
            onetime_query = OnetimeMembershipPayment.objects.filter(date__range=[start_date, end_date])

            for i in range(onetime_query.count()):
                paid_amount = getattr(onetime_query[i], "amount")
                amount += float(paid_amount)

            onetime_serializer = OnetimeMembershipPaymentSerializer(onetime_query, many=True)
            return Response({"type": pk, "data": onetime_serializer.data, "total": amount})

        return Response({"OK"})


class BankAndAmount(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        query1 = BankName.objects.all().order_by("-id")
        serializer1 = BankSerializer(query1, many=True)

        query2 = OnetimeAmount.objects.all()
        serializer2 = OnetimeAmountSerializer(query2, many=True)

        return Response({"bank_name": serializer1.data, "onetime_amount": serializer2.data})


class PaymentDueView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        amount = 0
        user = request.user
        email = getattr(user, "email")

        track_due = TrackDueTable.objects.filter(owner_email=email, paid=False)
        serializer = TrackDueTableSerializer(track_due, many=True)

        for i in range(track_due.count()):
            current_amount = getattr(track_due[i], "amount")
            amount += float(current_amount)

        return Response({"info": serializer.data, "total_due": amount})


class AllDueView(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        amount = 0
        query = TrackDueTable.objects.filter(paid=False)
        serializer = TrackDueTableSerializer(query, many=True)

        for i in range(query.count()):
            payment_amount = getattr(query[i], "amount")
            amount += float(payment_amount)

        return Response({"info": serializer.data, "total_due": amount})


class OnlinePayment(views.APIView):
    def post(self, request):
        data = request.data

        email = data["email"]
        phone = data["phone"]
        name = data["name"]
        nid = data["nid"]
        plot_no = data["plot_no"]
        road_no = data["road_no"]
        member_status = data["member_status"]
        payment_amount = data["payment_amount"]

        query = PaymentDateFix.objects.last()

        start_date = getattr(query, "start_date")
        end_date = getattr(query, "end_date")
        date_today = date.today()

        if TrackMembershipPayment.objects.filter(Q(member_email__member_email__email=email) |
                                                 Q(online_email__email__email=email),
                                                 plot_no=plot_no, start_date=start_date, end_date=end_date).exists():

            return Response({"data": "invalid"})

        else:
            store_id = settings.STORE_ID
            store_pass = settings.STORE_PASS
            mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

            status_url = request.build_absolute_uri(reverse('status'))
            mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

            mypayment.set_product_integration(total_amount=Decimal(payment_amount), currency='BDT',
                                              product_category='Membership Payment', product_name='None',
                                              num_of_item=1, shipping_method='online',
                                              product_profile='None')

            mypayment.set_customer_info(name=name, email=email,
                                        address1=plot_no, address2=road_no,
                                        city='Dhaka, Ashulia', postcode='None',
                                        country='Bangladesh', phone=phone)

            mypayment.set_shipping_info(shipping_to=email, address=plot_no,
                                        city='Dhaka, Ashulia', postcode='None',
                                        country='Bangladesh')

            mypayment.set_additional_values(value_a=email, value_b=plot_no, value_c=road_no,
                                            value_d=member_status)

            response_data = mypayment.init_payment()

            print(response_data['GatewayPageURL'])

            return Response(response_data['GatewayPageURL'])


@csrf_exempt
@api_view(['POST'])
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            value_a = payment_data['value_a']
            value_b = payment_data['value_b']
            value_c = payment_data['value_c']
            value_d = payment_data['value_d']
            amount = payment_data['amount']
            medium = payment_data['card_issuer']
            print(payment_data)

            email_query = Member.objects.get(email=value_a)
            status_query = Status.objects.get(title=value_d)

            nid = getattr(email_query, 'member_nid')

            query = PaymentDateFix.objects.last()

            start_date = getattr(query, "start_date")
            end_date = getattr(query, "end_date")

            date_today = date.today()
            payment_status = ""

            if start_date <= date_today <= end_date:
                payment_status = "ontime"
            else:
                payment_status = "late"

            PayOnline.objects.create(
                email=email_query,
                transaction_id=tran_id,
                medium=medium,
                member_nid=nid,
                plot_no=value_b,
                road_no=value_c,
                member_status=status_query,
                paid_amount=amount,
                start_date=start_date,
                end_date=end_date
            )

            query2 = PayOnline.objects.last()

            TrackMembershipPayment.objects.create(
                online_email=query2,
                member_status=value_d,
                plot_no=value_b,
                road_no=value_c,
                payment_type="online",
                payment_status=payment_status,
                start_date=start_date,
                end_date=end_date
            )

            track_due = TrackDueTable.objects.get(owner_email=value_a, plot_no=value_b, start_date=start_date,
                                                  end_date=end_date)
            track_due.paid = True
            track_due.save()

            return redirect("http://localhost:3000/user_payment_status")

        elif status == "FAILED":
            return redirect("http://localhost:3000/user_payment_status")


def sslc_complete(request, val_id, tran_id, value_a, value_b, value_c, value_d):
    pass
