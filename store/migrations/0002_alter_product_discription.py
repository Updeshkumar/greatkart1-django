# Generated by Django 4.0.3 on 2022-09-08 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discription',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
