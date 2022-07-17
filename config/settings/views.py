from django.http import JsonResponse

from api.models import get_403_message, get_404_message, get_500_message


def page_not_found_view(request, exception):
    return JsonResponse({"error": get_404_message()}, status=404)


def handler500(request):
    return JsonResponse({"error": get_500_message()}, status=500)


def handler403(request, exception):
    return JsonResponse({"error": get_403_message()}, status=403)
