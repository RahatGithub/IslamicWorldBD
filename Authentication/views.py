from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    def get(self, request):
        return render(request, 'Authentication/login.html') 

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_superuser:  # Ensure the user is a superadmin
                login(request, user)  # Log the user in
                # Redirect with the user ID and other details
                return redirect('/adminPanel/categories/')
            else:
                # If the user is not a superadmin
                return render(request, 'Authentication/login.html', {"error": "You do not have admin access."})
        else:
            # Invalid credentials
            return render(
                request,
                "Authentication/login.html",
                {"error": "Invalid username or password."},
            )


class LogoutView(View):
    def get(self, request):
        # Log the user out
        logout(request)
        # Redirect to the login page or homepage
        return redirect('/')