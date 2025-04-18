from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label= 'Username',
        required=True, 
        help_text='Do not use characters: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username:'})
    )
    email = forms.EmailField(
        label= 'Email',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email:'})
    )
    # some = forms.ModelChoiceField(queryset=User.objects.all())
    password1 = forms.CharField(label= 'Password',
    required=True, 
    help_text='Password should not be too short or simple',
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password:'})
    )
    password2 = forms.CharField(
        label= 'Confirm password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter password:'})
    )



    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': f'Enter your {field.label.lower()}'
            })


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label= 'Username',
        required=True, 
        help_text='Do not use characters: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username:'})
    )
    email = forms.EmailField(
        label = 'Email',
        required = True,
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email:'})
    )
    

    class Meta:
        model = User
        fields = ['email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} form-control bg-dark text-light border-secondary'
            field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'

    def save(self, commit = True):
        user = super().save(commit = False)
        
        profile, created = Profile.objects.get_or_create(user=user)

        if commit:
            user.save()
            profile.save()

        return user


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs.update({
                'class': f'{existing_class} form-control bg-dark text-light border-secondary',
                'placeholder': f'Enter your {field.label.lower()}'
            })


class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label= 'Upload photo',
        required=False,
        widget=forms.FileInput
    )
    gender = forms.ChoiceField(
        label='Select gender',
        choices = Profile.CHOICES,
        required = True,
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    receive_newsletter = forms.BooleanField(
        label = 'Subscribe to newsletter',
        required = False,
        widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Profile
        fields = ['img', 'gender', 'receive_newsletter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs['class'] = 'form-control bg-dark text-light border-secondary'
            else:
                existing = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing} form-control bg-dark text-light border-secondary'
                field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'




