# Generated by Django 5.1.6 on 2025-02-24 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_product_business_business_signature_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.FileField(upload_to='business_media/', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='media',
            name='media_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10, verbose_name='Media Type'),
        ),
    ]
