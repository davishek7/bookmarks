from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Profile


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'mb-2','placeholder':'Your Username or Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your Password'}))


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['username'].widget.attrs.update({
            'class':'mb-2','placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update(
            {'class':'mb-2','placeholder': 'Enter Email'})
        self.fields['first_name'].widget.attrs.update({
            'class':'mb-2','placeholder': 'Enter First name','required':'required'})
        self.fields['last_name'].widget.attrs.update({
            'class':'mb-2','placeholder': 'Enter Last name','required':'required'})
        self.fields['password1'].widget.attrs.update(
            {'class':'mb-2','placeholder': 'Enter Password'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Repeat Password'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An user with that email already exists, please use another one.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError('Username already exists!')
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password1']:
            raise forms.ValidationError('Passwords do not match!')
        return cd['password2']


class ProfileUpdateForm(forms.ModelForm):

    photo = forms.ImageField(widget=forms.FileInput(),required=False)

    date_of_birth = forms.DateField(
        widget=forms.NumberInput({'type':'date'})
    )

    class Meta:
        model = Profile
        fields = ['date_of_birth','photo']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class':'mb-2','readonly': 'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class':'mb-2','readonly': 'readonly'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'mb-2',}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'mb-2',}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

