from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, UserProfile
from django.contrib import messages
from django.db.models import Q  # For search filtering

# Home Page – Display & Search Books

def home(request):
    total_books = Book.objects.count()
    recent_books = Book.objects.order_by('-id')[:3]  # last 3 added
    context = {
        'total_books': total_books,
        'recent_books': recent_books
    }
    return render(request, 'lib/user&admin.html', context)


def index(request):
    query = request.GET.get('q')  # Get the search keyword from URL
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'lib/index.html', {'books': books, 'query': query})

def userhome(request):
    query = request.GET.get('q')  # Get the search keyword from URL
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'lib/userhome.html', {'books': books, 'query': query})

# Add New Book
def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        publication_year = request.POST['publication_year']
        isbn = request.POST['isbn']

        Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year,
            isbn=isbn
        )
        messages.success(request, "Book added successfully!")
        return redirect('index')
    return render(request, 'lib/add_book.html')

# Edit Book
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.publication_year = request.POST['publication_year']
        book.isbn = request.POST['isbn']
        book.save()
        messages.success(request, "Book updated successfully!")
        return redirect('index')
    return render(request, 'lib/edit_book.html', {'book': book})

# Delete Book
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    messages.success(request, "Book deleted successfully!")
    return redirect('index')



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(username=username, password=password)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('userhome')
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, 'lib/userhome.html')
    return render(request, 'lib/login.html')



def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 🧩 Validation checks
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'lib/register.html')

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'lib/register.html')

        # ✅ Save user
        UserProfile.objects.create(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    # ✅ Always return something for GET requests
    return render(request, 'lib/register.html')


def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # For simplicity, using hardcoded admin credentials
        if username == "admin" and password == "admin123":
            messages.success(request, "Welcome Admin!")
            return redirect('owner')
        else:
            messages.error(request, "Invalid admin credentials.")
            return render(request, 'lib/adminlogin.html')
    return render(request, 'lib/adminlogin.html')
def owner(request):
    query = request.GET.get('q')  # Get the search keyword from URL
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'lib/admin.html', {'books': books, 'query': query})


def users_list(request):
    # Get search query
    query = request.GET.get('q', '')

    # Filter users by username or email if search term exists
    if query:
        userprofile = UserProfile.objects.filter(
            username__icontains=query
        ) | UserProfile.objects.filter(
            email__icontains=query
        )
    else:
        userprofile = UserProfile.objects.all()

    # Render the template
    return render(request, 'lib/users.html', {
        'userprofile': userprofile,
        'query': query
    })

