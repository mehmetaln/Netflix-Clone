from django.core.mail import send_mail #mail gönderebilmemzi için gerekli  
from netflix5haziran.settings import EMAIL_HOST_USER 
from django.shortcuts import render, redirect
from appUser.models import *
from appMy.models import *
from django.contrib import messages
from django.contrib.auth.models import User


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
   
   # users = User.objects.all().values_list("email") # user içerisindeki emailleri döndermemize yarayan kod tuple olarak verilir 
   users = User.objects.all().values("email") # user içerisindeki emailleri döndermemize yarayan kod obje  olarak verilir 
   # print(list(users)) #[{'email': ''}, {'email': 'kemal.liya19@gmail.com'}, {'email': 'mehmettalnn@gmail.com'}, {'email': 'bbb@gmail.com'}] bunu veriri
   user_list = []
   for i in list(users):
     user_list.append(i["email"]) 
     
   print(user_list)
   
   if request.method == "POST":
      title = request.POST.get("title")
      text = request.POST.get("text")
     

     
      try: 
         send_mail(
            title,
            text,
            EMAIL_HOST_USER,
            user_list,
            fail_silently= False, 
         
         )
         messages.success(request,"Mesajınız Başarıyla gönderildi")
      except:
         messages.error(request,"Mesajınız Gönderilemedi")
      return redirect("emailSendPage")
   
   
   context ={}
   return render(request, "email-send.html", context)