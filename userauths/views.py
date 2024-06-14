from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from userauths.forms import UserRegisterForm, CustomPasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

User = get_user_model()

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .utils import generate_activation_code
from userauths.models import User
from django.db.models import Q

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists. Please choose a different one.")
                return redirect('userauths:register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists. Please choose a different one.")
                return redirect('userauths:register')
            
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive until activation
            user.activation_code = generate_activation_code()  # Generate activation code
            user.save()
            
            # Send activation email
            subject = 'Activate Your Account'
            message = f'Hi {user.username},\n\nThank you for registering. Your activation code is: {user.activation_code}\n\nBest regards,\nTeam Vishw'
            from_email = 'khatik.rk111@gmail.com'  # Replace with your email
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            messages.success(request, "Your account has been created. Please check your email for the activation code.")
            return redirect("userauths:activate")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f"{error}")
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")

        # Try to get user by username or email
        try:
            user_obj = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
        except User.DoesNotExist:
            messages.warning(request, "Invalid credentials.")
            return redirect("userauths:login")  # Redirect back to the login page

        # Check password
        if user_obj.check_password(password):
            if user_obj.is_active:
                login(request, user_obj)
                messages.success(request, "You are logged in")
                return redirect("core:index")
            else:
                messages.warning(request, "Your account is not activated. Please check your email for the activation code.")
                return redirect("userauths:login")  # Redirect back to the login page
        else:
            messages.warning(request, "Invalid credentials.")
            return redirect("userauths:login")  # Redirect back to the login page

    context = {}
    return render(request, "userauths/login.html", context)





@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect('userauths:login')


from django.urls import reverse_lazy


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'userauths/change-password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password was changed successfully')
        return response

    def form_invalid(self, form):
        error_messages = form.errors
        for field, errors in error_messages.items():
            for error in errors:
                if field == '__all__':  # Global form errors
                    messages.warning(self.request, error)
                else:
                    messages.warning(self.request, f"{error}")

        return super().form_invalid(form)

    


def activate_account_view(request):
    if request.method == 'POST':
        activation_code = request.POST.get('code')

        # Check if the activation code exists in the database
        try:
            user = User.objects.get(activation_code=activation_code)
        except User.DoesNotExist:
            messages.warning(request, 'Invalid activation code. Please try again.')
            return redirect('userauths:activate')  # Redirect back to the activation page for another attempt

        # Activate the user's account
        user.is_active = True
        user.activation_code = None  # Clear activation code after activation
        user.save()

        # Log in the user
        login(request, user)

        messages.success(request, 'Your account has been activated successfully!')
        return redirect('core:index')  # Redirect to the index page after activation

    return render(request, 'userauths/activate.html')






User = get_user_model()








def activate_account(request):
    if request.method == "POST":
        email = request.POST.get("email_activate")

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.warning(request, "Your account is already activated.")
            else:
                # Generate activation code
                user.activation_code = generate_activation_code()  # Generate activation code
                user.save()
                
                # Send activation email
                subject = 'Activate Your Account'
                message = f"""Hi {user.username},

Thank you for registering with us! To complete the registration process and start using your account, please use the following activation code:
Activation Code: {user.activation_code}

Enter this activation code on the activation page to activate your account.

If you didn't register for an account with us, please disregard this email.

Best regards,
Vishw Electronics"""
                from_email = 'khatik.rk111@gmail.com'  # Replace with your email
                to_email = user.email
                send_mail(subject, message, from_email, [to_email])
                
                # Save the activation code to the user object
                
                
                messages.success(request, "Activation code sent successfully. Please check your email.")
                return redirect("userauths:activate-code")
        except User.DoesNotExist:
            messages.warning(request, "No user found with this email address.")

    return render(request, "userauths/activate_account.html")

def activate_code(request):
  if request.method == 'POST':
        activation_code = request.POST.get('activation_code')

        # Check if the activation code exists in the database
        try:
            user = User.objects.get(activation_code=activation_code)
        except User.DoesNotExist:
            messages.warning(request, 'Invalid activation code. Please try again.')
            return redirect('userauths:activate-code')  # Redirect back to the activation page for another attempt

        # Activate the user's account
        user.is_active = True
        user.activation_code = None  # Clear activation code after activation
        user.save()
        
        messages.success(request, "Your account is activated successfully, now you can login")
        return redirect('userauths:login')

  return render(request, "userauths/activate_code.html")


