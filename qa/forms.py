from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Question, Answer

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autocomplete': 'off'  # Prevent browser from auto-filling
        }),
        help_text='Required. Please enter a valid email address.'
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'autocomplete': 'off'  # Prevent browser from auto-filling
        }),
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[
            RegexValidator(
                regex='^[\w.@+-]+$',
                message='Username can only contain letters, numbers, and @/./+/-/_ characters.'
            )
        ]
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your password',
            'id': 'password1',
            'onkeyup': 'checkPasswordStrength()',
            'autocomplete': 'new-password'  # Prevent browser from suggesting saved passwords
        }),
        help_text='''
        <ul class="password-requirements">
            <li id="length">At least 8 characters</li>
            <li id="letter">At least one letter</li>
            <li id="capital">At least one capital letter</li>
            <li id="number">At least one number</li>
            <li id="special">At least one special character</li>
        </ul>
        '''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm your password',
            'id': 'password2',
            'onkeyup': 'checkPasswordMatch()',
            'autocomplete': 'new-password'  # Prevent browser from suggesting saved passwords
        }),
        help_text='Enter the same password as before, for verification.'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different username.')
        return username
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')
        
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password1', e)
            
        # Check if password is too similar to username
        if username and password and username.lower() in password.lower():
            raise forms.ValidationError('Your password cannot be too similar to your username. Please choose a different password.')
            
        return password
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields didn\'t match.')
        return password2

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        } 