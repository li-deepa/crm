# Generated by Django 4.0.3 on 2022-05-07 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_product_product_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_pic',
            field=models.ImageField(blank=True, default='3.JPG', null=True, upload_to=''),
        ),
    ]