# Generated by Django 4.0.3 on 2022-09-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='discription',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]