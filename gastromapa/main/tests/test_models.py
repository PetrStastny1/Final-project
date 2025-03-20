import pytest
from django.contrib.auth.models import User
from main.models import Category, Business, Product, Review


@pytest.mark.django_db
def test_category_creation():
    """Test pro vytvoření nové kategorie"""
    category = Category.objects.create(name="Food", description="All about food")
    assert category.name == "Food"
    assert category.description == "All about food"


@pytest.mark.django_db
def test_business_creation():
    """Test pro vytvoření nového podniku"""
    # Vytvoření uživatele
    user = User.objects.create_user(username="testuser", password="testpassword")

    # Vytvoření kategorie
    category = Category.objects.create(
        name="Restaurant", description="Restaurants and Cafes"
    )

    # Vytvoření produktu
    product = Product.objects.create(name="Coffee")

    # Vytvoření podniku
    business = Business.objects.create(
        name="Test Business",
        address="123 Test Street",
        category=category,
        description="Great coffee shop",
        owner=user,
    )
    business.products.add(product)  # Přidání produktu do podniku

    assert business.name == "Test Business"
    assert business.address == "123 Test Street"
    assert business.category.name == "Restaurant"
    assert business.owner.username == "testuser"
    assert business.products.count() == 1  # Ověření přidání produktu


@pytest.mark.django_db
def test_review_creation():
    """Test pro vytvoření recenze podniku"""
    # Vytvoření uživatele
    user = User.objects.create_user(username="reviewer", password="testpassword")

    # Vytvoření kategorie
    category = Category.objects.create(name="Entertainment", description="Fun places")

    # Vytvoření podniku
    business = Business.objects.create(
        name="Cinema",
        address="456 Movie Lane",
        category=category,
        owner=user,
    )

    # Vytvoření recenze
    review = Review.objects.create(
        user=user,
        business=business,
        rating=9,
        comment="Great experience, loved the movies!"
    )

    assert review.business.name == "Cinema"
    assert review.user.username == "reviewer"
    assert review.rating == 9
    assert review.comment == "Great experience, loved the movies!"
