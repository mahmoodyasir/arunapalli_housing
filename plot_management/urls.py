from django.urls import path, include
from rest_framework import routers
from .views import *
from .views import obtain_auth_token

route = routers.DefaultRouter()
route.register("all_owner_view", TrackOwnerView, basename="all_owner_view")
# route.register("category", CategoryView, basename="CategoryView")


urlpatterns = [
    path("", include(route.urls)),
    path('member/', MemberView.as_view(), name="member"),
    path('all_member_view/', AllMemberView.as_view(), name="all_member_view"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', obtain_auth_token),
    path('admin_login/', CustomAuthToken.as_view(), name="admin_login"),
    path('admin_profile/', AdminProfileView.as_view(), name="admin_profile"),
    path('memberapi/', MemberAPI.as_view(), name="memberapi"),
    path('profileview/', ProfileView.as_view(), name="profileview"),
    path('statusview/', StatusView.as_view(), name="statusview"),
    path('add_member/', AddMember.as_view(), name="add_member"),
    path('plotpositionview/', PlotPositionView.as_view(), name="plotview"),
    path('roadplotview/', RoadPlotView.as_view(), name="roadplotview"),
    path('add_plot_road/', AddPlotRoad.as_view(), name="add_plot_road"),
    path('plot_add/', PlotAdd.as_view(), name="plot_add"),
    path('road_add/', RoadAdd.as_view(), name="road_add"),
    path('add_plot_owner/', PlotOwnerAdd.as_view(), name="add_plot_owner"),
    # path('all_owner_view/', TrackOwnerView.as_view(), name="all_owner_view"),
    # path('product/', ProductView.as_view(), name="product"),
    # path('product/<int:id>/', ProductView.as_view(), name="product"),

]
