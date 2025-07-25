from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from relationship_app.helpers import check_role

@user_passes_test(check_role('Librarian'))
def librarian_view(request):
    return render(request, 'librarian_view.html')