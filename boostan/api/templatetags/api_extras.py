from api.models import (
    get_menu_contribute_text,
    get_site_description_meta_tag,
    get_login_submit_text,
    get_login_password_text,
    get_site_title,
    get_login_username_text,
    get_login_page_title,
    get_order_button_text,
    get_menu_sessions_text,
    get_menu_forget_code_text,
    get_google_analysis_code,
    get_google_tag_manager_code,
    get_sentry_code,
    get_contribute_text,
)
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.simple_tag
def site_description():
    return get_site_description_meta_tag()

@register.simple_tag
def login_submit_text():
    return get_login_submit_text()

@register.simple_tag
def login_password_text():
    return get_login_password_text()

@register.simple_tag
def login_username_text():
    return get_login_username_text()

@register.simple_tag
def site_title():
    return get_site_title()

@register.simple_tag
def login_page_title():
    return get_login_page_title()

@register.simple_tag
def order_button_text():
    return get_order_button_text()

@register.simple_tag
def menu_sessions_text():
    return get_menu_sessions_text()

@register.simple_tag
def menu_forget_code_text():
    return get_menu_forget_code_text()

@register.simple_tag
def menu_contribute_text():
    return get_menu_contribute_text()

@register.simple_tag
def google_analysis_code():
    return get_google_analysis_code()

@register.simple_tag
def google_tag_manager_code():
    return get_google_tag_manager_code()

@register.simple_tag
def sentry_code():
    return get_sentry_code()

@register.simple_tag
def contribute_text():
    return mark_safe(get_contribute_text())