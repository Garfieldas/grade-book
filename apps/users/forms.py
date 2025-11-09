from django import forms

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            "class": "input input-bordered w-full py-3 text-base",
            "placeholder": "enter your email example@.com..."
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full py-3 text-base",
            "placeholder": "enter your password...",
        }
        )
    )