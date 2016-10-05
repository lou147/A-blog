from django import forms
from .models import Post, Comment
from django.contrib.auth import authenticate, get_user_model
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = [
            'title',
            'image',
            'content',
            'draft',
        ]


class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('用户名或密码错误')
        return super(UserForm, self).clean()


User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='confirm password')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'email',
        ]

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        email_qs = User.objects.filter(email=email)
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError('用户名已存在')
        if email_qs.exists():
            raise forms.ValidationError('邮箱已被注册')
        if password != password2:
            raise forms.ValidationError('密码不一致')
        print(type(password))
        return super(UserRegisterForm, self).clean()


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea, label='')


