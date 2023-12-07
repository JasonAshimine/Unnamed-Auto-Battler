from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("draft/", views.draft, name='draft')
]
