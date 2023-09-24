from django.contrib.auth import logout
from django.views import View
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class RegisterView(View):
    form_class = RegisterForm
    template_name = "users/signup.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)

        print(form)

        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаю {username}. Ваш аккаунт успішно створено")
            return redirect(to="users:login")

        return render(request, self.template_name, {"form": form})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'