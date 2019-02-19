from django.shortcuts import render


# トップページ
def index(request):
    context = {
      'users': request.user,
    }
    return render(request, 'index.html', context)
