from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),

    path("buy/", views.buy, name='buy'),
    path("buy_tier/", views.buy_tier, name='buy_tier'),
    path("reroll/", views.reroll, name='reroll'),
    # Info
    path("player/", views.player, name='player'),
    path("creature/", views.creature, name='creature'),
    path("gamedata/", views.gamedata, name='gamedata'),
    path("enemy/", views.enemy, name='enemy'),
    path("opponent/<int:tier>", views.opponent, name='opponent'),
    path("item/", views.item, name='item'),
    path("item/extend", views.extended_items, name='extended_items'),
]
