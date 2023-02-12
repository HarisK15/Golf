from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from msms.settings import DASHBOARD_URL
from records.models.user_models import User, UserType

def client_user_required(view_func=None, redirect_field_name=None, login_url=DASHBOARD_URL):
    """
    Check that the user is of type CLIENT
    Assumes that @login_required has been used prior
    """
    def _is_client_user(user):
        return user.type == UserType.CLIENT

    custom_decorator = user_passes_test(_is_client_user, login_url=login_url, redirect_field_name=redirect_field_name)
    return custom_decorator(view_func) if view_func else custom_decorator

def guest_user_required(view_func=None, redirect_field_name=None, login_url=DASHBOARD_URL):
    """
    Check that the user is unauthenticated
    """
    def _is_guest_user(user):
        return user.is_authenticated == False

    custom_decorator = user_passes_test(_is_guest_user, login_url=login_url, redirect_field_name=redirect_field_name)
    return custom_decorator(view_func) if view_func else custom_decorator