from django.test import TestCase
from django.core.exceptions import ValidationError
from records.models.user_models import User, ClientProfile, UserType
from records.forms.user_forms import *
from django import forms
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from ..helpers import LoginHelper
from django.contrib import messages

class LogOutViewTestCase(TestCase, LoginHelper):
    """
    Contains test cases for the log_out view
    """
    def setUp(self):
        self.url = reverse('log_out')

        # These users will be used to check for correct redirects
        self._create_client_user()

    """
    Test cases
    """

    def test_log_out_url(self):
        self.assertEqual(self.url, '/log-out/')

    def test_log_out_guest(self):
        response = self.client.get(self.url, follow=True)
        self.assert_redirected_to_login(response)

    def test_log_out_client(self):
        self._log_in_as_client()
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        self.assertFalse(self._is_logged_in())

        self.assertRedirects(response, reverse('log_in'), status_code=302, target_status_code=200)

        self.assertTemplateUsed(response, 'templates/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginUserForm))

    

    
    
    