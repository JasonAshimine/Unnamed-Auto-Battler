from django.contrib import admin

from api.models import CreatureItemCount, ItemType, Player, Creature, Item, GameData, CombatList


# --------------------------------------
# Creature

class ItemInline(admin.TabularInline):
    model = Creature.items.through
    fields = ['item', 'count']
    extra = 0

class CreatureAdmin(admin.ModelAdmin):
    list_display = ['player','name', 'max_health', 'attack', 'defense']
    #fields = ['name', ('max_health', 'attack', 'defense')]
    inlines = [ItemInline]


# --------------------------------------
# GameData

'''class DataItemInline(admin.TabularInline):
    model = GameData.store_list.through
    extra = 0'''


class GameDataAdmin(admin.ModelAdmin):
    list_display = ('player','round', 'tier')
    fields = [
        ('round','wins', 'loss'),
        ('gold', 'tier', 'tier_cost'),
        'store_list'
    ]
    #inlines = [DataItemInline]

# --------------------------------------
# Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'tier', 'value')
    fields = ['name', 'tier', 'value', 'type']
    list_filter = ['tier', 'type']

# --------------------------------------
# Player
class GameDataInline(admin.StackedInline):
    model = GameData
    fields = [
        ('round','wins', 'loss'),
        ('gold', 'tier', 'tier_cost'),
    ]
    show_change_link = True
    
class CreatureInline(admin.StackedInline):
    model = Creature
    fields = ['name', 'level', ('max_health', 'attack', 'defense')]
    show_change_link = True

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [GameDataInline, CreatureInline]


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemType)
admin.site.register(Player, PlayerAdmin)
admin.site.register(GameData, GameDataAdmin)
admin.site.register(Creature, CreatureAdmin)
admin.site.register(CombatList)