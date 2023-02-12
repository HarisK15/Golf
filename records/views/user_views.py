from django.shortcuts import render, redirect
from records.forms.user_forms import *
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from records.models.user_models import User, UserType
from django.views.decorators.http import require_POST, require_GET
from records.decorators import *
from django.http import HttpResponse

"""
Generic (no specifc type) - Login required
The view below can only be accessed by authenticated users, although the type of user is not checked.
Docs on login_required: https://docs.djangoproject.com/en/4.1/topics/auth/default/#the-login-required-decorator
"""

@login_required
def log_out(request):
    """
    Logs out the specified user
    """
    logout(request)
    return redirect('log_in')

@login_required
@require_GET
def dashboard(request):
    """
    Depending on type, points user to specific dashbaord relavent to their functionality.
    Cannot navigate to a dashboard if the user isn't logged in
    """

    # Getting current user: https://docs.djangoproject.com/en/4.1/topics/auth/default/#authentication-in-web-requests
    # Guarentted to not be annonymous as view is protected by @login_required
    user = request.user

    if (user.type == UserType.CLIENT):
        return render(request, 'templates/client/client_dashboard.html')

"""
Guest required
The views below cannot be accessed by authenticated users.
Docs on user_passes_test: https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.decorators.user_passes_test
"""

@guest_user_required
def log_in(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                # User successfully authenticated
                login(request, user)
                return redirect('dashboard')
            else:
                messages.add_message(request, messages.ERROR, 
                    "Email and password combination do not match a valid user. Please try again.")

    form = LoginUserForm()
    return render(request, 'templates/log_in.html', {'form': form})

"""
Other
"""

@transaction.non_atomic_requests
@guest_user_required
def register(request):
    """
    Prompt user to register themselves as a client.
    """

    # Docs: https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#django.contrib.auth.models.User.is_anonymous
    if (request.user.is_anonymous):
        if (request.method == 'POST'):
            form = RegisterClientForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('dashboard')
        else:
            form = RegisterClientForm()
        return render(request, 'templates/client/register_client.html', {'form': form})
    