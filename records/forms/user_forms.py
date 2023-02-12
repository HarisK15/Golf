from django import forms
from ..models import User, UserType, ClientProfile
from django.core.validators import RegexValidator

class LoginUserForm(forms.Form):
    """
    The form that is user to log a user in
    """
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterUserForm(forms.ModelForm):
    """
    The base form for registering users.
    Every form, regardless of account type, has these fields.
    """
    class Meta():
        """
        Select model fields that will be used within form.
        """
        model = User
        fields = [ 'first_name', 'last_name', 'email' ]

    # Additional fields outside of model
    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message="Password must contain upper, lower case letter and number"
        )])

    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

    def clean(self):
        """
        Used to check for validation errors that may occur ACROSS multiple fields
        """
        super().clean()

        # If the fields password and password_confirm don't match, an error is added.
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', 'Password confirmation not equal to password')

class RegisterClientForm(RegisterUserForm):
    """
    The registration form for when guests want to make new client accounts
    """
    def save(self):
        """
        Creates and saves a new client user with an associated empty client profile
        """
        super().save(commit=False)

        user = User.objects.create_user(
            self.cleaned_data.get('email'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            email = self.cleaned_data.get('email'),
            password = self.cleaned_data.get('password'),
            type = UserType.CLIENT,
            is_active=True)

        # Add empty client profile
        client_profile = ClientProfile()
        client_profile.user = user
        client_profile.save()
        
        return user
