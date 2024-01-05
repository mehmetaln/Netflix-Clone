from django.shortcuts import render
from appUser.models import *
from appMy.models import *



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
   }
   return render(request, 'browse-index.html', context)
