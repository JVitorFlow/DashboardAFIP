from django import forms


class LoginForm(forms.Form):
    """
    Login form.
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nome de usuário",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Senha",
                "class": "form-control"
            }
        ))
