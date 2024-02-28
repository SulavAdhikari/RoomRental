from django.urls import path
from .views import predict_price ,accept_application, room_apply, home, profile, post_room, marketplace, room_detail, logout_view, register, user_login

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='user_profile'),
    path('predict/', predict_price, name='price_predict'),
    path('postroom/', post_room, name='post_room'),
    path('marketplace/', marketplace, name='marketplace'),
    path('room/<int:id>/', room_detail, name='room_detail'),
    path('login/', user_login, name='user_login'),
    path('logout/', logout_view, name='user_logout'),
    path('register/',register, name='user_register'),
    path('apply/<int:room_id>/',room_apply, name='room_apply'),
    path('accept/<int:app_id>/',accept_application, name='accept_applicant'),
]

