from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        label="Roles",
        queryset=Group.objects.all().order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            "username", "email",
            "nombres", "apellido_paterno", "apellido_materno",
            "ci", "celular", "is_active", "is_staff",
            "groups",
        ]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class UserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        label="Roles",
        queryset=Group.objects.all().order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            "username", "email",
            "nombres", "apellido_paterno", "apellido_materno",
            "ci", "celular", "is_active", "is_staff",
            "groups",
        ]
