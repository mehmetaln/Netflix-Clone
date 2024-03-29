from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.models import User
from django.contrib import messages #mesajları çekmmeize yarar
from appUser.models import * 
from django.core.mail import send_mail #mail gönderebilmemzi için gerekli  
from netflix5haziran.settings import EMAIL_HOST_USER 
from django.utils.crypto import get_random_string # random_string çekmemzie yarar

def profilePage(request):
   # ==================================

   profile_list = Profile.objects.filter(user=request.user)
   
   if request.method == "POST":
      submit = request.POST.get("submit")
      if submit == "profileCreate":
         title = request.POST.get("title")
         image = request.FILES.get("image")
         if title and image:
            if len(profile_list) < 4:
               profile = Profile(title=title, image=image, user= request.user)
               profile.save()
               return redirect("profilePage") # yönlendirme
            else:
               messages.error(request, "Çok Zorlama Kardeşim!!!")
         else:
            messages.error(request, "Boş bırakılan yerler var!!")
      elif submit == "profileDelete":
         profileid = request.POST.get("profileid")
         profile = Profile.objects.get(id=profileid)
         
         title = request.POST.get("title")
         image = request.FILES.get("image")

         profile.title = title
         if image:
            profile.image = image
         
         profile.save()
         return redirect("profilePage")
      
   context = {
      "profile_list":profile_list,
   }
   return render(request, 'profile.html', context)

def profileDelete(request, pid):
   profile = Profile.objects.get(id=pid)
   profile.delete()
   return redirect("profilePage")

def profileBrowse(request, pid):
   profile = Profile.objects.get(id=pid) # Giriş Yapılan Profile
   user_profile_list = Profile.objects.filter(user=request.user) # Kullanıcının Tüm Profilleri
   user_profile_list.update(islogin=False) # Tüm Profilleri Çıkış Yaptır.
   profile.islogin = True # Giriş Yapanı True Yap
   profile.save()
   return redirect("browsePage2")
   
   

def hesapPage(request):
   profile = Profile.objects.get(user=request.user, islogin=True)

   if request.method =="POST":
      submit = request.POST.get("submit")
      if submit=="emailSubmit":
         email = request.POST.get("email")
         password = request.POST.get("password")
         if email and password: 
            # email.strip(" ") and password.strip(" ")
            # strip boşluk bırakarak geçmesini engelmmek için
            if request.user.check_password(password): # parolayı kontrol etmemize yarar   
               request.user.email =email
               request.user.save()
               messages.success(request,"Email adresiniz başarı ile değişştirildi..")
               logout(request)
               return redirect('loginPage')
               # return redirect(loginPage)
            else:
               messages.error(request, "Şifreniz yanlış..")
         else:
            messages.error(request,"Boş bırakılan yerler var")
   
            
      elif submit =="passwordSubmit":
         password =request.POST.get("password")
         password1 =request.POST.get("password1")
         password2 =request.POST.get("password2")
         if password and password1 and password2:
            if request.user.check_password(password): # parolayı kontrol etmemize yarar   
               if password1 == password2:
                  request.user.set_password(password1) # parolayı değiştirmemzi yarar
                  request.user.save()
                  messages.success(request, "Şifre Değiştirmeniz Başarılı")
                  logout(request)
                  return redirect('loginPage')
               else:
                  messages.error(request, "Parolanız Eşleşimiyor")
            else:
               messages.error(request,"Parolanız yanlış")        
         else:
            messages.error(request, "boş bırakılan yerler var")           
                                 
                                 
      
      elif submit =="telSubmit":
         tel = request.POST.get("tel")
         password = request.POST.get("password")
         if tel and password: 
            # email.strip(" ") and password.strip(" ")
            # strip boşluk bırakarak geçmesini engelmmek için
            if request.user.check_password(password): # parolayı kontrol etmemize yarar   
               request.user.usermy.tel =tel
               request.user.usermy.save()
               messages.success(request,"Telefonunuz Başarı ile Değiştirildi")
               # return redirect(loginPage)
               logout(request)
               return redirect('loginPage')
            else:
               messages.error(request, "Şifreniz Yanlış")
         else: 
            messages.error(request, "Boş bırakılan yerler var")
      
   
      return redirect('hesapPage')
   context = {
      "profile":profile
   }
   return render(request, 'hesap.html', context)

def videoPage(request):
   context = {}
   return render(request, 'video.html', context)

def loginPage(request):
   
   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      remember = request.POST.get("rememberme")


      if remember:
         request.session.set_expiry(1209600)
      else:
         request.session.set_expiry(0)
         
      
      user = authenticate(username=username, password=password)
      if user is not None:
         login(request, user)
         messages.success(request, "Girişiniz Yapıldı...")
         return redirect("profilePage")
      else:
         messages.error(request, "Kullanıcı adı veya şifre yanlış!!")
         return redirect("loginPage")
         
   
   context = {}
   return render(request, 'user/login.html', context)

def registerPage(request):
   
   if request.method == "POST":
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      email = request.POST.get("email")
      username = request.POST.get("username")
      password1 = request.POST.get("password1")
      password2 = request.POST.get("password2")
      check_site = request.POST.get("check-site")
      check_kvkk = request.POST.get("check-kvkk")

      if fname and lname and email and username and password1 and password2 and check_site and check_kvkk:
         if password1 == password2:
            if not User.objects.filter(username=username).exists():
               if not User.objects.filter(email=email).exists():
                  random_link =get_random_string(44)
                  email_link =   "http://"+request.get_host()+"/emailactive/"+random_link
                  user = User.objects.create_user(username=username, password=password1, email=email,first_name=fname, last_name=lname )
                  user.is_active = False
                  user.save()
                  
                  packed =Packed.objects.get(slug = "normal-paket")
                  print("packed ===",packed)
                  usermy =Usermy(user=user,user_active = random_link,packed=packed)
                  usermy.save()

                  send_mail(
                     "Netflix Email Onaylayınız",
                     f"Lütfen Email hesabınızı onaylayınız:{email_link}",
                     EMAIL_HOST_USER,
                     [email],
                     fail_silently=False
                  )
                  
                  messages.success(request, "Kaydınız başarıyla oluşturuldu...")
                  return redirect("loginPage")
               else:
                  messages.error(request, "Bu email zaten kullanılıyor !!")
            else:
               messages.error(request, "Bu kullanıcı adı zaten kullanılıyor !!")
         else:
            messages.error(request, "Şifreler eşleşmiyor !!")
      else:
         messages.error(request, "Lütfen boş bırakılan yerleri doldurun !!")
                  
   context = {}
   return render(request, 'user/register.html', context)



def logoutPage(request):
   logout(request)
   return redirect("loginPage")