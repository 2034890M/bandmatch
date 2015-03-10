from django.contrib import admin

from bandmatch.models import Player, Message, Band, Advert

# Register your models here.


class PlayerAdmin(admin.ModelAdmin):

	list_display = ('user', 'contact_info', 'description')


class BandAdmin(admin.ModelAdmin):
	list_display = ('name', 'location', 'description')


admin.site.register(Player, PlayerAdmin)
admin.site.register(Band, BandAdmin)