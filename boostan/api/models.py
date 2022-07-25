from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.db.models import Max
from django.db.models import Min
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext as _
from utils.general_model import GeneralModel


'''
    Student Model with following fields:
        stu_number: Student number
        name: Student name
        password: Student password
        credit: Student credit
        count_of_used: Count of used
        top_credit: Top credit
        total_recieved_list: Total recieved list
        total_reserved_food: Total reserved food
        total_forget_code: Total forget code
        status: Student status
        last_used: Last used
        first_used: First used
    
    This model stores user data
'''
class Student(GeneralModel):
    '''
        Student status:
            0: Active
            1: Banned
            2: White listed
    '''
    STATUSES = (
        (0, _("Normal")),
        (1, _("Blocked user")),
        (2, _("Whitelist user")),
    )

    full_name = models.TextField(
        verbose_name=_("Full name"),
    )

    stu_number = models.TextField(
        verbose_name=_("Student number"),
    )

    password = models.TextField(
        verbose_name=_("Password"),
    )

    count_of_used = models.IntegerField(
        verbose_name=_("count of used"),
    )

    credit = models.FloatField(
        verbose_name=_("Credit"),
    )

    top_credit = models.FloatField(
        verbose_name=_("Top credit"),
        default=0.0,
    )

    status = models.IntegerField(
        choices=STATUSES, default=STATUSES[0][0], verbose_name=_("Status")
    )
    total_recieved_list = models.IntegerField(verbose_name=_("Tota received list"), default=0) # Total recieved list
    total_reserved_food = models.IntegerField(verbose_name=_("Total reserved food"), default=0) # Total reserved food
    total_forget_code = models.IntegerField(verbose_name=_("Total forget code"), default=0) # Total forget code

    def __str__(self):
        return f"{self.full_name} {self.stu_number}"

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def first_used_time(self):
        return naturaltime(super().first_used)

    first_used_time.short_description = _("First used time")

    def last_used_time(self):
        return naturaltime(super().last_used)

    last_used_time.short_description = _("Last used time")

'''
    Session Model with following fields:
        student: Student (ForeignKey)
        session: Session
        ip_address: IP address
        telegram_id: Telegram id
        telegram_username: Telegram username
        user_agent: User agent
        last_used: Last used
        first_used: First used
    
    This model stores user sessions
    each user could have several sessions and
    each session is permanent until user 
    logged out manually
'''
class Session(GeneralModel):
    '''
        Each session has a student
        and each student could have many sessions
    '''
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("Student"),
    )

    # Random generated string
    session = models.TextField(
        verbose_name=_("Session"),
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP address"),
        blank=True,
        null=True,
    )

    telegram_id = models.CharField(
        max_length=64, blank=True, null=True, verbose_name=_("Telegram ID")
    )
    telegram_username = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Telegram Username")
    )

    user_agent = models.CharField(verbose_name=_("User agent"), max_length=256, null=True)

    def first_used_time(self):
        return naturaltime(super().first_used)

    first_used_time.short_description = _("First used time")

    def last_used_time(self):
        return naturaltime(super().last_used)

    last_used_time.short_description = _("Last used time")

    def __str__(self):
        return f"{self.student.full_name} {self.session}"

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")

'''
    Visitor Model with following fields:
        ip_address: IP address
        user_agent: User agent
        path: Path (URL)
        is_admin_panel: Is admin panel (Check if the path is admin panel)
        data: Data (Get/Post)
        last_used: Last used
        first_used: First used
    
    This model logs any requests 
    if logging is enabled in settings
'''
class Visitor(GeneralModel):
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP address"),
    )

    user_agent = models.CharField(verbose_name=_("User agent"), max_length=256, null=True)
    path = models.CharField(verbose_name=_("Url path"), max_length=256, null=True)
    is_admin_panel = models.BooleanField(verbose_name=_("Is admin panel"), default=False)
    data = models.TextField(verbose_name=_("Data"), null=True, blank=True)

    def last_used_time(self):
        return naturaltime(super().last_used)

    last_used_time.short_description = _("Last used time")

    class Meta:
        verbose_name = _("visitor")
        verbose_name_plural = _("visitors")

    def __str__(self):
        return f"{self.ip_address}, {self.user_agent}"

'''
    Setting Model with following fields:
        name: Setting name
        value: Setting value
    
    This model have several records for for 
    adjusting site functionallity
    such:
        telegram API
        telegram admin id
        telegram chat id
        telegram special users
        rate limit interval
        visitor model toggle
        set site operating mode
        ...
'''
class Setting(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256)
    value = models.TextField(verbose_name=_("Value"))

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return f"{self.name}"

