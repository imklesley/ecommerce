# Generated by Django 3.1.4 on 2020-12-11 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20201210_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingadress',
            name='a',
        ),
    ]