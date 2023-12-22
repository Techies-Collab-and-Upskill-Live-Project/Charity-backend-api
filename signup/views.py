from django.shortcuts import render ,redirect
from .forms import RegistrationForm # importing  RegistrationForm from forms.py
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
#access the homepage by localhost:8000/accounts because  path('accounts/', include('signup.urls'))from the project urls.py

# dummy Homepage View to check that the login was working

def homepage(request):
    return render(request, 'signup/homepage.html') # Rendering the homepage template



# registration view

def Registration(request):
    form = RegistrationForm()
    if request.method =="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login') #redirects to the login page
    return render(request,"signup/registration.html",{"form":form} )


#login view

def LoginView(request):
    if request.method == "POST": 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/accounts/')
    else:
        form = AuthenticationForm()

    return render(request, "signup/login.html", {"form": form})

#logout view

def LogoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login') 
    return render(request, 'signup/logout.html')
        

        
