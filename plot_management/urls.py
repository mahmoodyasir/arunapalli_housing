from django.urls import path, include
from rest_framework import routers
from .views import *
from .views import obtain_auth_token

route = routers.DefaultRouter()
# route.register("memberapi", MemberAPI, basename="memberapi")
# route.register("category", CategoryView, basename="CategoryView")


urlpatterns = [
    path("", include(route.urls)),
    path('member/', MemberView.as_view(), name="member"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', obtain_auth_token),
    path('admin_login/', CustomAuthToken.as_view(), name="admin_login"),
    path('admin_profile/', AdminProfileView.as_view(), name="admin_profile"),
    path('memberapi/', MemberAPI.as_view(), name="memberapi"),
    path('profileview/', ProfileView.as_view(), name="profileview"),
    path('statusview/', StatusView.as_view(), name="statusview"),
    path('add_member/', AddMember.as_view(), name="add_member"),
    # path('product/', ProductView.as_view(), name="product"),
    # path('product/<int:id>/', ProductView.as_view(), name="product"),

]
