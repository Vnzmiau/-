from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('applications/', views.manageApplications, name='applications_list'),
    path('applications/<int:application_id>/', views.manageApplication, name='application_detail'),
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutpage,name='logout'),
    path('api/login/', views.api_login, name='api_login'), 
]
