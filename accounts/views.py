from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from dashboard.services.summary_service import get_dashboard_summary

from .forms import CustomUserCreationForm


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard-home")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    summary = get_dashboard_summary(request.user)

    return render(
        request, "accounts/profile.html", {"user": request.user, "summary": summary}
    )
