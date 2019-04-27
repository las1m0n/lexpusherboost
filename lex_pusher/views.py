from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse


def base_view(request):
    return render(request, 'lex_pusher/index.html', {})
