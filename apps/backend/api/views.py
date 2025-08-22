from django.http import JsonResponse # type: ignore

# Create your views here.

def health_check(request):
    return JsonResponse({"status": "ok","service":"django"})
