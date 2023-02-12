from django.test import TestCase
from django.core.exceptions import ValidationError
from records.models.user_models import User, ClientProfile, UserType
from records.forms.user_forms import *
from django import forms
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from ..helpers import LoginHelper
from django.contrib import messages

class LoginViewTestCase(TestCase, LoginHelper):
    """
    Contains test cases for the log_in view
    """
    def setUp(self):
        self.url = reverse('log_in')

        # These users will be used to check for correct redirects
        self._create_client_user()

    """
    Test cases
    """

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log-in/')
    
    def test_get_log_in(self):
        response = self.client.get(self.url)

        # Check for success HTTP response
        self.assertEqual(response.status_code, 200)

        # Check template used
        self.assertTemplateUsed(response, 'templates/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginUserForm))
        
        # Check no error came up
        messagesList = list(response.context['messages'])
        self.assertEqual(len(messagesList), 0)

        # Shouldn't be bound as new instance
        self.assertFalse(form.is_bound)

    def test_unsuccesful_log_in(self):
        form_input = { 
            'email': 'client@example.com', 
            'password': 'WrongPassword123', }

        response = self.client.post(self.url, form_input)

        # Check for success HTTP response
        self.assertEqual(response.status_code, 200)

        # Should stay on same page
        self.assertTemplateUsed(response, 'templates/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginUserForm))

        # No log in should've occured
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

        # An error message should've flagged.
        messagesList = list(response.context['messages'])
        self.assertTrue(len(messagesList) >= 1)
        self.assertEqual(messagesList[0].level, messages.ERROR)

    def test_succesful_client_log_in(self):
        form_input = { 
            'email': 'client@example.com', 
            'password': 'Password123', }

        response = self.client.post(self.url, form_input, follow=True)

        # Client should login
        self.assertTrue(self._is_logged_in())

        # Should be redirected to dashboard
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'templates/client/client_dashboard.html')

        # No error messages should be present
        messagesList = list(response.context['messages'])
        self.assertEqual(len(messagesList), 0)

    
    def test_valid_login_by_inactive_client(self):
        # Inactive users should not be able to login, despite the credentials being correct
        self.client_user.is_active = False
        self.client_user.save()

        form_input = { 
            'email': 'client@example.com', 
            'password': 'Password123', }

        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'templates/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginUserForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messagesList = list(response.context['messages'])
        self.assertEqual(len(messagesList), 1)
        self.assertEqual(messagesList[0].level, messages.ERROR)

    