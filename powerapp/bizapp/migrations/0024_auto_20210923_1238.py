# Generated by Django 2.0 on 2021-09-23 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bizapp', '0023_auto_20210923_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bizapp.Product'),
        ),
    ]
