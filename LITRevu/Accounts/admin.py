"""
Ce fichier permet d'enregistrer les modèles 'Member' et 'Subscription' dans
l'interface d'administration de Django afin de permettre aux administrateurs
de gérer ces objets via l'interface web.
"""


from django.contrib import admin

from .models import Member, Subscription


class MemberAdmin(admin.ModelAdmin):
    # Affiche ces champs dans la liste des membres
    list_display = ('username', 'email', 'date_joined')
    # Permet de rechercher par ces champs
    search_fields = ('username', 'email')


admin.site.register(Member, MemberAdmin)
admin.site.register(Subscription)
