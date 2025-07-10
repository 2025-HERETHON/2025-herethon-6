from django.urls import path
from .views.login import login_view
from .views.signup import signup_view

app_name = "users"

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),

]