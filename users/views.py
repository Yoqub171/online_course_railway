from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import LoginForm,RegisterModelForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # email = request.POST.get('email','')
            # password = request.POST.get('password','')
            user = authenticate(request,email = cd['email'],password = cd['password'])
            
            if user:
                login(request,user)
                return redirect('shop:home')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Username or Password incorrect'   
                )
                pass
            # messages
    return render(request,'users/login.html',{'form':form})



def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:home')
    
    
def register_page(request):
    form = RegisterModelForm()
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('shop:home')
    return render(request, 'users/register.html', {'form': form})
