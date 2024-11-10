# Définition des URLs pour l'application Accounts :
# 1. Gestion de la connexion, déconnexion et inscription des membres.
# 2. Gestion des abonnements et des suivis entre membres.

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .config import MemberCreationForm
from django.views.generic import CreateView

from .views import SubscriptionView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', CreateView.as_view(template_name='signup.html',
                                       form_class=MemberCreationForm,
                                       success_url='/login/'), name='signup'),

    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('follow/<int:member_id>/', SubscriptionView.as_view(),
         name='follow-member'
         ),
]
