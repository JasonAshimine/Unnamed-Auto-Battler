from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string

from api.views import get_full_user_data

#from main.models import User

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, "main/index.html", get_full_user_data(request))

    return render(request, "main/index.html")


def component(request):
    return HttpResponse(render_to_string('main/data.html', get_full_user_data(request)), content_type="text/plain")