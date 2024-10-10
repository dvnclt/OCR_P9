from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .config import MemberCreationForm
from django.views.generic import CreateView

from .views import home

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CreateView.as_view(template_name='signup.html',
                                       form_class=MemberCreationForm,
                                       success_url='/login/'), name='signup'),

    path('home/', home, name='home'),
]
