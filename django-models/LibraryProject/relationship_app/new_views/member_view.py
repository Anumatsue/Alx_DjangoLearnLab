from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
#from relationship_app.helpers import check_role


def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')

#@user_passes_test(check_role('Member'))
#def member_view(request):
#    return render(request, 'member_view.html')