from django.contrib import admin

from api.models import Player, Creature, Item, GameData, CombatList

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'type', 'value')
    list_filter = ['tier', 'type']


admin.site.register(Item, ItemAdmin)
admin.site.register(Player)
admin.site.register(Creature)
admin.site.register(CombatList)