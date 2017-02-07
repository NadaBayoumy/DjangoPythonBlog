#nada
from django import forms
from .models import Category
from .models import ForbiddenWords
from .models import Post
from django import forms
#end nada

#alem
from models import Post, Reply 
#end alem

#hossam
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#end hossam


#simona
from django.forms.widgets import Widget
from django.contrib.auth.forms import  UserCreationForm
#end simona




#nada
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=('categoryName',)
        
                
        
class ForbiddenWordsForm(forms.ModelForm):
    class Meta:
        model=ForbiddenWords
        fields=('forbiddenWord',)
        
        
        
      
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('postTitle','postPic','postContent','userID','postCategory')
        
#endnada    
        
        
#alem

class Post_Form(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('postTitle', 'postPic', 'postContent')#'userID', 'postCategory')

class Comment_Form(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('replyContent',)
        
#end alem







#hossam

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser')


class ChangePwForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), help_text="This is a disabled field.")
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


#end hossam
    
        
        
        
        
#simona
        
class RegistrationForm(UserCreationForm):
    class Meta:
        model =User
        
        fields=['username','email','password1', 'password2']

    def clean_email(self):
        clean_data = super(RegistrationForm, self).clean()
        email=clean_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError("this email is already in use")
        print("clean_email")
        return email
    def clean_username(self):
        
        clean_data = super(RegistrationForm, self).clean()
        name=clean_data.get('username')
        
        return name
    

#end simona

        
