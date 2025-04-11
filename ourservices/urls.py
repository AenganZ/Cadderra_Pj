from django.urls import path
from . import views

urlpatterns = [
    path('service1/', views.service1, name='service1'),
    path('', views.chatbot, name='chatbot'),
    path('get_response/', views.get_bot_response, name='get_bot_response'),
    path('service3/', views.service3, name='service3'),
    path('service4/', views.service4, name='service4'),
    path('service5/', views.service5, name='service5'),
    path('service6/', views.service6, name='service6'),
    path('law/terms/', views.terms, name='terms'),
    path('law/privacy/', views.privacy, name='privacy'),  # '개인정보처리방침' 페이지
    path('law/privacy-details/', views.privacy_details, name='privacy_details'),  # '개인정보 이용내역' 페이지
    path('check_login/', views.check_login, name='check_login'),
    path('user_usage_history/', views.user_usage_history, name='user_usage_history'),
    path('contact/', views.contact, name='contact'),
]
