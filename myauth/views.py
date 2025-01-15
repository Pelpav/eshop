from django.shortcuts import render, redirect

# def login(request):
#     return render(request, 'myauth/login.html', {})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    from django.contrib.auth.forms import UserCreationForm
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        from .models import Customer
        Customer(user=user).save()
        from django.contrib.auth import authenticate, login
        login(request, 
            authenticate(username=user.username, password=form.cleaned_data['password1']))
        return redirect('home')
    return render(request, 'myauth/register.html', {'form': form})