'''
    Message Model with following fields:
        name: Message name
        value: Message value
    
    This model stores any BackEnd alerts and errors
    and can be eddited easily via admin panel
'''
class Message(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256)
    value = models.TextField(verbose_name=_("Value"))

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return f"{self.name}"

'''
    TemplateTags Model with following fields:
        name: TemplateTags name
        value: TemplateTags value

    This model stores any FrontEnd user prompts and alerts
    and can be eddited easily via admin panel
'''
class TemplateTags(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256)
    value = models.TextField(verbose_name=_("Value"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return f"{self.name}"

'''
    Statistics Model with following fields:
        name: Statistics name
        value: Statistics value

    This model can save any user defined statistics 
    and show them in readonly fields via admin panel
'''
class Statistics(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256)
    value = models.BigIntegerField(verbose_name=_("Value"), default=0)

    class Meta:
        verbose_name = _("Statistics")
        verbose_name_plural = _("Statistics")

    def __str__(self):
        return f"{self.name}"

'''
    All api app queries starts from 
    here to end of this file
'''
def get_telegram_api():
    try:
        return Setting.objects.get(name="telegram_api").value
    except:
        return ""


def get_all_admin_chat_id():
    return Setting.objects.filter(name="telegram_chat_id").all()


def get_main_admin_chat_id():
    try:
        return Setting.objects.get(name="main_admin").value
    except:
        return ""


def get_deadline_message():
    try:
        return Message.objects.get(name="deadline_message").value
    except:
        return ""


def get_insufficient_balance_message():
    try:
        return Message.objects.get(name="insufficient_balance_message").value
    except:
        return ""


def get_invalid_credential_message():
    try:
        return Message.objects.get(name="invalid_credential_message").value
    except:
        return ""


def get_special_users():
    ar = []
    values = Setting.objects.filter(name="special_user").values_list("value")
    for item in values:
        ar.append(item[0])
    return ar


def get_missing_parameter_message():
    try:
        return Message.objects.get(name="missing_parameter_message").value
    except:
        return ""


def get_blocked_message():
    return Message.objects.filter(name="blocked_message").first().value


def get_whitelist_message():
    return Message.objects.filter(name="whitelist_message").first().value


def get_unknown_operation_message():
    return Message.objects.filter(name="unknown_operation_message").first().value


def create_student(**kwargs):
    student = Student(**kwargs)
    student.save()
    return student


def create_visitor(**kwargs):
    visitor = Visitor(**kwargs)
    visitor.save()
    return visitor


def mark_visitor_as_is_admin(visitor):
    visitor.is_admin_panel = True
    visitor.save()
    return visitor


def increment_count_of_used(student):
    student.count_of_used += 1
    student.save()
    return student


def get_student_by_stu_number(stu_number):
    return Student.objects.filter(stu_number=stu_number).first()


def check_student_exists(stu_number):
    return Student.objects.filter(stu_number=stu_number).exists()


def check_and_update_student_top_credit(student, credit):
    if student.top_credit < credit:
        student.top_credit = credit
        student.save()


def increment_total_recieved_list(student):
    student.total_recieved_list += 1
    student.save()
    return student


def increment_total_reserved_food(student):
    student.total_reserved_food += 1
    student.save()
    return student


def increment_total_forget_code(student):
    student.total_forget_code += 1
    student.save()
    return student


def check_and_update_password(student, password):
    if not student.password == password:
        student.password = password
        student.save()


def get_student_status(student):
    return student.status


def update_user_credit(user, credit):
    user.credit = credit
    user.save()
    return user


def check_operating_mode():
    value = Setting.objects.filter(name="operating_mode").first().value
    if not value:
        return "normal"
    return value


def get_beinol_bot_ip():
    try:
        return Setting.objects.filter(name="beinol_bot_ip").first().value
    except:
        return ""


def get_rate_limit():
    try:
        value = float(Setting.objects.filter(name="rate_limit").first().value)
        return value
    except:
        return ""


def get_connection_timeout():
    try:
        value = float(Setting.objects.filter(name="connection_timeout").first().value)
        return value
    except:
        return ""


def is_rate_limit_enabled():
    try:
        value = get_rate_limit()
        if float(value) > 0:
            return True
        else:
            return False
    except:
        return True


def get_wait_message():
    try:
        return Message.objects.filter(name="wait_message").first().value
    except:
        return ""


def get_succeess_login_message():
    try:
        return Message.objects.filter(name="success_login_message").first().value
    except:
        return ""


def get_missing_food_list_message():
    try:
        return Message.objects.filter(name="missing_food_list_message").first().value
    except:
        return ""


def get_success_reserve_message():
    try:
        return Message.objects.filter(name="success_reserve_message").first().value
    except:
        return ""


def get_food_reserve_unexpected_error_message():
    try:
        return Message.objects.filter(name="food_reserve_unexpected_error_message").first().value
    except:
        return ""


def check_visitor_log():
    try:
        return Setting.objects.filter(name="visitor_log_status").first().value
    except:
        return False


def statistics_total_students_count():
    stu_counts = Student.objects.count()
    try:
        statistics = Statistics.objects.get(name="total_students_count")
        statistics.value = stu_counts
        statistics.save()
    except:
        Statistics.objects.create(name="total_students_count", value=stu_counts)


def statistics_total_requests():
    try:
        statistics = Statistics.objects.get(name="total_requests")
        statistics.value += 1
        statistics.save()
    except:
        Statistics.objects.create(name="total_requests", value=1)


def statistics_total_reserves():
    try:
        statistics = Statistics.objects.get(name="total_reserves")
        statistics.value += 1
        statistics.save()
    except:
        Statistics.objects.create(name="total_reserves", value=1)


def statistics_total_list():
    try:
        statistics = Statistics.objects.get(name="total_list")
        statistics.value += 1
        statistics.save()
    except:
        Statistics.objects.create(name="total_list", value=1)


def statistics_total_forget_code():
    try:
        statistics = Statistics.objects.get(name="total_forget_code")
        statistics.value += 1
        statistics.save()
    except:
        Statistics.objects.create(name="total_forget_code", value=1)


def statistics_first_user_used():
    first_time = int(
        Student.objects.aggregate(Min("first_used"))["first_used__min"].strftime("%Y%m%d%H%M%S")
    )
    try:
        statistics = Statistics.objects.get(name="first_user_used")
        statistics.value = first_time
        statistics.save()
    except:
        Statistics.objects.create(name="first_user_used", value=first_time)


def statistics_last_user_used():
    last_time = int(
        Student.objects.aggregate(Max("last_used"))["last_used__max"].strftime("%Y%m%d%H%M%S")
    )
    try:
        statistics = Statistics.objects.get(name="last_user_used")
        statistics.value = last_time
        statistics.save()
    except:
        Statistics.objects.create(name="last_user_used", value=last_time)


def statistics_total_login():
    sum_count = Student.objects.aggregate(Sum("count_of_used"))["count_of_used__sum"]
    try:
        statistics = Statistics.objects.get(name="total_login")
        statistics.value = sum_count
        statistics.save()
    except:
        Statistics.objects.create(name="total_login", value=sum_count)


def get_no_reserved_food_message():
    try:
        return Message.objects.filter(name="no_reserved_food_message").first().value
    except:
        return ""


def get_forget_code_deadline_message():
    try:
        return Message.objects.filter(name="forget_code_deadline_message").first().value
    except:
        return ""


def get_student_by_session(session):
    try:
        stu_session = Session.objects.get(session=session)
        stu_session.last_used = timezone.now()
        stu_session.save()
        return stu_session.student
    except:
        return None


def get_not_logged_in_yet_message():
    try:
        return Message.objects.filter(name="not_logged_in_yet_message").first().value
    except:
        return ""


def update_user_ip_address_user_agent(session, ip_address, user_agent):
    try:
        session_obj = Session.objects.get(session=session)
        session_obj.ip_address = ip_address
        session_obj.user_agent = user_agent
        session_obj.save()
        return session_obj.student
    except:
        return None


def create_session_object_for_student(**kwargs):
    session = Session.objects.create(**kwargs)
    return session


def delete_session_object_for_student(session):
    try:
        session_obj = Session.objects.get(session=session)
        session_obj.delete()
        return True
    except:
        return None


def get_session_not_found_message():
    try:
        return Message.objects.filter(name="session_not_found_message").first().value
    except:
        return ""


def get_success_logout_message():
    try:
        return Message.objects.filter(name="success_logout_message").first().value
    except:
        return ""


def get_session_not_passed_message():
    try:
        return Message.objects.filter(name="session_not_passed_message").first().value
    except:
        return ""


def get_all_user_sessions_by_sesion(session):
    try:
        student = get_student_by_session(session)
        return student.sessions.all().order_by("-last_used")
    except:
        return None


def get_404_message():
    try:
        return Message.objects.filter(name="404_message").first().value
    except:
        return ""


def get_500_message():
    try:
        return Message.objects.filter(name="500_message").first().value
    except:
        return ""


def get_403_message():
    try:
        return Message.objects.filter(name="403_message").first().value
    except:
        return ""

def get_csrf_failure_message():
    try:
        return Message.objects.filter(name="csrf_failure_message").first().value
    except:
        return ""

def get_site_description_meta_tag():
    try:
        return TemplateTags.objects.filter(name="site_description_meta_tag").first().value
    except:
        return ""

def get_site_title():
    try:
        return TemplateTags.objects.filter(name="site_title").first().value
    except:
        return ""

def get_login_page_title():
    try:
        return TemplateTags.objects.filter(name="login_page_title").first().value
    except:
        return ""

def get_login_username_text():
    try:
        return TemplateTags.objects.filter(name="login_username_text").first().value
    except:
        return ""

def get_login_password_text():
    try:
        return TemplateTags.objects.filter(name="login_password_text").first().value
    except:
        return ""

def get_login_submit_text():
    try:
        return TemplateTags.objects.filter(name="login_submit_text").first().value
    except:
        return ""

def get_order_button_text():
    try:
        return TemplateTags.objects.filter(name="order_button_text").first().value
    except:
        return ""

def get_menu_sessions_text():
    try:
        return TemplateTags.objects.filter(name="menu_sessions_text").first().value
    except:
        return ""

def get_menu_forget_code_text():
    try:
        return TemplateTags.objects.filter(name="menu_forget_code_text").first().value
    except:
        return ""

def get_sessions_current_device_text():
    try:
        return TemplateTags.objects.filter(name="sessions_current_device_text").first().value
    except:
        return ""

def get_sessions_device_text():
    try:
        return TemplateTags.objects.filter(name="sessions_device_text").first().value
    except:
        return ""

def get_sessions_last_used_text():
    try:
        return TemplateTags.objects.filter(name="sessions_last_used_text").first().value
    except:
        return ""

def get_sessions_browser_text():
    try:
        return TemplateTags.objects.filter(name="sessions_browser_text").first().value
    except:
        return ""

def get_sessions_os_text():
    try:
        return TemplateTags.objects.filter(name="sessions_os_text").first().value
    except:
        return ""

def get_sessions_ip_text():
    try:
        return TemplateTags.objects.filter(name="sessions_ip_text").first().value
    except:
        return ""

def get_forget_code_text_message():
    try:
        return TemplateTags.objects.filter(name="forget_code_text_message").first().value
    except:
        return ""

def get_success_food_list_text_message():
    try:
        return TemplateTags.objects.filter(name="success_food_list_text_message").first().value
    except:
        return ""

def get_food_list_text_message():
    try:
        return TemplateTags.objects.filter(name="food_list_text_message").first().value
    except:
        return ""

def get_reserve_food_text_message():
    try:
        return TemplateTags.objects.filter(name="reserve_food_text_message").first().value
    except:
        return ""

def get_login_text_message():
    try:
        return TemplateTags.objects.filter(name="login_text_message").first().value
    except:
        return ""

def get_dinner_text():
    try:
        return TemplateTags.objects.filter(name="dinner_text").first().value
    except:
        return ""

def get_lunch_text():
    try:
        return TemplateTags.objects.filter(name="lunch_text").first().value
    except:
        return ""

def get_breakfast_text():
    try:
        return TemplateTags.objects.filter(name="breakfast_text").first().value
    except:
        return ""

def get_meal_submit_text():
    try:
        return TemplateTags.objects.filter(name="meal_submit_text").first().value
    except:
        return ""

def get_insufficient_balance_text():
    try:
        return TemplateTags.objects.filter(name="insufficient_balance_text").first().value
    except:
        return ""

def get_logout_text():
    try:
        return TemplateTags.objects.filter(name="logout_text").first().value
    except:
        return ""

def get_not_reserved_text():
    try:
        return TemplateTags.objects.filter(name="not_reserved_text").first().value
    except:
        return ""

def get_already_reserved_text():
    try:
        return TemplateTags.objects.filter(name="already_reserved_text").first().value
    except:
        return ""

def get_reserve_text():
    try:
        return TemplateTags.objects.filter(name="reserve_text").first().value
    except:
        return ""

def get_cancel_text():
    try:
        return TemplateTags.objects.filter(name="cancel_text").first().value
    except:
        return ""

def get_menu_contribute_text():
    try:
        return TemplateTags.objects.filter(name="menu_contribute_text").first().value
    except:
        return ""

def get_google_analysis_code():
    try:
        return TemplateTags.objects.filter(name="google_analysis_code").first().value
    except:
        return ""

def get_google_tag_manager_code():
    try:
        return TemplateTags.objects.filter(name="google_tag_manager_code").first().value
    except:
        return ""

def get_sentry_code():
    try:
        return TemplateTags.objects.filter(name="sentry_code").first().value
    except:
        return ""

def get_contribute_text():
    try:
        return TemplateTags.objects.filter(name="contribute_text").first().value
    except:
        return ""