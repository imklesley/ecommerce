# Generated by Django 3.1.4 on 2020-12-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20201213_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
    ]