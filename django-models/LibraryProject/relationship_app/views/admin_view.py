from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from relationship_app.helpers import check_role


@user_passes_test(check_role('Admin'))
def admin_view(request):
    return render(request, 'admin_view.html')