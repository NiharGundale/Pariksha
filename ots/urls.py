from django.urls import path
from ots.views import *
app_name='ots'

urlpatterns=[
    path('',welcome),
    path('new-candidate',candidateRegistrationForm,name='registrationform'),
    path('storecandidate',candidateRegistration,name="storeCandidate"),
    path('login',loginview,name='login'),
    path('home',candidatehome,name='home'),
    path('test-paper',testpaper,name='testpaper'),
    path('calculate-result',calculateTestResult,name='calculateTest'),
    path('tes-history',testResultHistory,name='testHistory'),
    path('result',showTestResult,name='result'),
    path('logout',logoutView,name='logout'),



]