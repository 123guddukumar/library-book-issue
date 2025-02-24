from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import BookIssue
from datetime import datetime

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect('login')
    return render(request, 'books/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'books/login.html')

@login_required
def dashboard(request):
    issues = BookIssue.objects.filter(user=request.user, returned=False)
    # Check for return date and send email
    for issue in issues:
        if issue.return_date == datetime.now().date():
            send_mail(
                'Book Return Reminder',
                f'Dear {request.user.username},\nPlease return "{issue.book_name}" to the library today.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
    return render(request, 'books/dashboard.html', {'issues': issues})

def home(request):
    if request.method == 'POST':
        book_number = request.POST['book_number']
        book_name = request.POST['book_name']
        return_date = request.POST['return_date']
        
        if request.user.is_authenticated:
            book_issue = BookIssue.objects.create(
                user=request.user,
                book_number=book_number,
                book_name=book_name,
                return_date=return_date
            )
            # Send email to admin
            send_mail(
                'New Book Issue Request',
                f'User: {request.user.username}\nBook: {book_name}\nNumber: {book_number}\nReturn Date: {return_date}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            return redirect('dashboard')
    return render(request, 'books/home.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')