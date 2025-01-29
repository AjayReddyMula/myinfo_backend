from django.urls import path
from myinfo import views

app_name = 'myinfo'

urlpatterns = [
    path("authorize/", views.MyInfoAuthorizeAPIView.as_view(), name="authorize"),
    path("callback/", views.MyInfoCallbackAPIView.as_view(), name="callback"),
]
