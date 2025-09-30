from django.contrib import admin
from .models import Petition, VoteBallot

# Register your models here.
admin.site.register(Petition)
admin.site.register(VoteBallot)
