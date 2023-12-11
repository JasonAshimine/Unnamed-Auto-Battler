from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("draft/", views.draft, name='draft'),
    path("player/", views.player, name='player'),
    path("creature/", views.creature, name='creature'),
    path("gamedata/", views.gamedata, name='gamedata'),
    path("item/", views.item, name='item'),
]
