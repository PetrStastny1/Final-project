from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Třída představující kategorii firem."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Třída představující produkt."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Business(models.Model):
    """Třída reprezentující obchod."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='businesses'
    )
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='businesses', blank=True)
    signature_product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='signature_for_business',
    )
    image = models.ImageField(
        upload_to='business_images/', blank=True, null=True
    )
    video = models.FileField(
        upload_to='business_videos/', blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        """Metadata pro Business."""
        verbose_name = "Business"
        verbose_name_plural = "Businesses"


class Review(models.Model):
    """Třída pro recenze."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.business.name} - {self.rating}/10"


class Media(models.Model):
    """Třída pro média."""
    MEDIA_TYPES = (('image', 'Image'), ('video', 'Video'))
    business = models.ForeignKey(
        'Business', on_delete=models.CASCADE, related_name='media'
    )
    media_type = models.CharField(
        max_length=10, choices=MEDIA_TYPES, verbose_name='Media Type'
    )
    file = models.FileField(upload_to='business_media/', verbose_name='File')
    description = models.TextField(blank=True, verbose_name='Description')

    def __str__(self):
        return f"{self.get_media_type_display()} for {self.business.name}"
