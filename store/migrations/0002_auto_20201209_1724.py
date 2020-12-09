# Generated by Django 3.1.4 on 2020-12-09 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('In the cart', 'In the cart'), ('Waiting for Payment', 'Waiting for Payment'), ('Preparation', 'Preparation'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], default=('Waiting for Payment', 'Waiting for Payment'), max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
