from django.shortcuts import render, redirect
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
import pdb;
import threading
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from . utils import token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send(fail_silently=False)


def LoginView(request):
    if request.method=="GET":
        return render(request, 'authentication/login.html')
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            if username=='a1' or username=='a2' or username=='a3' :
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    messages.success(request, 'Welcome '+user.username+'! You are now logged in!')
                    return redirect('nDashboard')
                else:
                    messages.error(request, 'Invalid credentials, please enter the correct credentials')
                    return redirect('nlogin')
            else:
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    messages.success(request, 'Welcome '+user.username+'! You are now logged in!')
                    return redirect('ndashboard')
                else:
                    messages.error(request, 'Invalid credentials, please enter the correct credentials')
                    return redirect('nlogin')
        else:
            messages.error(request, 'Please fill all fields!')
            return render(request, 'authentication/login.html')



def LogoutView(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You have been logged out successfully!')
        return redirect('nlogin')
    else:
        messages.error(request, 'You tried to access a prohibited url!!')
        return redirect('nlogin')
        
                
def RequestPasswordResetEmail(request):
    if request.method == "GET":
        return render(request, 'authentication/resetpassword.html')
    
    if request.method == "POST":
        email = request.POST['email']
        context={'values':request.POST}

        if not validate_email(email): 
            messages.error(request, 'Please enter a valid email id.')
            return render(request, 'authentication/resetpassword.html', context)
        if not User.objects.filter(email=email).exists() or not validate_email(email): 
            messages.error(request, 'This email is not registered with us. Please register yourself first.')
            return render(request, 'authentication/resetpassword.html', context)
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        if user.exists():
            email_contents = {
                    'user': user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0])),
                    'token': PasswordResetTokenGenerator().make_token(user[0]),
                }

            link = reverse('set-new-password', kwargs={'uidb64': email_contents['uid'], 'token': email_contents['token']})
            email_subject = 'Reset your password'
            reset_url = 'http://'+current_site.domain+link
            email = EmailMessage(
                    email_subject,
                    'Hi there!, Please click the link below to set a new password for your account \n'+ reset_url,
                    'noreply@semycolon.com',
                    [email],
                )
            EmailThread(email).start()
            messages.success(request, 'We have sent you an email with the link to reset your password')
        
                
        return render(request, 'authentication/resetpassword.html') 



def SetNewPasswordView(request,uidb64, token):
    if request.method=="GET":
        context = {'uidb64':uidb64,'token':token}
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link is invalid or has been used earlier, please request a new one.')
                return render(request, 'authentication/resetpassword.html')
        except Exception as a: 
            pass   
        return render( request, 'authentication/setnewpass.html', context)

    if request.method=="POST":
        context = {'uidb64':uidb64,'token':token}
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Passwords do not match. Re-enter both again.')
            return render( request, 'authentication/setnewpass.html', context)
        if len(password1)<6:
            messages.error(request, 'Enter a password greater than 6 characters.')
            return render( request, 'authentication/setnewpass.html', context)
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=id)
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password reset successful. You can login with the new password.')
            return redirect('nlogin')
        except Exception as ex:
            messages.info(request, 'Something went wrong, try again.')
            return render( request, 'authentication/setnewpass.html', context)          
            

        



