from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class UserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, employee_code, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not employee_code:
            raise ValueError('The given employee code must be set')
        email = self.normalize_email(email)
        user = self.model(employee_code=employee_code, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, employee_code, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(employee_code, email, password, **extra_fields)

    def create_superuser(self, employee_code, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(employee_code, email, password, **extra_fields)
