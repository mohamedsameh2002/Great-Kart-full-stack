# Generated by Django 4.2.3 on 2023-08-15 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_user_profile_reviewrating_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
