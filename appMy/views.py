from django.shortcuts import render,redirect
from appUser.models import *
from appMy.models import *
from django.core.mail import send_mail #mail gönderebilmemzi için gerekli 
from netflix5haziran.settings import EMAIL_HOST_USER
from django.contrib import messages


def indexPage(request):
   context = {}
   return render(request, 'index.html', context)

def browsePage(request, pid=None, fslug = None):
   
   if fslug:
      contents_list = Contents.objects.filter(category__slug = fslug).order_by("-id")
   else:
      contents_list=Contents.objects.all().order_by("-id")
      
      
      
   if pid:
      profile = Profile.objects.get(id=pid)
   else:
      profile = Profile.objects.get(user=request.user, islogin=True)
      
   
   category_list = Category.objects.all()
   context = {
      "profile":profile,
      "contents_list":contents_list,
      "category_list":category_list,
      "fslug":fslug,
   }
   return render(request, 'browse-index.html', context)


def emailSendPage(request):
   
   if request.method == "POST":
      title = request.POST.get("title")
      text = request.POST.get("text")
     
      send_mail(
            title,
            text,
            EMAIL_HOST_USER,
            ["serdarkose9@hotmail.com"],
            fail_silently= False, 
         )

      messages.error(request,"Email Gönderilemedi")
      
      return redirect("emailSendPage")
   context ={}
   return render(request, "email-send.html", context)