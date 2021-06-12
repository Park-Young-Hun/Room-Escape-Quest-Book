from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    # 화면 urls 항목
    path('', views.home, name='home'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:pk>', views.review_detail, name='review_detail'),
    path('b_item/', views.b_item, name='b_item_list'),


    # 사용자 관리
    path('member_register', views.member_register, name="member_register"),
    path('member_id_check', views.member_id_check, name="member_id_check"),
    path('member_insert', views.member_insert, name="member_insert"),
    path('member_login', views.member_login, name="member_login"),
    path('member_logout', views.member_logout, name="member_logout"),
    path('member_check', views.member_check, name="member_check"),
    path('member_pwd_check', views.member_pwd_check, name="member_pwd_check"),
    path('member_edit', views.member_edit, name="member_edit"),
    path('member_update', views.member_update, name="member_update"),

    ]
