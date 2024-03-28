from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import User, Token
from django.contrib.auth.hashers import make_password, verify_password
import secrets
import string

@csrf_exempt
def authentificate(request):
    data = JSONParser().parse(request)
    user = User.objects.filter(username = data["username"])
    res = {
        "success": False,
    }
    if (not user.exists()): return JsonResponse(res, safe=False)
    user = user[0   ]
    if (verify_password(data["password"], user.password)[0]):
        token = Token.objects.create(
            userId = user.id,
            token = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(15))
        )        
        token.save()
        res = {
            "logged": True,
            "isAdmin": user.isAdmin,
            "token": token.token
        }
    return JsonResponse(res, safe=False)

def authorization(request, token):
    user = Token.objects.filter(token=token)
    res = {
        "isAdmin": False,
        "logged": user.exists()
    }
    if (res["logged"]):
        res["isAdmin"] = User.objects.get(id = Token.objects.filter(token=token)[0].userId).isAdmin
    return JsonResponse(res, safe=False)

@csrf_exempt
def register(request):
    data = JSONParser().parse(request)
    user = User.objects.create(
        username = data["username"],
        password = make_password(data["password"])
    )
    user.save()
    return JsonResponse({}, safe=False)
