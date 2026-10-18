from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def profile_page(request):
     return render(request, "accounts/profile_page.html",{
          "user": request.user
     })