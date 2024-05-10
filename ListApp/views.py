from django.shortcuts import redirect, render


def render_index_html(request):
    return render(request, "index.html")
