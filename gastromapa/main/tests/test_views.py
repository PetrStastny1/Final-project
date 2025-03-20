import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Category, Business
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_category_create_success():
    """Test úspěšného vytvoření nové kategorie"""
    client = APIClient()

    data = {
        "name": "Test Category",
        "description": "A test category description",
    }
    response = client.post(reverse("category-list"), data)

    assert response.status_code == 201
    assert response.data["name"] == "Test Category"
    assert response.data["description"] == "A test category description"


@pytest.mark.django_db
def test_category_create_missing_name():
    """Test neúspěšného vytvoření kategorie bez `name`"""
    client = APIClient()

    data = {
        "description": "A test category description",
    }
    response = client.post(reverse("category-list"), data)

    assert response.status_code == 400  # Očekávaná chyba (Bad Request)
    assert "name" in response.data  # Ověření, že `name` chybí v odpovědi


@pytest.mark.django_db
def test_business_list_with_data():
    """Test získání seznamu podniků (není prázdný)"""
    client = APIClient()

    user = User.objects.create_user(username="testuser", password="testpassword")
    category = Category.objects.create(name="Food", description="Restaurants and Cafes")

    Business.objects.create(
        name="Test Business 1", address="123 Test St", category=category, owner=user
    )
    Business.objects.create(
        name="Test Business 2", address="456 Test Ave", category=category, owner=user
    )

    response = client.get(reverse("business-list"))
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Test Business 1"
    assert response.data[1]["name"] == "Test Business 2"


@pytest.mark.django_db
def test_business_list_empty():
    """Test získání podniků, pokud žádné podniky neexistují"""
    client = APIClient()

    response = client.get(reverse("business-list"))
    assert response.status_code == 200
    assert len(response.data) == 0  # Očekáváme prázdný seznam


@pytest.mark.django_db
def test_business_create_authenticated():
    """Test úspěšného vytvoření podniku autentizovan"""