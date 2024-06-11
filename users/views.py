from django.views import View
from django.shortcuts import render


class UsersView(View):
    def get(self, request):
        return render(request, 'users/users.html')
