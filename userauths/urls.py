from django.urls import path
from userauths import views
from userauths.views import CustomPasswordChangeView


app_name = 'userauths'

urlpatterns = [
    path("sign-up/", views.register_view, name = "sign-up"),
    path("login/", views.login_view, name = "login"),
    path("sign-out/", views.logout_view, name = "sign-out"),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change-password'),
    path('activate/', views.activate_account_view, name="activate"),
   path('activate_account/', views.activate_account, name="activate-account"),
   path('activation-code', views.activate_code, name="activate-code")

]



