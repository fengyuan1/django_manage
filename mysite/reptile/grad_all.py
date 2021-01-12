from django.http import HttpResponse
from django.shortcuts import render

from polls import models

def grad_all_view(request):
    context={

    }

    return render(request, 'grad_all.html', context)