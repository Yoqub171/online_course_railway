from django.shortcuts import render,redirect
from .forms import LoginForm, CustomUserRegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


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
    return render(request,'users/login.html',{'form':form})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:home')
    

def register_page(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ro‘yxatdan o‘tish muvaffaqiyatli bo‘ldi. Endi kirishingiz mumkin.')
            return redirect('users:login_page')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
