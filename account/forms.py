from django import forms
from account.models import Profile
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()

# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ("email", "first_name", "last_name", "pto_balance")
    
#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control form-control-user'
#             visible.field.widget.attrs['placeholder'] = visible.field.label
class SignUpForm(UserCreationForm):
    # https://stackoverflow.com/questions/48049498/django-usercreationform-custom-fields
    first_name = forms.CharField(
        max_length=12,
        min_length=4,
        required=True,
        help_text='Required: First Name',
        widget=forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder': 'First Name'
                }
            )
        )
    last_name = forms.CharField(
        max_length=12,
        min_length=4,
        required=True, 
        help_text='Required: Last Name',
        widget=forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder': 'Last Name'
                }
            )
        )
    
    email = forms.EmailField(
        max_length=50, 
        help_text='Required. Inform a valid email address.',
        widget=forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user', 
                    'placeholder': 'Email'
                }
            )
        )
    
    password1 = forms.CharField(
        label=_('Password'),
        widget=(forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password'})),
        help_text=password_validation.password_validators_help_text_html())
    
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Password Confirmation'}),
                                help_text=_('Just Enter the same password, for confirmation'))
    
    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'})
    )

    pto_balance = forms.FloatField(
        required=True, 
        help_text='Required: Current PTO Balance',
        widget=forms.TextInput(
                attrs={
                    'class': 'form-control form-control-user',
                    'placeholder': '0.0'
                }
            )
        )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("email", "first_name", "last_name", "pto_balance")
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            print(visible)
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            visible.field.widget.attrs['placeholder'] = visible.field.label