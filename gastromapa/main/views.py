from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Business, Review, Category, Media
from .forms import ReviewForm, BusinessForm
from .serializers import BusinessSerializer, ReviewSerializer, CategorySerializer


# HTML Views
def home(request):
    """Úvodní stránka aplikace."""
    return render(request, 'home.html')


def business_list(request):
    """Seznam všech podniků."""
    businesses = Business.objects.all().order_by('name')
    return render(request, 'business_list.html', {'businesses': businesses})


def business_detail(request, id):
    """Detail vybraného podniku."""
    business = get_object_or_404(Business, id=id)
    reviews = business.reviews.all()
    media_items = business.media.all()
    return render(request, 'business_detail.html',
                  {'business': business, 'reviews': reviews, 'media_items': media_items})


def business_search(request):
    """Vyhledávání podniků podle klíčového slova."""
    query = request.GET.get('q', '').strip()
    businesses = Business.objects.filter(name__icontains=query) if query else []
    return render(request, 'business_search.html', {'query': query, 'businesses': businesses})


@user_passes_test(lambda user: user.is_staff)
def admin_dashboard(request):
    """Dashboard pro administrátora."""
    businesses = Business.objects.all()
    return render(request, 'admin_dashboard.html', {'businesses': businesses})


@login_required
def add_review(request, id):
    """Přidání recenze k podniku."""
    business = get_object_or_404(Business, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = business
            review.user = request.user
            review.save()
            messages.success(request, "Recenze byla úspěšně přidána.")
            return redirect('business_detail', id=business.id)
        else:
            messages.error(request, "Recenzi se nepodařilo uložit. Zkontrolujte formulář.")
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'business': business})


@user_passes_test(lambda user: user.is_staff)
def add_business(request):
    """Přidání nového podniku pro administrátora."""
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user  # důležité: nastavíme vlastníka
            business.save()
            form.save_m2m()
            messages.success(request, "Podnik byl úspěšně přidán.")
            return redirect('business_list')
        else:
            messages.error(request, "Podniku se nepodařilo uložit. Zkontrolujte formulář.")
    else:
        form = BusinessForm()
    return render(request, 'add_business.html', {'form': form})


@user_passes_test(lambda user: user.is_staff)
@require_POST
def business_delete(request, id):
    """Smazání podniku (pouze admin, POST)."""
    business = get_object_or_404(Business, id=id)
    category_id = business.category_id
    business.delete()
    messages.success(request, "Podnik byl smazán.")
    return redirect('category_detail', category_id=category_id)


def category_list(request):
    """Výpis seznamu kategorií."""
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_detail(request, category_id):
    """Detail vybrané kategorie."""
    category = get_object_or_404(Category, id=category_id)
    businesses = category.businesses.all()
    return render(request, 'category_detail.html', {'category': category, 'businesses': businesses})


def register_view(request):
    """Registrace nového uživatele."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registrace proběhla úspěšně, nyní se můžete přihlásit.")
            return redirect('login')
        else:
            messages.error(request, "Registraci se nepodařilo dokončit. Zkontrolujte formulář.")
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """Přihlášení uživatele."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Vítejte zpět, {user.username}!")
                return redirect('home')
        else:
            messages.error(request, "Přihlášení se nepodařilo. Zkontrolujte své údaje.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def media_list(request):
    """Seznam mediálních souborů."""
    media_items = Media.objects.all()
    return render(request, 'media_list.html', {'media_items': media_items})


# API Views for REST Framework
class BusinessViewSet(ModelViewSet):
    """ViewSet pro seznam a detaily podniků."""
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class CategoryViewSet(ModelViewSet):
    """ViewSet pro seznam a detaily kategorií."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    """ViewSet pro seznam a detaily recenzí."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# Ručně definované API endpointy
@api_view(['GET'])
def api_business_list(request):
    """Seznam všech podniků."""
    businesses = Business.objects.all()
    serializer = BusinessSerializer(businesses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_business_detail(request, id):
    """Detail podniku podle ID."""
    business = get_object_or_404(Business, id=id)
    serializer = BusinessSerializer(business)
    return Response(serializer.data)


@api_view(['GET'])
def api_review_list(request):
    """Seznam všech recenzí."""
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_category_list(request):
    """Seznam všech kategorií."""
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)