from django.contrib import admin

from .models import RealizedTrade, Trade

admin.site.register(Trade)
admin.site.register(RealizedTrade)
