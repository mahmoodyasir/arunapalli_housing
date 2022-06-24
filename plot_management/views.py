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
    # authentication_classes = [TokenAuthentication, ]
    # permission_classes = [IsAdminUser, ]

    def get(self, request):
        query = Member.objects.all()
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


class PlotPositionView(views.APIView):
    def get(self, request):
        query = PlotPosition.objects.all().order_by("-id")
        serializer = PlotPositionSerializer(query, many=True)
        return Response(serializer.data)


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
            # mem_stat = data["member_status"]
            serializers.save()
            # member_obj = Member.objects.last()
            # member_obj.member_status = Status.objects.get(id=mem_stat)
            # member_obj.save()

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
            # print(user_obj)
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
    def get(self, request):
        user = request.user

        owner_query = TrackPlotOwnership.objects.filter(owner_email__email=user)
        owner_serializer = TrackPlotOwnershipSerializer(owner_query, many=True)

        return Response(owner_serializer.data)


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

            return redirect("http://localhost:3000/user_payment_status")


def sslc_complete(request, val_id, tran_id, value_a, value_b, value_c, value_d):
    pass
