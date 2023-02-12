from django.test import TestCase
from django.core.exceptions import ValidationError
from records.models.user_models import User, ClientProfile, UserType
from records.forms.user_forms import *
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from decorators import LoginHelper

class RegisterViewTestCase(TestCase, LoginHelper):
    """
    Contains the test cases for the client registration view
    """

    def setUp(self):
        """
        Simulate the form input and get routed URL
        """
        # It is done this way so that if URL it altered in future, test doesn't break
        self.url = reverse('register')

        self.form_input = {
            'first_name': 'Jane',
            'last_name' : 'Doe',
            'email' : 'janedoe@example.com',
            'password' : 'Password123',
            'password_confirm' : 'Password123', }

    """
    Test cases
    """

    def test_register_url(self):
        self.assertEqual(self.url, '/register/')
    
    def test_get_register_for_guest(self):
        response = self.client.get(self.url)

        # Check for success HTTP response
        self.assertEqual(response.status_code, 200)

        # Check template used
        self.assertTemplateUsed(response, 'templates/client/register_client.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterClientForm))

        # Shouldn't be bound as new instance
        self.assertFalse(form.is_bound)


    def test_view_restricted_for_client(self):
        self._create_client_user()
        self._log_in_as_client()
        self.assertTrue(self._is_logged_in())

        response = self.client.get(self.url, follow=True)
        self.assert_redirected_to_dashboard(response=response, dashboard_type=UserType.CLIENT)

    """
    RegisterClientForm
    """

    def test_unsuccesful_client_registration(self):
        self.form_input['email'] = 'bademail'

        before_user_count = User.objects.count()
        before_profile_count = ClientProfile.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_user_count = User.objects.count()
        after_profile_count = ClientProfile.objects.count()

        # Check no inserts have taken place
        self.assertEqual(before_profile_count, after_profile_count)
        self.assertEqual(before_user_count, after_user_count)

        # Check page still valid
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'templates/client/register_client.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterClientForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_succesful_client_registration(self):
        before_user_count = User.objects.count()
        before_profile_count = ClientProfile.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_user_count = User.objects.count()
        after_profile_count = ClientProfile.objects.count()

        # Check both inserts have taken place
        self.assertEqual(before_profile_count, after_profile_count - 1)
        self.assertEqual(before_user_count, after_user_count - 1)
        
        # Check that response goes to next page
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

        user = User.objects.get(username = 'janedoe@example.com')

        # Check that response goes to correct dashboard
        self.assertTemplateUsed(response, 'templates/client/client_dashboard.html')
        
        # Check that the fields went through to database
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.com')
        self.assertEqual(user.type, UserType.CLIENT)
        self.assertEqual(user.is_active, True)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())

    