# Generated by Django 4.2.7 on 2023-12-24 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0002_alter_userprofile_address_alter_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
