# Generated by Django 5.1.4 on 2024-12-12 08:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('image', models.ImageField(blank=True, upload_to='category_images/')),
                ('order', models.PositiveSmallIntegerField(blank=True, default=0, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminPanel.category')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('link', models.URLField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='resource_images/')),
                ('description', models.TextField(blank=True)),
                ('author', models.CharField(blank=True, max_length=100)),
                ('order', models.PositiveSmallIntegerField(blank=True, default=0, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_recommended', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminPanel.category')),
            ],
        ),
    ]
