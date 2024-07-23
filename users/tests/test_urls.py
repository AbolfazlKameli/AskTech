from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views


class TestUrls(TestCase):
    def setUp(self):
        # Tokens
        self.token_obtain_pair_url = reverse('users:token_obtain_pair')
        self.token_refresh_url = reverse('users:token_refresh')
        self.token_block_url = reverse('users:token_block')
        # Password
        self.password_change_url = reverse('users:change_password')
        self.password_reset_url = reverse('users:reset_password')
        self.set_password_url = reverse('users:set_password', args=('this is a test token',))
        # Registration
        self.user_register_url = reverse('users:user_register')
        self.register_verify_url = reverse('users:user_register_verify', args=('this is a test token',))
        self.resend_verification_url = reverse('users:user_register_resend_email')
        # Users Info
        self.user_profile_url = reverse('users:user_profile', args=(21,))
        self.user_list_url = reverse('users:users_list')

    # Tokens
    def test_token_obtain_pair_url(self):
        self.assertEqual(resolve(self.token_obtain_pair_url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        self.assertEqual(resolve(self.token_refresh_url).func.view_class, TokenRefreshView)

    def test_token_block_url(self):
        self.assertEqual(resolve(self.token_block_url).func.view_class, views.BlockTokenAPI)

    # Password
    def test_change_password_url(self):
        self.assertEqual(resolve(self.password_change_url).func.view_class, views.ChangePasswordAPI)

    def test_reset_password_url(self):
        self.assertEqual(resolve(self.password_reset_url).func.view_class, views.ResetPasswordAPI)

    def test_set_password_url(self):
        self.assertEqual(resolve(self.set_password_url).func.view_class, views.SetPasswordAPI)

    # Registration
    def test_user_register_url(self):
        self.assertEqual(resolve(self.user_register_url).func.view_class, views.UserRegisterAPI)

    def test_register_verify_url(self):
        self.assertEqual(resolve(self.register_verify_url).func.view_class, views.UserRegisterVerifyAPI)

    def test_resend_verification_email_url(self):
        self.assertEqual(resolve(self.resend_verification_url).func.view_class, views.ResendVerificationEmailAPI)

    # User Info
    def test_user_profile_url(self):
        self.assertEqual(resolve(self.user_profile_url).func.view_class, views.UserProfileAPI)

    def test_user_list_url(self):
        self.assertEqual(resolve(self.user_list_url).func.view_class, views.UsersListAPI)
