# Generated by Django 5.1.4 on 2024-12-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0002_alter_category_order_alter_resource_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
