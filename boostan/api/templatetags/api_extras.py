from api.models import (
    get_site_description_meta_tag,
    get_login_submit_label,
    get_login_password_label,
    get_site_title,
    get_login_username_label,
    get_login_page_title,
    get_order_button_label,
    get_menu_sessions_label,
    get_menu_forget_code_label,
)

from django import template

register = template.Library()

@register.simple_tag
def site_description():
    return get_site_description_meta_tag()

@register.simple_tag
def login_submit_label():
    return get_login_submit_label()

@register.simple_tag
def login_password_label():
    return get_login_password_label()

@register.simple_tag
def login_username_label():
    return get_login_username_label()

@register.simple_tag
def site_title():
    return get_site_title()

@register.simple_tag
def login_page_title():
    return get_login_page_title()

@register.simple_tag
def order_button_label():
    return get_order_button_label()

@register.simple_tag
def menu_sessions_label():
    return get_menu_sessions_label()

@register.simple_tag
def menu_forget_code_label():
    return get_menu_forget_code_label()