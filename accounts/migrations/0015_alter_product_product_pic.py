# Generated by Django 4.0.3 on 2022-05-07 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
