from django.contrib import admin
from .models import Citoyen, Agent, CodePostale, Reclamation

admin.site.register(Citoyen)
admin.site.register(Agent)
admin.site.register(CodePostale)
admin.site.register(Reclamation)


