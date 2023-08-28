from django.contrib.auth import logout
from django.views import View
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages


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
