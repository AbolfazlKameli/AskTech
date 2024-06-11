from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
