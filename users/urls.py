from django.urls import path
from users.views import login_page
app_name = 'users'

urlpatterns = [
    path('login-page/', login_page, name='login_page')
]