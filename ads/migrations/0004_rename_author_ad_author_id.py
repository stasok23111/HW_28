# Generated by Django 4.2.1 on 2023-05-12 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_remove_ad_address_ad_category_ad_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='author',
            new_name='author_id',
        ),
    ]
