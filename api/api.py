from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(["POST"])
def login(request):
    print('hoeluoechr')

    username = request.POST['username']
    password = requset.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        result = login(request, user)
        print(result)
        return JsonResponse({'data': result}, safe=False)
    else:
        return JsonResponse({'error': 'Username or password was incorrect'}, safe=False)

