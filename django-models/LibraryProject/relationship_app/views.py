from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import user_passes_test


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('list_books')  # Change this to any page you like
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def check_role(role):
    def inner(user):
        return hasattr(user, 'userprofile') and user.userprofile.role == role
    return inner

@user_passes_test(check_role('Admin'))
def admin_view(request):
    return render(request, 'admin_view.html')

@user_passes_test(check_role('Librarian'))
def librarian_view(request):
    return render(request, 'librarian_view.html')
    
@user_passes_test(check_role('Member'))
def member_view(request):
    return render(request, 'member_view.html')

def list_books(request):
    return render(request, 'books.html')

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'