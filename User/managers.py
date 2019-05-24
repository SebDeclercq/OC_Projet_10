from typing import Any
from django.contrib.auth.base_user import BaseUserManager
from django.utils.text import format_lazy

class UserManager(BaseUserManager):
    use_in_migration: bool = True

    def _create_user(
            self, email: str, password: str, **extra_fields: Any
    ) -> 'User':  # type: ignore  # noqa
        if not email or not password:
            raise ValueError(f'Email and Password are required for Users')
        email = self.normalize_email(email)
        user: 'User' = self.model(email=email, **extra_fields)  # type: ignore  # noqa
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str, **extra_fields: Any
    ) -> 'User':  # type: ignore # noqa
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields: Any
    ) -> 'User':  # type: ignore  # noqa
        for config_field in ('is_superuser', 'is_staff'):
            extra_fields.setdefault(config_field, True)
            if extra_fields.get(config_field) is not True:
                raise ValueError(format_lazy(
                    'Superuser must have {field}=True.', field=config_field
                ))
        return self._create_user(email, password, **extra_fields)
