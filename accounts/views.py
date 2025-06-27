from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import CustomUser, Subject, Document
from .forms import CustomUserCreationForm, DocumentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'accounts/home.html')

def subjects_list(request):
    subjects = Subject.objects.prefetch_related('subsubjects').all()
    return render(request, 'accounts/subjects.html', {'subjects': subjects})

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get user's recent uploaded documents
    recent_uploads = Document.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')[:5]
    
    # Calculate user statistics
    total_uploads = Document.objects.filter(uploaded_by=request.user).count()
    
    context = {
        'user': request.user,
        'recent_uploads': recent_uploads,
        'total_uploads': total_uploads,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'accounts/edit_profile.html')

def upload_document_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    from .models import Subject
    subjects = Subject.objects.all()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            # Save has_correction and corrected fields
            document.has_correction = form.cleaned_data.get('has_correction', False)
            document.corrected_file = form.cleaned_data.get('corrected_file')
            document.corrected_link = form.cleaned_data.get('corrected_link')
            document.save()
            # Optionally, add a success message
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'accounts/upload_document.html', {'form': form, 'subjects': subjects})
