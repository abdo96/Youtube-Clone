from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm,SignUpForm,NewVideoForm,CommentForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from .models import Video,Comment
#from project import settings 
from django.conf import settings
import random,string
import os
# Create your views here.
from django.core.files import uploadhandler
class HomeView(View):
       def get(self,request):
           # minus before datetime to fetch the most recent videos firstly 
           if request.user.is_authenticated:
                  tabName = 'logout'
           else:
                  tabName = 'login'       
           most_recent_videos = Video.objects.order_by('-datetime')[:10] 
           return render(request,'home.html',{'tabName':tabName,'most_recent_videos':most_recent_videos})

       def post(self,request):
            return HttpResponse('The method is used is Get Request')   




class VideoView(View):
       def get(self,request,id):
           video_by_id =Video.objects.get(id=id)
           print(video_by_id.path)
           #new_path = str(settings.BASE_DIR)+'/'+initial_path
           #os.rename(initial_path, new_path)
                  
           context = {'video':video_by_id}
           if request.user.is_authenticated:
                  comment_form = CommentForm()
                  context['form'] = comment_form
                  tabName = 'logout'
                 
           else:
                  tabName = 'login'  
           context['tabName'] = tabName 
           # make a filteration by video object is getting the 
           # the comments which is asscoiated to the video
           # it's the idea of the blog post
           comments =  Comment.objects.filter(video__id=id)
           context['comments'] = comments
           return render(request,'video.html',context)

       def post(self,request,id):
            return HttpResponse('The method is used is Get Request')   
class CommentView(View):
       
        def post(self,request):
        
            comment_form=CommentForm(request.POST)
              
            if(comment_form.is_valid()):
                   text=comment_form.cleaned_data['text']
                   video=Video.objects.get(id =request.POST['video'])
                   new_comment=Comment(text=text,user=request.user,video=video)
                   new_comment.save()
                   return HttpResponseRedirect('video/{}'.format(request.POST['video']))
            else:
                   comment_form = CommentForm()
                   return render(request,'register.html',{'title':title,'body_text':body_text,hint_text:'hint_text','form':signupform,'tabName':tabName,'btnName':btnName})            
class SignUpView(View):
        def get(self,request):
           signupform=SignUpForm()
           title = 'SignUp'
           body_text = ""
           if request.user.is_authenticated == False:
                      tabName = 'login'
           else:
                      tabName = 'logout'           
           btnName = 'SignUp'
           hint_text = 'fill required fields*'
           return render(request,'register.html',{'title':title,'body_text':body_text,hint_text:'hint_text','form':signupform,'tabName':tabName,'btnName':btnName})

        def post(self,request):
            signupform=SignUpForm(request.POST)

            if(signupform.is_valid()):
                   username=signupform.cleaned_data['username']
                   password=signupform.cleaned_data['password']
                   email=signupform.cleaned_data['email']
                   new_user=User(username=username,password=password,email=email)
                   new_user.set_password(raw_password=password)
                   new_user.save()
                   return HttpResponseRedirect('/')
            else:
                   signupform = SignUpForm()
                   title = 'SignUp'
                   body_text = " "
                   tabName = 'login'
                   btnName = 'SignUp'
                   hint_text = 'the data you entered please enter valid data'
                   return render(request,'register.html',{'title':title,'body_text':body_text,hint_text:'hint_text','form':signupform,'tabName':tabName,'btnName':btnName})              
class LoginView(View):
       def get(self,request):
           if(request.user.is_authenticated):
                  #btnName = 'Signout'
                  return HttpResponseRedirect('/')     
                    
           loginform=LoginForm()
           title = 'Log in to account'
           body_text = ''
           tabName = 'login'
           btnName = 'LogIn'
           hint_text = 'fill these fields*'
           return render(request,'login.html',{'title':title,'body_text':body_text,'hint_text':hint_text,'form':loginform,'tabName':tabName,'btnName':btnName})

       def post(self,request):
            loginform=LoginForm(request.POST)
            
            if(loginform.is_valid()):
                   username=loginform.cleaned_data['username']
                   password=loginform.cleaned_data['password']
                   loggedUser=authenticate(username=username, password=password)
                   if loggedUser is not None:
                       # User is authenticated
                       login(request, loggedUser)
                       tabName = 'logout'
                       most_recent_videos = Video.objects.order_by('-datetime')[:10] 
                       return render(request,'home.html',{'tabName':tabName,'most_recent_videos':most_recent_videos})
                        
                   else:
                        loginform = LoginForm()
                        text = '.'
                        title = 'Log in to account'
                        body_text = ''
                        tabName = 'login'
                        btnName = 'LogIn'
                        hint_text = 'there is not registered account'
                        return render(request,'login.html',{'title':title,'body_text':body_text,'hint_text':hint_text,'form':loginform,'tabName':tabName,'btnName':btnName})         
                   
            else:
                   loginform = LoginForm()
                   title = 'Log in to account'
                   body_text = ''
                   tabName = 'login'
                   btnName = 'LogIn'
                   hint_text = 'fill these fields*'
                   return render(request,'login.html',{'title':title,'body_text':body_text,'hint_text':hint_text,'form':loginform,'tabName':tabName,btnName:'btnName'})
                   
class LogoutView(View):
     def get(self,request):
             title = 'logout'
             logout(request)
             return HttpResponseRedirect('/')               
            

class NewVideo(View):
       def get(self,request):
           if request.user.is_authenticated==False:
                  return HttpResponse('You have to register or log in so you could upload new video !')    
           new_video = NewVideoForm()
           title = 'New_Video'
           body_text = ["This is the New Video.","This is the Request Function."] 
           tabName = 'logout'
           btnName = 'Upload'
           hint_text = 'please upload the video file*'
           return render(request,'new_video.html',{'title':title,'body_text':body_text,'hint_text':hint_text,'form':new_video,'tabName':tabName,'btnName':btnName})

       def post(self,request):
            new_video_form = NewVideoForm(request.POST,request.FILES)
            #print(new_video_form)
            #print(request.POST)
            #print(uploadhandler.TemporaryUploadedFile.temporary_file_path())
            #print(request.FILES)
            if new_video_form.is_valid():
                  title= new_video_form.cleaned_data['title']
                  description= new_video_form.cleaned_data['description']
                  upload_file= new_video_form.cleaned_data['upload_file']
                  random_char = ''.join(random.choices(string.ascii_uppercase+string.digits,k=10))
                  path = random_char+upload_file.name 
                  file_system_video=open(str(settings.MEDIA_ROOT)+'/'+'youtube'+'/'+path,'wb+')
                  file_system_video.write(request.FILES['upload_file'].read())
                  path=str(settings.MEDIA_URL)+'youtube'+'/'+path
                  print(settings.MEDIA_URL)
                  print(settings.MEDIA_ROOT)
                   # upload_file only will output Memory uploadedd file
                  # dir function to show the objects and functions inside the object
                  new_video=Video(title=title,description=description,user=request.user,path=path)
                  new_video.save()
                  return HttpResponseRedirect('/video/{}'.format(new_video.id))
            else:
                  return HttpResponse('Please Enter Valid Data') 
