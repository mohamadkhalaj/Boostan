from django.http import JsonResponse
from django.shortcuts import redirect, render

from api.models import (
    get_403_message, 
    get_404_message, 
    get_500_message, 
    get_csrf_failure_message,
    get_sessions_current_device_text,
    get_sessions_device_text,
    get_sessions_last_used_text,
    get_sessions_browser_text,
    get_sessions_os_text,
    get_sessions_ip_text,
    get_forget_code_text_message,
    get_success_food_list_text_message,
    get_food_list_text_message,
    get_reserve_food_text_message,
    get_login_text_message,
    get_dinner_text,
    get_lunch_text,
    get_breakfast_text,
    get_meal_submit_text,
    get_insufficient_balance_text,
    get_logout_text,
    get_not_reserved_text,
    get_already_reserved_text,
    get_reserve_text,
    get_cancel_text,
    get_telegram_main_btn_order_text,
    get_telegram_main_btn_sending_data_loading_text,
    get_sending_data_loading_text,
    get_order_button_text,
)

'''
    send template tags to food page
'''
def food(request):
    context = {
        'tags': {
            'sessions_current_device': get_sessions_current_device_text(),
            'sessions_device': get_sessions_device_text(),
            'sessions_last_used': get_sessions_last_used_text(),
            'sessions_browser': get_sessions_browser_text(),
            'sessions_os': get_sessions_os_text(),
            'sessions_ip': get_sessions_ip_text(),
            'forget_code': get_forget_code_text_message(),
            'success_food_list': get_success_food_list_text_message(),
            'food_list': get_food_list_text_message(),
            'reserve_food': get_reserve_food_text_message(),
            'login': get_login_text_message(),
            'dinner': get_dinner_text(),
            'lunch': get_lunch_text(),
            'breakfast': get_breakfast_text(),
            'meal_submit': get_meal_submit_text(),
            'insufficient_balance': get_insufficient_balance_text(),
            'logout': get_logout_text(),
            'not_reserved': get_not_reserved_text(),
            'already_reserved': get_already_reserved_text(),
            'reserve': get_reserve_text(),
            'cancel': get_cancel_text(),
            'telegram_main_btn_order': get_telegram_main_btn_order_text(),
            'telegram_main_btn_sending_data_loading': get_telegram_main_btn_sending_data_loading_text(),
            'sending_data_loading': get_sending_data_loading_text(),
            'order_button': get_order_button_text(),
        }
    }
    return render(request, 'pages/food.html', context=context)

def home(request):
    return redirect('food')

def page_not_found_view(request, exception):
    return JsonResponse({"error": get_404_message()}, status=404)


def handler500(request):
    return JsonResponse({"error": get_500_message()}, status=500)


def handler403(request, exception):
    return JsonResponse({"error": get_403_message()}, status=403)


def csrf_failure(request, reason=""):
    return JsonResponse({"error": get_csrf_failure_message()}, status=403)