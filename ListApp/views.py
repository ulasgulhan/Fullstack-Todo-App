from django.shortcuts import render


def render_index_html(request):
    return render(request, "index.html")
