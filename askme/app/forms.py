from django import forms
from app.models import Profile, Question, Answer, User

class LoginForm(forms.Form):
    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 3:
            raise forms.ValidationError("Password should be more than 3 symbols.")
        return data

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    avatar = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_repeat']:
            self.add_error(None, "Passwords are different.")

        if len(cleaned_data['password']) < 3:
            raise forms.ValidationError("Password should be more than 3 symbols.")

class SettingsForm(forms.ModelForm):
    avatar = forms.FileField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'avatar']

    def save(self, *args, **kwargs):
        user = super().save(*args, *kwargs)
        return user

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter no more than 3 tags. Tags are entered separated by commas."}))

    class Meta:
        model = Question
        fields = ["title", "text"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Your question"}),
            "text": forms.Textarea(attrs={"placeholder": "Description of your question"})
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["text"]

        widgets = {
            "text": forms.Textarea(attrs={"placeholder": "Enter your answer here..."})
        }
