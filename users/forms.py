from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm



class UserRegisterForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('coordinator', 'Field Coordinator '),
        ('field_agent', 'Field Agent '),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        role = self.cleaned_data['role']
        if role == 'coordinator':
            user.is_coordinator = True
        elif role == 'field_agent':
            user.is_field_agent = True
            
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Username or Email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500',
            'placeholder': 'Password'
        })

        self.fields['username'].label = 'Username or Email'
        self.fields['password'].label = 'Password'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full px-3 py-2 border rounded-lg'})
