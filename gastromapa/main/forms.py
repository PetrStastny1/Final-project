from django import forms
from .models import Review, Business


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Hodnocení (1-10)',
            'comment': 'Komentář',
        }


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'address', 'description', 'category']
        labels = {
            'name': 'Název podniku',
            'address': 'Adresa',
            'description': 'Popis podniku',
            'category': 'Kategorie',
        }
