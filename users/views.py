from django.contrib import messages
from users.models import User
from .forms import UserRegisterForm
from django.views import View
from django.shortcuts import render, redirect


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password2'])
            messages.success(request, 'registered successfully', extra_tags='success')
            return redirect('home:home')
        messages.error(request, 'enter valid information', extra_tags='danger')
        return render(request, self.template_name, {'form': form})
