"""
Ce fichier définit la configuration de l'application 'Accounts' dans Django.
Il permet à Django de reconnaître cette application et de l'intégrer
correctement dans le projet.
"""


from django.apps import AppConfig


# Configure l'application 'Accounts' dans le projet Django.
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Accounts'
