from records.forms.user_forms import *
from django.urls import reverse


class LoginHelper:
    """
    Assertion methods
    """

    def assert_redirected_to_login(self, response):
        """
        Asserts that a user has been redirected to the login form
        """
        # Check for redirect
        response_url = f"{ reverse('log_in') }?next={ self.url }"
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

        # Check template used
        self.assertTemplateUsed(response, 'templates/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginUserForm))

        # Shouldn't be bound as new instance
        self.assertFalse(form.is_bound)

    def assert_redirected_to_dashboard(self, response, dashboard_type):
        """
        Asserts that a user has been redirected back to their dashboard
        """
        # Check for redirect
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

        # Check template used
        if (dashboard_type == UserType.CLIENT):
            self.assertTemplateUsed(response, 'templates/client/client_dashboard.html')
    """
    Helper methods
    """

    def _is_logged_in(self):
        """
        Checks whether current user is logged in
        This log-in test was based off the same technique shown in the intructional videos on KEATs
        """
        return '_auth_user_id' in self.client.session.keys()

    def _create_client_user(self):
        """
        Will create active client user with following credentials:
        Email: client@example.com
        Password: Password123
        """

        self.client_user = User.objects.create_user(
            'client@example.com',
            first_name='Jane',
            last_name='Doe',
            email='client@example.com',
            password='Password123',
            type=UserType.CLIENT,
            is_active=True)

        # Add empty client profile
        client_profile = ClientProfile()
        client_profile.user = self.client_user
        client_profile.save()

    def _create_secondary_client_user(self):
        """
        Creates another client user
        """

        # Create secondary user
        self.client_user_2 = User.objects.create_user(
            'client_2@example.com',
            first_name='John',
            last_name='Doe',
            email='client_2@example.com',
            password='Password123',
            type=UserType.CLIENT,
            is_active=True)

        # Add empty client profile
        client_profile = ClientProfile()
        client_profile.user = self.client_user_2
        client_profile.save()

    
    def _log_in_as_client(self):
        """
        Logs in the client as a client.
        Assumes that the default client user is present within database.
        """
        if (self._is_logged_in()):
            self.client.logout()
        self.client.login(username='client@example.com', password='Password123')

    