from django.contrib import admin

from core.models import Commande, LigneCommande

admin.site.register(Commande)
admin.site.register(LigneCommande)