from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("draft/", views.draft, name='draft'),

    path("buy/<int:id>", views.buy, name='buy'),
    # Info
    path("player/", views.player, name='player'),
    path("creature/", views.creature, name='creature'),
    path("gamedata/", views.gamedata, name='gamedata'),
    path("enemy/", views.enemy, name='enemy'),
    path("item/", views.item, name='item'),
]
