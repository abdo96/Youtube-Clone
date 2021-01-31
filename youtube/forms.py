from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,label='username',required=True)
    password = forms.CharField(max_length=50,label='password',required=True)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30,label='username',required=True)
    password = forms.CharField(max_length=50,label='password',required=True)
    email = forms.EmailField(label='email')

def file_upload(instance,file_name):
         name,extension=file_name.split('.')
         return "youtube/{}".format(file_name)
class NewVideoForm(forms.Form):
    title  = forms. CharField(max_length=50,label='title')    
    description = forms.CharField(max_length=50,label='description')
    upload_file = forms.FileField(label='file')

class CommentForm(forms.Form):
     text = forms.CharField(max_length=300,label='text')   
     # hidden the input field I think the security issue  
     user = forms.IntegerField(widget=forms.HiddenInput(),initial=1)
