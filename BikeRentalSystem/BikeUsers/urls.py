from django.urls import path
from django.contrib.auth import views as auth_view
from .views import *

urlpatterns = [
    path('', view=home, name='CustomerHome'),
    path('add_station', view=add_station, name='AddStation'),
    path('register/', view=SignUpView.as_view(), name='CustomerRegister'),
    path('login/', view=SignIn.as_view(), name='CustomerLogin'),
    path('logout/', view=auth_view.LogoutView.as_view(template_name='BikeUsers/login.html'), name='CustomerLogout'),
    path('bikeadd/', view=BikeAddView.as_view(), name='BikeRegister'),
    path('bike/<int:pk>/update/', view=BikeUpdateView.as_view(), name='Bike-UpdateView'),
    path('bike/<int:pk>/delete/', view=BikeDeleteView.as_view(), name='Bike-DeleteView'),
    path('feedback/', view=Rettingadd.as_view(), name='BikeRegister'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='BikeUsers/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="BikeUsers/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='BikeUsers/password/password_reset_complete.html'), name='password_reset_complete'),  
    path("password_reset/", password_reset_request, name="password_reset"),
    path('search_city/', view=search_city, name='SearchCity'),
    path('search_station/', view=search_station, name='SearchStation'),
    path('get_map/<int:pk>/', view=get_map, name='GetMap'),
    path('bike/<int:pk>/',view=Bikedetails.as_view(),name='ShowBikeDetails'),
]

