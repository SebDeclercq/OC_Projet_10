from typing import Optional, Sequence, Type
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User


class AdminForm(forms.ModelForm):
    # NOTE: For a more dynamic form (w/ JS), refer to :
    # https://stackoverflow.com/a/15992088
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'),
                                widget=forms.PasswordInput)

    class Meta:
        model: Type[User] = User
        fields: Sequence[str] = ('email', 'password1', 'password2', 'name',
                                 'firstname', 'is_active', 'is_superuser',
                                 'is_staff', 'user_permissions',)

    def clean_password2(self) -> Optional[str]:
        password1: Optional[str] = self.cleaned_data.get('password1')
        password2: Optional[str] = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Password mismatch'))
        return password2

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class SignUpForm(AdminForm):
    class Meta:
        model: Type[User] = User
        fields: Sequence[str] = ('email', 'firstname',)
